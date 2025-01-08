# main.py
#!/usr/bin/env python3

from src.scraper.engine import ZkraperEngine
import argparse



def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Web scraping script.")
    
  
    
  
    parser.add_argument(
        "--base-url", 
        type=str, 
        required=True, 
        help="Base URL of the website to scrape."
    )
    parser.add_argument(
        "--max-scrapers", 
        type=int, 
        required=False, 
        help="Maximum number of concurrent scrapers."
    )
    args = parser.parse_args()


    sk = ZkraperEngine(
        pid = 1000,
        starting_url= args.base_url,
        max_scrapers = args.max_scrapers

    )
   

if __name__ == '__main__':
    main()