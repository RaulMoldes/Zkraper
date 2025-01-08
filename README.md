# Zkraper

Zkraper is a Python-based web scraping tool that uses Selenium with Google Chrome in headless mode for automated browsing and data extraction. The project is designed to run inside a Docker container, ensuring an isolated and consistent environment.

# Key features:
* **Automated Web Scraping**: Uses Selenium with Google Chrome for automated interaction with web pages.
* **Headless Mode**: Chrome operates in headless mode, allowing the scraper to run without a visible browser UI, making it faster and less resource-intensive.
* **Docker Integration**: Encapsulated within a Docker container, ensuring consistency in dependencies and environment setup.
* **Customizable**: Configure the Chrome driver options through a JSON file to adapt to various scraping needs.
* **Output Flexibility**: Saves scraped data to a user-specified output directory.
* **Concurrent Scraping**: Utilizes multithreading to run multiple scrapers concurrently, allowing for faster data extraction.


# Project setup:

1. **Build the image**
To create the Docker image for Zkraper, use the following command:
`docker build -t zkraper:V0 .`
This command will create an image named zkraper with the tag V0.

2 **Run the container**
To run the scraper within a Docker container, use this command:
`docker run -it -v "%cd%":/app --rm zkraper:V0`
Explanation:

- `-it`: Runs the container in interactive mode with a pseudo-TTY.
- `-v "%cd%":/app`: Mounts the current directory (%cd% for Windows, use $(pwd) for Unix-like systems) to the /app directory inside the container. This allows access to your local files from inside the container.
- `--rm`: Removes the container after it stops running.
- `zkraper:V0`: Specifies the Docker image to run.

# Usage
## Command Line Arguments
The main.py script requires several command-line arguments to control the scraping behavior. Below is a breakdown of the options:

* `--base_url`: (Required) The base URL of the website you want to scrape.
* `--max-scrapers`: (Optional) The maximum number of concurrent scrapers to run. Default is 10.

## Example:
 - `python -m main --base-url "https://www.marca.com" --max-scrapers 10`
