import os
import json
import time
import re
from selenium import webdriver  # Usar selenium-wire en lugar de selenium
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


def start_driver(driver_options_path: str):
    # Load driver configuration from the JSON file
    with open(driver_options_path, 'r') as file:
        driver_config = json.load(file)

   
    # Use webdrivermanager to install ChromeDriver if needed
    chrome_driver_path = ChromeDriverManager().install()

    # Set up Chrome options
    options = ChromeOptions()

    # Add Chrome options dynamically from the JSON configuration
    if 'user_agent' in driver_config:
        options.add_argument(f"user-agent={driver_config['user_agent']}")

    if driver_config.get("headless", False):
        options.add_argument("--headless")

    if driver_config.get("no_sandbox", False):
        options.add_argument("--no-sandbox")

    if driver_config.get("disable_dev_shm_usage", False):
        options.add_argument("--disable-dev-shm-usage")

    if driver_config.get("disable_web_security", False):
        options.add_argument("--disable-web-security")

    if driver_config.get("disable_notifications", False):
        options.add_argument("--disable-notifications")

    if driver_config.get("disable_extensions", False):
        options.add_argument("--disable-extensions")
    else:
        extensions = driver_config.get("extensions", [])
        if len(extensions) > 0:
            for ext in extensions:
                options.add_argument(f"--load-extension={os.path.abspath(ext)}")

    if driver_config.get("ignore_certificate_errors", False):
        options.add_argument("--ignore-certificate-errors")
        
    if driver_config.get("disable_translate", False):
        options.add_argument("--disable-features=Translate")
        
    if driver_config.get("password_store", None):
        options.add_argument(f"--password-store={driver_config['password_store']}")

    if driver_config.get("allow_running_insecure_content", False):
        options.add_argument("--allow-running-insecure-content")

    if driver_config.get("no_default_browser_check", False):
        options.add_argument("--no-default-browser-check")

    if driver_config.get("no_first_run", False):
        options.add_argument("--no-first-run")

    if 'log_level' in driver_config:
        options.add_argument(f"--log-level={driver_config['log_level']}")

    if driver_config.get("no_proxy_server", False):
        options.add_argument("--no-proxy-server")

    if 'no_blink_features' in driver_config:
        options.add_argument(f"--no-blink-features={driver_config['no_blink_features']}")

    if driver_config.get("enable_javascript", False):
        options.add_argument("--enable-javascript")

    if driver_config.get("experimental_options", {}) != {}:
        options.add_experimental_option(
                "prefs",
                driver_config["experimental_option"]
            )

    # Initialize Chrome WebDriver with the service and options
    serv = ChromeService(chrome_driver_path)
    driver = webdriver.Chrome(service=serv, options=options)


    return driver

def quit_driver(driver):
    driver.quit()
    return True


