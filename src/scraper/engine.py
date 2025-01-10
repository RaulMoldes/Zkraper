from src.scraper.driver import start_driver, quit_driver
from src.scraper.scraper import Scraper
from src.scraper.functions import scrape_page_basic
from queue import Queue
import logging
import logging.config
import yaml
from concurrent.futures import as_completed, ThreadPoolExecutor
from functools import partial



USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

def scrape(scraper: Scraper):
    '''
    Wrapper for the start_scraping function of the Scraper instance
    '''
    return scraper.start_scraping()
class ZkraperEngine:
    """
    ZkraperEngine class manages the scraping process by initializing and running multiple scrapers.
    It spawns scrapers concurrently, manages visited URLs, and logs the process.
    """

    def __init__(self,
                 pid: int, 
                 starting_url:str, 
                 max_scrapers: int = None, 
                 config_file: str = './configs/scraper_config.json',
                 log_config_file: str = './configs/log.yaml',
                 log_file: str = './log/scraper.log'):
        
        """
        Initialize the ZkraperEngine instance.

        Arguments:
        - pid: int - The PID of the zkraper engine.
        - starting_url: str - The URL where the scraping process starts.
        - max_scrapers: int - The maximum number of concurrent scrapers to run.
        - config_file: str - Path to the scraper's configuration file (default is '../configs/scraper_config.json').
        - log_config_file: str - Path to the logging configuration file (default is '../configs/log.yaml').
        """
        self.__pid = pid
        self.__start_url = starting_url
        self.__driver = start_driver(driver_options_path= config_file)
        if max_scrapers is not None:
            self.__max_scrapers = max_scrapers
        else:
            self.__max_scrapers = 10
        self.queue = Queue() ## Initialize the queue which will be shared by all scrapers
        self.visited_links = set() ## Maintain info about the urls that are already visited.
        
        self.__logger =  self.__config_log(log_config_file)
        self.__log_file = log_file
        self.next_pid = pid + 1

    def get_pid(self):
        return self.__pid


    def __config_log(self, log_config_file: str, logger_name: str = 'scraper'):
        """
        Configures logging using a YAML configuration file.

        Arguments:
        - log_config_file: str - The path to the log configuration file.
        - logger_name: str - The logger's name (default is 'scraper').

        Returns:
        - logger: logging.Logger - A logger instance for use in the class.
        """
        with open(log_config_file, 'r') as log_file:
            config = yaml.safe_load(log_file.read())
            logging.config.dictConfig(config)
        
        logger = logging.getLogger(logger_name)

        return logger
    
    def quit(self):
        """
        Clean up the scraper engine by clearing the queue, visited links, and quitting the driver.
        """
        self.queue = Queue()
        self.visited_links = set()
        quit_driver(self.__driver)
        ## TRUNCATE THE LOG FILE
        
        with open(self.__log_file, 'w'):
            pass  # Opening the file in write mode clears its contents


    def run(self):
        """
        Starts the ZkraperEngine. This method begins scraping by managing multiple scrapers concurrently.
        Each scraper works on a URL from the queue and updates the visited links set.
        """
        self.__logger.info("Starting Zkraper Engine!")
        self.queue.put(self.__start_url)
        
        with ThreadPoolExecutor(max_workers=self.__max_scrapers) as executor:
            futures = list()

            while not self.queue.empty() or any([future.running() for future in futures]):
                if len(futures) < self.__max_scrapers and not self.queue.empty():
                    # Get the next URL from the queue
                    next_url = self.queue.get()

                    if next_url not in self.visited_links:
                        pid = self.next_pid
                        ### SPAWNS A NEW SCRAPER
                        scraper = Scraper(pid = pid, url = next_url, driver = self.__driver, 
                                      user_agent = USER_AGENT, logger = self.__logger, routine = scrape_page_basic)
                        
                        self.next_pid = pid + 1
                        future = executor.submit(scrape, scraper= scraper)
                        futures.append(future)

                # Clean up completed futures
                for future in as_completed(futures):
                    futures.remove(future)
                    scraper = future.result() 
                    links = scraper.get_links()  

                    ## Update the visited links
                    for l in list(links):
                        self.queue.put(l)
                        self.visited_links.update(l)
                    
                  
                    if scraper.get_output():
                        scraper.save_output()

        self.quit()