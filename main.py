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
    

    input = Input()
    input.user_input_function()

    dict_input = input.user_dict_output()

    driver =  weather_model.initialize_driver()
    util_functions.logging_settings()
    try:
       weather_model.scrape_dynamic_table(driver, **dict_input)
    except KeyboardInterrupt:
        logging.info("Script interrupted by user.")
    finally:
        driver.quit()
        logging.info("WebDriver closed.")


