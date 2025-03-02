#from cryptography.hazmat.primitives import serialization
#import asyncio
# from weatheralgo.clients import  KalshiWebSocketClient
import logging
import pytz
from weatheralgo.model import weather_model
from weatheralgo import util_functions
from weatheralgo import scrape_functions
from weatheralgo import trade_functions
from weatheralgo.input_variables import Input
from weatheralgo.clients import client
from datetime import datetime, timedelta
import pytz
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from weatheralgo.clients import client



# Initialize the WebSocket client
# ws_client = KalshiWebSocketClient(
#     key_id=client.key_id,
#     private_key=client.private_key,
#     environment=client.environment
# )

# Connect via WebSocket
# asyncio.run(ws_client.connect())

if __name__ == "__main__":
    
    xml_url = "https://forecast.weather.gov/MapClick.php?lat=41.7842&lon=-87.7553&FcstType=digitalDWML"
    timezone =  pytz.timezone("America/Chicago")
    expected_high_date = scrape_functions.xml_scrape(xml_url, timezone)[0]
    my_dict = {'current_temp': 24.8, 'market': 'KXHIGHCHI', 'yes_price': 1, 'count': 1, 'balance_min': 100, 'temperatures': [40, 26.6, 26.6, 26.06, 26.6, 26.6, 26.6, 26.6, 26.6, 26.6, 26.6, 26.6, 26.6, 26.6, 26.6, 26.6, 26.06, 26.6, 26.6, 24.8, 26.6, 24.8, 26.6, 26.6, 26.6, 26.6, 26.6, 26.6, 24.8, 24.98, 24.8, 24.8, 24.8, 24.8, 24.8, 24.8, 24.8, 24.8, 24.8], 'lr_length': 5, 'timezone': 'America/Chicago', 'expected_high_date': expected_high_date, 'minutes_from_max': 15}

    x = trade_functions.trade_criteria_met(temperatures=my_dict['temperatures'], lr_length=5, timezone=pytz.timezone("America/Chicago"),expected_high_date=expected_high_date, 
                                           market='KXHIGHCHI', minutes_from_max=1000, balance_min=100, yes_price=1, count=1)
    
    print(expected_high_date)
    # input = Input()
    # input.user_input_function()

    # dict_input = input.user_dict_output()

    # driver =  weather_model.initialize_driver()
    # util_functions.logging_settings()
    # try:
    #    weather_model.scrape_dynamic_table(driver, **dict_input)
    # except KeyboardInterrupt:
    #     logging.info("Script interrupted by user.")
    # finally:
    #     driver.quit()
    #     logging.info("WebDriver closed.")


