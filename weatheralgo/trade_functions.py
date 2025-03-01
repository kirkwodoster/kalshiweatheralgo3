#from nws_scrape_2nd import check_ema_downtrend
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import logging
import uuid

from weatheralgo.clients import client
from weatheralgo import util_functions
from weatheralgo import scrape_functions


def trade_execution(market: str, temperatures: list, balance_min: int,  yes_price: int, count: int):
    try:
        highest_temp = np.array(temperatures).max()
        highest_temp = int(highest_temp)
        market_ticker = util_functions.order_pipeline(highest_temp=highest_temp, market=market)

        balance = client.get_balance()['balance'] > balance_min
        if balance:          
            logging.info('order_pipeline worked')
            order_id = str(uuid.uuid4())
            client.create_order(ticker=market_ticker, client_order_id=order_id,  yes_price=yes_price, count=count)
            logging.info(f'Order Submitted {market_ticker}')
          
            return True
        else:
            return False
    
    except Exception as e:
        logging.info(f'trade_execution : {e}')
    
def if_temp_reaches_max(current_temp: int, market: str, yes_price: int, count: int, balance_min: int):
    try:
        market_temp_max = list(util_functions.weather_config(market).items())[-1][1]
        balance = client.get_balance()['balance'] > balance_min
        if current_temp >= market_temp_max and balance:
            market_ticker = util_functions.order_pipeline(highest_temp=current_temp, market=market)
            order_id = str(uuid.uuid4())
            client.create_order(ticker=market_ticker,client_order_id=order_id,count=count,yes_price=yes_price)
            logging.info(f"Max temp reached and order created {current_temp}")
         
            return True
        else:
            False
    except Exception as e:
        logging.info(f'if_temp_reaches_max : {e}')
    
    
def trade_criteria_met(temperatures: list, lr_length: int, timezone, xml_url: str, minutes_from_max: int, market: str):
    
    try:
        current_time = datetime.now(timezone)
        minute_max_temp = scrape_functions.xml_scrape(xml_url, timezone)[0]

        #trade_range = (current_time >= hour_max_temp - minutes_from_max) and (current_time <= hour_max_temp + minutes_from_max)
        trade_range = (current_time >= minute_max_temp - timedelta(minutes=minutes_from_max)) and \
                      (current_time <= minute_max_temp + timedelta(minutes=minutes_from_max))
        
        length = len(temperatures) >= lr_length
        
        highest_temp = np.array(temperatures).max()
        order_pipeline_check = util_functions.order_pipeline(highest_temp=highest_temp, market=market)

        if trade_range and length and order_pipeline_check:
            x = np.arange(0, lr_length).reshape(-1,1)
            temp_length = temperatures[-lr_length:]
            regressor = LinearRegression().fit(x, temp_length)
            slope = regressor.coef_
            if slope <= 0:
                logging.info(f"Slope: {slope}")
                logging.info(f"X: {temp_length}")
                logging.info(f"Max Temp: {highest_temp}")
                return True
            else:
                False
    except Exception as e:
        logging.error(f"Error in trade_criteria_met: {e}")
        
    