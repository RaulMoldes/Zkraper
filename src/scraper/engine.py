from src.scraper.driver import start_driver, quit_driver
from src.scraper.scraper import Scraper
from src.scraper.functions import scrape_page_basic
from queue import Queue
import logging
import logging.config
import yaml
from concurrent.futures import as_completed, ThreadPoolExecutor as executor




USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
class ZkraperEngine:
    """
    ZkraperEngine class manages the scraping process by initializing and running multiple scrapers.
    It spawns scrapers concurrently, manages visited URLs, and logs the process.
    """

    def __init__(self, 
                 starting_url:str, 
                 max_scrapers: int, 
                 config_file: str = './configs/scraper_config.json',
                 log_config_file: str = './configs/log.yaml'):
        
        """
        Initialize the ZkraperEngine instance.

        Arguments:
        - starting_url: str - The URL where the scraping process starts.
        - max_scrapers: int - The maximum number of concurrent scrapers to run.
        - config_file: str - Path to the scraper's configuration file (default is '../configs/scraper_config.json').
        - log_config_file: str - Path to the logging configuration file (default is '../configs/log.yaml').
        """
        
        self.__start_url = starting_url

        self.__driver = start_driver(driver_options_path= config_file)
        self.__max_scrapers = max_scrapers
        self.queue = Queue() ## Initialize the queue which will be shared by all scrapers
        self.visited_links = set() ## Maintain info about the urls that are already visited.
        self.__logger =  self.__config_log(log_config_file)
        


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

    def run(self):
        """
        Starts the ZkraperEngine. This method begins scraping by managing multiple scrapers concurrently.
        Each scraper works on a URL from the queue and updates the visited links set.
        """
        self.__logger.info("Starting Zkraper Engine!")
        self.queue.put(self.__start_url)
        with executor(max_workers=self.__max_scrapers):
            futures = list()

            while not self.queue.empty() or any([future.running() for future in futures]):
                if len(futures) < self.__max_scrapers and not self.queue.empty():
                    # Get the next URL from the queue
                    next_url = self.queue.get()

                    if next_url not in self.visited_links:
                        ### SPAWNS A NEW SCRAPER
                        scraper = Scraper(url = next_url, driver = self.__driver, 
                                      user_agent = USER_AGENT, logger = self.__logger, routine = scrape_page_basic)
                    
                        executor.submit(scraper.start_scraping())

                # Clean up completed futures
                for future in as_completed(futures):
                    futures.remove(future)
                    scraper = future.result() 
                    links = scraper.get_links()  
                    ## Update the visited links
                    self.queue.put(links)
                    self.visited_links.update(links)

        self.quit()