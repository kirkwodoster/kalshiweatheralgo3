import logging
import numpy as np
import pandas as pd
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import requests
import xml.etree.ElementTree as ET
import time
from weatheralgo.clients import client
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

    
def scrape_temperature(driver, url) -> list[str, float]:
    
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'path[fill="#2caffe"]'))
        )
        path_elements = driver.find_elements(By.CSS_SELECTOR, 'path[fill="#2caffe"]')

        datetemp_list = [path.get_attribute("aria-label") for path in path_elements]
       
        date = [', '.join(i.split(', ')[0:3]) for i in datetemp_list]
        temp = [float(i.split(', ')[-1].split(' ')[0][:-1]) for i in datetemp_list]
    
        return [date, temp]  # Return date and temperature
        
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
    
        

    