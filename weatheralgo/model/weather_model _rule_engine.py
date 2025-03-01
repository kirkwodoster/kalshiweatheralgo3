from fake_useragent import UserAgent
import logging

import time
import random

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


class ScrapeInputs:
    def __init__(self, driver, city, market, timezone, url, xml_url, 
                 lr_length, scraping_hours, minutes_from_max, count,
                 yes_price, balance_min):
        # Configuration parameters
        self.driver = driver
        self.city = city
        self.market = market
        self.timezone = timezone
        self.url = url
        self.xml_url = xml_url
        self.lr_length = lr_length
        self.scraping_hours = scraping_hours  # Fixed typo: "scraping_hours" -> "scraping_hours"
        self.minutes_from_max = minutes_from_max
        self.count = count
        self.yes_price = yes_price
        self.balance_min = balance_min

      
        self.dates = []
        self.temperatures = []
        
        self.scrape_permission = scrape_functions.permission_to_scrape(
        market=self.market, 
        timezone=self.timezone, 
        scraping_hours=self.scraping_hours)
        
        self.scrape = scrape_functions.scrape_temperature(
            driver=self.driver,
            url=self.url,
            timezone=self.timezone
        )
        
        self.datetemp_append = scrape_functions.date_temp_append(
            driver=self.driver, 
            url=self.url, 
            timezone=self.timezone, 
            dates=self.dates)
        
        self.max_temp = trade_functions.if_temp_reaches_max(
            current_temp=self.current_temp, 
            market = self.market, 
            yes_price=self.yes_price, 
            count=self.count,
            balance_min=self.balance_min
        )
        
        self.trade_criteria = trade_functions.trade_criteria_met(
            temperatures=self.temperatures,
            lr_length=self.lr_length,
            timezone=self.timezone,
            xml_url=self.xml_url,
            minutes_from_max=self.minutes_from_max,
            market=self.market
            
        )
            
        self.trade_execute = trade_functions.trade_execution(
            market=self.market,
            temperatures=self.temperatrues,
            balance_min=self.balance_min,
            yes_price=self.yes_price,
            count=self.count
        )
   

    def handler(self):
        while True:
            time.sleep(1)
            if self.scrape_permission:        
                self.current_temp = self.datetemp_append[0]
                self.current_date = self.datetemp_append[1]
                self.dates.append(self.current_date)
                self.temperatures.append(self.current_date)
                
            if self.trade_criteria:
                self.trade_execute
                

                
        
        
    
# class Rule:
#     def __init__(self, condition, action):
#         self.condition = condition
#         self.action = action


# class RulesEngine:
#     def __init__(self, *rules):
#         self.rules = rules
        
#     def run(self, state):
        
#         for rule in self.rules:
#             if rule.condition(state):
#                 return rule.action(state)

    

        