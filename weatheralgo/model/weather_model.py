from fake_useragent import UserAgent
import logging

import time
import random
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from weatheralgo import trade_functions
from weatheralgo import scrape_functions
from weatheralgo import util_functions


# Initialize Selenium WebDriver
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-data")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=3')
    ua = UserAgent()
    chrome_options.add_argument(f"user-agent={ua.random}")
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)



# Main function to scrape and process data
def scrape_dynamic_table(driver, market, timezone, url, xml_url, lr_length, scraping_hours, 
                         minutes_from_max, count, yes_price, balance_min):
    

    util_functions.logging_settings()
    temperatures = []
    dates = []
    
    restart_threshold = 20  # Restart WebDriver every 50 iterations
    loop_counter = 0

    rand = random.randint(2, 4)

    today = datetime.now(timezone).date()
    expected_high_date = scrape_functions.xml_scrape(xml_url, timezone)[0]

    while True:
        
        current_local_date = datetime.now(timezone).date()
        if today != current_local_date:
           today = current_local_date
           expected_high_date = scrape_functions.xml_scrape(xml_url, timezone)[0]
            
        permission_scrape = scrape_functions.permission_to_scrape(market=market, 
                                                                  timezone=timezone, 
                                                                  scraping_hours=scraping_hours, 
                                                                  expected_high_date=expected_high_date,
                                                                 )
        
        datetemp_append = scrape_functions.date_temp_append(
                                                            driver=driver, 
                                                            url=url, 
                                                            timezone=timezone, 
                                                            dates=dates
            
                                                            )
        
        trade_made_today = scrape_functions.trade_today(
                                                        market=market,
                                                        timezone=timezone
                                                        )
        

        time.sleep(rand)
        try:
            if permission_scrape and datetemp_append:
             
                current_date = datetemp_append[0]
                current_temp = datetemp_append[1]
                
                dates.append(current_date)
                temperatures.append(current_temp)
                
                logging.info(f"Date: {dates}")
                logging.info(f"Temperature: {temperatures}")
                
                current_temp_is_max = trade_functions.if_temp_reaches_max(current_temp=current_temp, 
                                                                            market = market, 
                                                                            yes_price=yes_price,
                                                                            count=count,
                                                                            balance_min=balance_min)
                
                trade_criteria = trade_functions.trade_criteria_met(temperatures=temperatures, 
                                                    lr_length=lr_length,
                                                    timezone=timezone,
                                                    expected_high_date=expected_high_date, 
                                                    minutes_from_max= minutes_from_max,
                                                    market=market)
                
                trade_execute = trade_functions.trade_execution(temperatures=temperatures,
                                                    market=market,
                                                    yes_price=yes_price,
                                                    count=count, 
                                                    balance_min=balance_min)
                if current_temp_is_max:
                    logging.info('Max Temperature Reached')


                if trade_criteria:
                    logging.info('Trade Criteria Met')

                    if trade_execute:
                        logging.info('Order Exectured')
                  
                else:
                    time.sleep(rand)
                   
            elif trade_made_today:
                temperatures = []
                dates = []
                
                is_order_filled = util_functions.order_filled(market)
                if is_order_filled:
                    logging.info(f'Order filled and saved: {market}')
                else:
                    continue
               
            else:
                continue
          
        except Exception as e:
            logging.error(f"in main loop: {e}")

            loop_counter += 1
            if loop_counter >= restart_threshold:
                logging.info("Restarting WebDriver to prevent stale sessions...")
                driver.quit()
                driver = initialize_driver()
                loop_counter = 0  # Reset counter

            
            time.sleep(rand)




# # Entry point
# if __name__ == "__main__":

#     driver = initialize_driver()

#     try:
#         scrape_dynamic_table(driver)
 
#     except KeyboardInterrupt:
#         logging.info("Script interrupted by user.")
#     finally:
#         driver.quit()
#         logging.info("WebDriver closed.")
        