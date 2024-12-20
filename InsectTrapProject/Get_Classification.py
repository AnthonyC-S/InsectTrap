from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os


# Set iNaturalist username and password in order to login
USERNAME = ""
PASSWORD = ""


def initialize_driver(auto):

    # Set up the WebDriver, will need to adjust to run in headless.
    chrome_options = Options()

    chrome_options.binary_location = "/usr/bin/chromium-browser"
    #chrome_options.add_argument("--headless=new") # for Chrome >= 109
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("enable-automation")
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--dns-prefetch-disable")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.page_load_strategy = 'normal'


    driver_path = "/usr/bin/chromedriver"
    service_path = Service(driver_path)
    driver = webdriver.Chrome(service=service_path, options=chrome_options)
    

    # Navigate to the iNaturalist login page
    driver.get("https://www.inaturalist.org/login")

    # Find and fill in the username/email field
    username_field = WebDriverWait(driver, 4).until(  
        EC.presence_of_element_located((By.ID, "user_email"))
    )
    username_field.send_keys(USERNAME)

    # Find and fill in the password field
    password_field = driver.find_element(By.ID, "user_password")
    password_field.send_keys(PASSWORD)

    # Find and click the login button
    login_button = driver.find_element(By.NAME, "commit")
    login_button.click()
    # Wait for the login process to complete
    time.sleep(1)

    # Verify if login was successful
    if not auto:
        if "iNaturalist" in driver.title:
            print("Login successful!")
        else:
            print("Login failed or unexpected page loaded.")

    # Navigate to the iNaturalist Upload website
    driver.get("https://www.inaturalist.org/observations/upload")

    # Wait for the page to load
    time.sleep(1)

    return driver


def get_ID(image_filename, driver, auto):
    results = {}

    # Locate the file input element and send the file path to it
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    photo_path = os.path.abspath(image_filename)
    file_input.send_keys(photo_path)

    time.sleep(1)  

    # Wait for suggestions to load
    taxon_field = WebDriverWait(driver, 2).until(   #5 -> 2 waittime
        EC.presence_of_element_located((By.NAME, "taxon_name"))
    )

    # Click the field to get CV classification recommendation
    taxon_field.click()

    time.sleep(3) 

    # Extract most likely genus
    taxon_most_likely = WebDriverWait(driver, 2).until(  
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.ui-autocomplete li.category:nth-child(1) + li"))
    )

    taxon_most_likely_common_name = taxon_most_likely.find_element(By.CSS_SELECTOR, ".title").text
    taxon_most_likely_scientific_name = taxon_most_likely.find_element(By.CSS_SELECTOR, ".subtitle").text
    if ' ' not in taxon_most_likely_scientific_name:
        taxon_most_likely_scientific_name = taxon_most_likely.find_element(By.CSS_SELECTOR, ".subtitle").text + ' ' + taxon_most_likely_common_name

    try:
    # Extract top suggestion species
        top_suggestion = WebDriverWait(driver, 3).until(  
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.ui-autocomplete li.category:nth-child(3) + li"))
        )

        top_suggestion_common_name = top_suggestion.find_element(By.CSS_SELECTOR, ".title").text
        top_suggestion_species_name = top_suggestion.find_element(By.CSS_SELECTOR, ".subtitle").text
        if ' ' not in top_suggestion_species_name:
            top_suggestion_species_name = top_suggestion.find_element(By.CSS_SELECTOR, ".subtitle").text + ' ' + top_suggestion_common_name

    except TimeoutException:
        top_suggestion_common_name = taxon_most_likely_common_name
        top_suggestion_species_name = taxon_most_likely_scientific_name
        taxon_most_likely_common_name = 'Not Found'
        taxon_most_likely_scientific_name = 'Not Found'

    results = {
        "taxon_most_likely_common_name": taxon_most_likely_common_name,
        "taxon_most_likely_scientific_name": taxon_most_likely_scientific_name,
        'top_suggestion_common_name': top_suggestion_common_name,
        'top_suggestion_species_name': top_suggestion_species_name
        }


    # Navigate back to the upload page for the next image
    driver.get("https://www.inaturalist.org/observations/upload")
    if not auto:
        if len(results) > 0:
            print("Image processed. Results:")
            print(f"Image: {image_filename}")
            print(f"  taxon_most_likely_common_name: {results['taxon_most_likely_common_name']}")
            print(f"  taxon_most_likely_scientific_name: {results['taxon_most_likely_scientific_name']}")
            print(f"  top_suggestion_common_name: {results['top_suggestion_common_name']}")
            print(f"  top_suggestion_species_name: {results['top_suggestion_species_name']}")
            print()
        else:
            print("No image files found in the specified folder.")
    return driver, results

def quit_driver(driver):
    # Close the browser
    driver.quit()
