import requests
from bs4 import BeautifulSoup
import os
from pymongo import MongoClient
class Scraper:
    '''
    Class to encapsulate a scraper instance
    '''

    def __init__(self, pid:int, url:str, driver, user_agent, logger, routine: callable):
        self.__pid = pid
        if isinstance(url, list) or isinstance(url, tuple):
            self.__url = url[0]
        else:
            self.__url = url
        print(self.__url)
        self.__driver = driver
        self.__user_agent = user_agent
        self.__routine = routine
        self.logger = logger
        self.__links = set()
        self.__output = None

    def get_driver(self):
        return self.__driver
    
    def get_logger(self):
        return self.__logger
    
    def set_url(self, url:str):
        self.__url = url

    def get_links(self):
        return self.__links
    
    def get_pid(self):
        return self.__pid

    
    def get_soup_from_url(self):
        self.__driver.get(self.__url)
        html = self.__driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def start_scraping(self):
        '''
        Function to start the scraping process for a single scraper instance
        '''
        if self.can_scrape():
            self.logger.info(f"Url: {self.__url} is scrapeable")
            soup = self.get_soup_from_url()
            response = self.__routine(soup = soup, logger = self.logger,  url = self.__url)
            self.__output = response
            if response.get("status") == 'SUCCEED':
                self.__links = set(response.get('links'))
                
        else:
            self.logger.info(f"Skipping: {self.__url}")

        return self

    
    def save_output(self, database: str = 'zkraper_db', collection:str = 'scraper_logs'):
        '''
        Function to save the output of the scraper.
        If the folder exists, creates four subfolders in it.
        Otherwise, creates the folder and the subfolders.
    
        Args:
            output_path (str): The path where the main folder and subfolders will be created.
        '''
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        client = MongoClient(mongo_uri)

         # Access the database and create collections for each subpath
        db = client[database]  # Replace 'scraper_db' with your desired database name
        self.__output['scraper_id'] = self.get_pid()
        collection = db[collection]
        if isinstance(self.__output, list):
            
            collection.insert_many(self.__output)
        elif isinstance(self.__output, dict):
            collection.insert_one(self.__output)
        else:
            raise ValueError(f"Unsupported data format for {collection}: {type(self.__output)}")

        # Close the MongoDB connection
        client.close()

    def get_output(self):
        if self.__output is None:
            return False
        else:
            return True

            

    def can_scrape(self, minimum_content_length = 50, items_to_check = ['article', 'main', 'div', 'section']):
        '''
        Basic function to check if we can scrape a web.
        For now, to keep it simple, I check if I can make a basic request with the provided USER AGENT, 
        and if the retrieved content at least meets a minimum length

        '''
        try:
            
            response = requests.get(self.__url, headers={'User-Agent':self.__user_agent})
        
       
            if response.status_code != 200:
                self.logger.error(f"Error while trying to access url: {self.__url}")
                return False
        
            # Build the soup
            soup = BeautifulSoup(response.text, 'html.parser')
        
        
            principal = soup.get_text().strip()
        
        
            if len(principal) < minimum_content_length or not soup.find(items_to_check):
                self.logger.error("Not enough content for url: {}".format(str(self.__url)))
                return False
            

            return True
    
        except Exception as e:
            self.logger.error(f"Error while trying to access url: {self.__url}")

            return False
    
