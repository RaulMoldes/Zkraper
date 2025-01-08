import requests
from bs4 import BeautifulSoup
import os
import pickle
class Scraper:
    '''
    Class to encapsulate a scraper instance
    '''

    def __init__(self, pid:int, url:str, driver, user_agent, logger, routine: callable):
        self.__pid = id
        self.__url = url
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

    
    def save_output(self, output_path: str):
        '''
        Function to save the output of the scraper.
        If the folder exists, creates four subfolders in it.
        Otherwise, creates the folder and the subfolders.
    
        Args:
            output_path (str): The path where the main folder and subfolders will be created.
        '''
        if not os.path.exists(output_path):
            # If the folder does not exist, create it along with subfolders
            os.makedirs(output_path)  # Create the main folder

        for subpath in ['images', 'text', 'links', 'meta']:
            if not os.path.exists(os.path.join(output_path, subpath)):
                os.makedirs(os.path.join(output_path, subpath))

            if self.__output is not None:
                data = self.__output.get(subpath)
                
                with open(os.path.join(output_path, subpath), 'wb'):
                    pickle.dump(data)
            

    def can_scrape(self, minimum_content_length = 50, items_to_check = ['article', 'main', 'div', 'section']):
        '''
        Basic function to check if we can scrape a web.
        For now, to keep it simple, I check if I can make a basic request with the provided USER AGENT, 
        and if the retrieved content at least meets a minimum length

        '''
        try:
            
            response = requests.get(self.__url, headers={'User-Agent':self.__user_agent})
        
       
            if response.status_code != 200:
                self.logger.error("Error while trying to access url: {}".format(str(e)))
                return False
        
            # Build the soup
            soup = BeautifulSoup(response.text, 'html.parser')
        
        
            principal = soup.get_text().strip()
        
        
            if len(principal) < minimum_content_length or not soup.find(items_to_check):
                self.logger.error("Not enough content for url: {}".format(str(e)))
                return False
            

            return True
    
        except requests.RequestException as e:
            self.logger.error("Error while trying to access url: {}".format(str(e)))

            return False, "Error al intentar acceder a la URL: {}".format(str(e))
    
