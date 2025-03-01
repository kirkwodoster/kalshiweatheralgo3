
import pytz


class Input:

    def __init__(self):
        self.all_markets = {
            "DENVER": {
                "SERIES": "KXHIGHDEN",
                "TIMEZONE": "America/Denver",
                "URL": "https://www.weather.gov/wrh/timeseries?site=KDEN&hours=3",
                "XML_URL": "https://forecast.weather.gov/MapClick.php?lat=39.8589&lon=-104.6733&FcstType=digitalDWML",
            },
            "CHICAGO": {
                "SERIES": "KXHIGHCHI",
                "TIMEZONE": "America/Chicago",
                "URL": "https://www.weather.gov/wrh/timeseries?site=KMDW&hours=3",
                "XML_URL": "https://forecast.weather.gov/MapClick.php?lat=41.7842&lon=-87.7553&FcstType=digitalDWML",
            },
            "MIAMI": {
                "SERIES": "KXHIGHMIA",
                "TIMEZONE": "US/Eastern",
                "URL": "https://www.weather.gov/wrh/timeseries?site=KMIA&hours=3",
                "XML_URL": "https://forecast.weather.gov/MapClick.php?lat=25.7934&lon=-80.2901&FcstType=digitalDWML",
            },
            "AUSTIN": {
                "SERIES": "KXHIGHAUS",
                "TIMEZONE": "US/Central",
                "URL": "https://www.weather.gov/wrh/timeseries?site=KAUS&hours=3",
                "XML_URL": "https://forecast.weather.gov/MapClick.php?lat=30.1945&lon=-97.6699&FcstType=digitalDWML",
            },
            "PHILADELPHIA": {
                "SERIES": "KXHIGHPHIL",
                "TIMEZONE": "US/Eastern",
                "URL": "https://www.weather.gov/wrh/timeseries?site=KPHL&hours=3",
                "XML_URL": "https://forecast.weather.gov/MapClick.php?lat=39.8721&lon=-75.2407&FcstType=digitalDWML",
            },
            "LOS ANGELES": {
                "SERIES": "KXHIGHLAX",
                "TIMEZONE": "America/Los_Angeles",
                "URL": "https://www.weather.gov/wrh/timeseries?site=KLAX&hours=3",
                "XML_URL": "https://forecast.weather.gov/MapClick.php?lat=33.9425&lon=-118.409&FcstType=digitalDWML",
            }
        }

        self.city = None  # Initialize city
        self.LR_LENGTH = 5
        self.SCRAPING_HOURS = (120,60)
        self.MINUTES_FROM_MAX = 15
        self.COUNT = 1
        self.YES_PRICE = 85
        self.BALANCE_MIN = 100

    def user_input_function(self):
        
        
        while True:
            self.city = input("City (DENVER, CHICAGO, MIAMI, AUSTIN, PHILADELPHIA, LOS ANGELES): ").upper() # .upper() for case-insensitivity
            if self.city in self.all_markets:  # Validate city input
                print(f"Selected City: {self.city}")
                self.market = self.all_markets[self.city]
                break # Exit loop if city is valid
            else:
                print("Invalid city. Please choose from the list.") 

        while True:
            default = input("Default [Y] or [n]: ")
            if default == 'n':
                       
                while True:  # Loop for lr_length input
                    try:
                        self.LR_LENGTH = int(input("Linear Regression Length: "))
                        # print(f"LR Length: {self.LR_LENGTH}")
                        break  # Exit loop if input is valid
                    except ValueError:
                        print("Invalid input. Please enter an integer.")

                while True: # Loop for scraping_hours input
                    try:
                        self.SCRAPING_HOURS_STR = input("Scraping minutes from high of day hour eg. (120, 60): ") #Get string input first
                        self.SCRAPING_HOURS = tuple(map(int, self.SCRAPING_HOURS_STR.split(",")))
                        #Split and convert to tuple of ints
                        # print(f"Scraping Hours: {self.SCRAPING_HOURS}")
                        break
                    except ValueError:
                        print("Invalid input. Please enter comma-separated integers.")
                
                
                while True: # Loop for trade_execution_hours input
                    try:
                        self.MINUTES_FROM_MAX = int(input("MINUTES FROM MAX PREDICTED TEMPERATURE : "))
                        # print(f"HOURS FROM EXPECTED MAX TEMPERATURE: {self.MINUTES_FROM_MAX}")
                        break
                    except ValueError:
                        print("Invalid input. Please enter an integer.")
                while True:
                    try:
                        self.COUNT = int(input("Contract Size: "))
                        # print(f"Contract Size: {self.COUNT}")
                        break
                    except ValueError:
                        print("Invalid input. Please enter an integer.")
                while True:
                    try:
                        self.YES_PRICE = int(input("Limit Order: "))
                        # print(f"Limit Order: {self.YES_PRICE}")
                        break
                    except ValueError:
                        print("Invalid input. Please enter an integer.")
                while True:
                    try:
                        self.BALANCE_MIN = int(input("Minimum Balance for Trade: "))
                        # print(f"Minimum Balance for Trade: ")
                        break
                    except ValueError:
                        print("Invalid input. Please enter an integer.")
                break

            elif default == 'Y':
                break
            
            else:
                print("Invalid input. Please enter 'Y' or 'n'.")
          
            

    
    def user_dict_output(self):
        

        output = { 
            # 'city': self.city,
            'market': self.market['SERIES'],
            'timezone':  pytz.timezone(self.market['TIMEZONE']),
            'url': self.market['URL'],
            'xml_url': self.market['XML_URL'],
            'lr_length': self.LR_LENGTH,
            'scraping_hours': self.SCRAPING_HOURS,
            'minutes_from_max': self.MINUTES_FROM_MAX,
            'count': self.COUNT,
            'yes_price': self.YES_PRICE,
            'balance_min': self.BALANCE_MIN
            }
        
        return output





