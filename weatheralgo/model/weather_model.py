from fake_useragent import UserAgent
import logging

import time
import random

# from selenium import webdriver
from seleniumwire import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from weatheralgo import trade_functions
from weatheralgo import scrape_functions
from weatheralgo import util_functions


# Suppress logs from third-party libraries
logging.getLogger('seleniumwire').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.getLogger('webdriver_manager').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)
# Initialize Selenium WebDriver
def initialize_driver():
    proxy_url = util_functions.get_random_proxy()
    seleniumwire_options = {
        'proxy': {
            'http': proxy_url,
            'https': proxy_url,
            'no_proxy': 'localhost,127.0.0.1'  # Exclude local addresses
        }
    }

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-data")
    chrome_options.add_argument("--headless=")
    chrome_options.add_argument('--log-level=3')

    

    ua = UserAgent()
    chrome_options.add_argument(f"user-agent={ua.random}")

    
   

    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), 
        options=chrome_options,
        seleniumwire_options=seleniumwire_options
        )





# Main function to scrape and process data
def scrape_dynamic_table(driver, city, market, timezone, url, xml_url, lr_length, scraping_hours, 
                         minutes_from_max, count, yes_price, balance_min):
    

    util_functions.logging_settings()
    temperatures = []
    dates = []
    
    restart_threshold = 20  # Restart WebDriver every 40 iterations
    loop_counter = 0

    rand = random.randint(15, 30)
    expected_high = scrape_functions.xml_scrape(xml_url, timezone)[2]
    expected_hour = scrape_functions.xml_scrape(xml_url, timezone)[1]
    logging.info(f'Algo Loading in {city} expected high: {expected_high} and expected high hour {expected_hour}')

    while True:
        begin_scraping = scrape_functions.begin_scrape(timezone=timezone, scraping_hours=scraping_hours)
        trade_made_today = util_functions.trade_today(market=market, timezone=timezone)

        time.sleep(rand)
        try:

            if begin_scraping and not trade_made_today:
                
                scrape_temp = scrape_functions.scrape_temperature(driver=driver, url=url, timezone=timezone)
                current_date = scrape_temp[0]
                current_temp = scrape_temp[1]
            
                
                if len(dates) == 0 or (len(dates) > 0 and dates[-1] != current_date):
                    
                    dates.append(current_date)
                    temperatures.append(current_temp)
                    
                    logging.info(f"Date: {dates}")
                    logging.info(f"Date: {temperatures}")

                    #checks to see if currentc temp is at max of available markets then makes bet
                
                    current_temp_is_max = trade_functions.if_temp_reaches_max(current_temp=current_temp, 
                                                                              market = market, 
                                                                              yes_price=yes_price, 
                                                                              count=count,
                                                                              balance_min=balance_min)
                    if current_temp_is_max:
                        logging.info('Max Temperature Reached')
   
                    trade_criteria = trade_functions.trade_criteria_met(temperatures=temperatures, 
                                                                        lr_length=lr_length,
                                                                        timezone=timezone, 
                                                                        xml_url=xml_url,
                                                                        minutes_from_max= minutes_from_max,
                                                                        market=market)
                    if trade_criteria:
                        trade_execute = trade_functions.trade_execution(temperatures=temperatures,
                                                                        market=market,
                                                                        yes_price=yes_price,
                                                                        count=count, 
                                                                        balance_min=balance_min)
                        if trade_execute:
                            logging.info('Trade Criteria True')
                  
                
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
            
            # If it's a connection timeout, restart immediately
            if "Read timed out" in str(e) or "HTTPConnectionPool" in str(e):
                logging.info("Connection timeout detected, restarting WebDriver...")
                try:
                    driver.quit()
                except:
                    pass  # In case driver.quit() itself fails
                time.sleep(10)  # Give it time to fully close
                driver = initialize_driver()
                loop_counter = 0
            else:
                loop_counter += 1
                if loop_counter >= restart_threshold:
                    # Your existing restart code

            
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
        
