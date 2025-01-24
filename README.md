# Zkraper

Zkraper is a Python-based web scraping tool that uses Selenium with Google Chrome in headless mode for automated browsing and data extraction. The project is designed to run inside a Docker container, ensuring an isolated and consistent environment.

# Key features:

* **Automated Web Scraping**: Uses Selenium with Google Chrome for automated interaction with web pages.

* **Headless Mode**: Chrome operates in headless mode, allowing the scraper to run without a visible browser UI, making it faster and less resource-intensive.

* **Docker & MongoDB Integration**: Encapsulated within a Docker container, ensuring consistency in dependencies and environment setup. The scraping service uses mongoDB to store its output in BSON format.

* **Customizable**: Configure the Chrome driver options through a JSON file to adapt to various scraping needs.

* **Concurrent Scraping**: Utilizes a threadpool to run multiple scrapers concurrently, allowing for faster data extraction.


# Project setup:

Ensure you have docker installed on your computer. After that, navigate to the project directory and execute:
```bash

docker compose up -d

```

To modify the **start_url** or the **max_scrapers** parameters, modify the environment variables in the docker-compose file.

Note that the first url you pass to the scraper must be a scrapeable url for the engine to start.

To see the output, connect to the mongo instance running in the mongo container created in the docker compose file.

```bash
docker exec -it mongo bash
```
Inside the container, open a mongo shell:

```bash
mongosh
```
Then, you can navigate to the scraper database and visualize its outputs:

```bash

show dbs;

use zkraper_db;

show collections;

db.scraper_logs.findOne();

```