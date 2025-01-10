# main.py
#!/usr/bin/env python3

from src.scraper.engine import ZkraperEngine
import os


def main():
    
    

    base_url = os.getenv('BASE_URL', "https://www.marca.com")
    max_scrapers = os.getenv('MAX_SCRAPERS', 10)

    sk = ZkraperEngine(
        pid = 1000,
        starting_url= base_url,
        max_scrapers = int(max_scrapers)

    )
    sk.run()
   

if __name__ == '__main__':
    main()