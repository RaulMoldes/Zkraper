import requests
from bs4 import BeautifulSoup
from queue import Queue

class Scraper:
    '''
    Class to encapsulate a scraper instance
    '''

    def __init__(self, url, driver, user_agent, logger, routine: callable):
        self.__url = url
        self.__driver = driver
        self.__user_agent = user_agent
        self.__routine = routine
        self.logger = logger
        self.__links = set()

    def get_driver(self):
        return self.__driver
    
    def get_logger(self):
        return self.__logger
    
    def set_url(self, url:str):
        self.__url = url

    def get_links(self):
        return self.__links
    
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
            if response.get("status") == 'SUCCEED':
                self.__links = set(response.get('links'))
        else:
            self.logger.info(f"Skipping: {self.__url}")

        return self

    
    
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
    
