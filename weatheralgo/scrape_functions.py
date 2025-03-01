import logging
import numpy as np
import pandas as pd
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import requests
import xml.etree.ElementTree as ET
import time
from weatheralgo.clients import client



    
def scrape_temperature(driver, url, timezone) -> list[str]:
    
    try:
        driver.get(url)

        time.sleep(20)  # Wait for the page to load
        tbody = driver.find_element(By.XPATH, "//table[@id='OBS_DATA']/tbody")
        first_row = tbody.find_elements(By.TAG_NAME, "tr")[0]
        cells = first_row.find_elements(By.TAG_NAME, "td")
        
        current_denver_time = datetime.now(timezone)
        denver_strip = datetime.strftime(current_denver_time, "%A").split(',')
        denver_date = denver_strip[0]
    
        date_scrape = [cell.text.strip() for cell in cells][:2][0]

        date_scrape_format = datetime.strptime(date_scrape, '%b %d, %I:%M %p').strftime('%b %d, %I:%M %p')
    
        final_date = f'{denver_date}, {date_scrape_format},'

        path_element = driver.find_element(By.CSS_SELECTOR, f'path[aria-label*="{final_date}"]')
        aria_label = path_element.get_attribute('aria-label')
        temp = float(aria_label.split(' ')[5][:-1])
    

        return [date_scrape, temp]  # Return date and temperature
        
    except Exception as e:
        logging.error(f"Error scrape_temperature: {e}")
        return None



def xml_scrape(xml_url, timezone):

    try:
        response = requests.get(xml_url)
        root = ET.fromstring(response.content)

        start_times = root.findall('.//start-valid-time')
        dates = [time.text for time in start_times]

        temperature_element = root.find('.//temperature[@type="hourly"]')
        value_elements = temperature_element.findall('.//value')
        temp = [int(value.text) for value in value_elements if isinstance(value.text, str)]
        temp_length = len(temp)
 
        forecasted = pd.DataFrame({'DateTime': dates[:temp_length], 'Temperature': temp})
        forecasted['DateTime'] = pd.to_datetime(forecasted['DateTime'])
        forecasted = forecasted.sort_values(by='DateTime')

        denver_today = datetime.now(timezone).day

        next_day_high = forecasted[forecasted['DateTime'].dt.day == denver_today]['Temperature'].idxmax()
        date = forecasted['DateTime'].iloc[next_day_high]
        hour_of_high = forecasted['DateTime'].iloc[next_day_high].hour
        temp_high = forecasted['Temperature'].iloc[next_day_high]

        return [date, hour_of_high, temp_high]

    except Exception as e:
      print(e)


def trade_today(market, timezone):

    try:
        today = datetime.now(timezone)
        todaysDate = today.strftime('%y%b%d').upper()
        event = f'{market}-{todaysDate}'
        orders = client.get_orders(event_ticker=event)['orders']
        
        if len(orders) >= 1:
           
            return True
        else:
            return False

    except Exception as e:
        logging.error(f"Error Trade Today: {e}")

def begin_scrape(scraping_hours, expected_high_date, timezone):
    
    try:
        today = datetime.now(timezone)
        start_scrape = today >= expected_high_date - timedelta(minutes=scraping_hours[0])
        end_scrape = today <= expected_high_date + timedelta(minutes=scraping_hours[1])


        if start_scrape and end_scrape:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Error in begin_scrape: {e}")

def permission_to_scrape(market, timezone, scraping_hours, expected_high_date):
    
    if not trade_today(market, timezone) and begin_scrape(scraping_hours, expected_high_date, timezone):
        return True
    else:
        return False
    
        
def date_temp_append(driver, url, timezone, dates):
    try:
        scrape_data = scrape_temperature(driver=driver, url=url, timezone=timezone)
        current_date = scrape_data[0]
        current_temp = scrape_data[1]
        if len(dates) == 0 or (len(dates) > 0 and dates[-1] != current_date):
            return [current_date, current_temp]
        else:
            return False
    except Exception as e:
        logging.error(f"Error in date_temp_append: {e}")
    
    