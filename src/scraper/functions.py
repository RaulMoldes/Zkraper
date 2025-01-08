
from src.utils.scraping_utils import extract_all_links, extract_images, extract_meta_data, extract_all_text, extract_domain

'''
This module contains the routines that the scraper can execute.

All of them should return True if the scraping was successfully performed, or False otherwise.

Functions:

1. scrape_page_basic(soup, logger, url, domain, output_dir): Basic scraping. Extract all data from the soup and save it to files

'''

# Basic scraping function
def scrape_page_basic(soup, logger, url: str):

    '''
    Extract all data and save it to files
    '''
    try:

        # Extract all data
        domain = extract_domain(url=url)
        meta_data = extract_meta_data(soup)
        images = extract_images(soup, url)
        links = extract_all_links(soup, domain, url)
        text = extract_all_text(soup)
        # Save the extracted data
        logger.info(f"Successfully scraped {url}.")

        return {
            "status" : "SUCCEED",
            "domain": domain,
            "base_url": url,
            "meta": meta_data,
            "links": list(set(links)), ## REMOVE DUPLICATES
            "text": text


        }
    
    except Exception as e:

        logger.error(f"Error while scraping {url}: ", e)
        return {
            "status" : "ERROR",
            "base_url": url,
            "message": "Error while scraping url."
        }
        

