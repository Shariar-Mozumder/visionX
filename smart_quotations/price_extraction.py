import time
from googlesearch import search
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image
import pytesseract
import tempfile
import requests
from io import BytesIO
from requests.exceptions import HTTPError

# Set up Selenium with headless Chrome
def init_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service('C:/Users/Lenovo/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe')  # Replace with your chromedriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to get the top 5 product links from Google search
# def get_product_links(query, num_results=5):
#     query = f'"{query}" site:google.com'  # Adjust the query to search for products
#     links = []
#     for result in search(query, num_results=num_results):
#         if "amazon" in result or "ebay" in result or "flipkart" in result:
#             links.append(result)
#     return links
def get_product_links(query, num_results=5, retries=3, delay=5):
    """
    Get top e-commerce links for a product using Google Search, with delay and retries.
    
    Args:
        query (str): The search query.
        num_results (int): Number of results to fetch.
        retries (int): Number of retries in case of HTTP errors.
        delay (int): Delay in seconds between retries.
    
    Returns:
        list: List of product links matching e-commerce sites.
    """
    links = []
    attempts = 0

    while attempts < retries:
        try:
            print(f"Attempt {attempts + 1}: Searching for '{query}'")
            for result in search(query, num_results=num_results):
                # if "amazon" in result or "ebay" in result or "flipkart" in result:
                links.append(result)
                # Delay between individual search results
                time.sleep(2)  # 2 seconds between results to avoid being flagged

            if links:
                return links  # Return links if successfully fetched
            else:
                print("No relevant links found. Retrying...")
        except HTTPError as e:
            if e.response.status_code == 429:  # Too Many Requests
                print(f"Too many requests. Retrying in {delay} seconds...")
                time.sleep(delay)
                attempts += 1
            else:
                print(f"An HTTP error occurred: {e}")
                raise e  # Re-raise error if it's not a 429
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise e  # Handle other exceptions

    raise Exception("Failed to fetch results after multiple retries.")

# Capture screenshot from a webpage using Selenium
def capture_screenshot(url, driver):
    driver.get(url)
    time.sleep(3)  # Wait for page to load completely
    screenshot = driver.get_screenshot_as_png()  # Take screenshot as PNG
    image = Image.open(BytesIO(screenshot))  # Convert PNG to image
    return image

# Extract product details (price, name) using Tesseract OCR
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

# Main function that integrates everything
def cross_validate_prices(product_name):
    driver = init_selenium()
    
    # Get the top 5 product links
    product_links = get_product_links(product_name)
    
    # Save product details
    product_details = []

    for link in product_links:
        print(f"Processing: {link}")
        try:
            # Capture screenshot of the product page
            screenshot = capture_screenshot(link, driver)
            
            # Extract text from the screenshot using OCR
            text = extract_text_from_image(screenshot)
            
            # Store the product link and extracted text
            product_details.append({
                'link': link,
                'text': text
            })
        except Exception as e:
            print(f"Error processing {link}: {e}")
    
    driver.quit()  # Quit the Selenium driver

    # Return the collected product details
    return product_details

# Example usage
if __name__ == "__main__":
    product_name = input("Enter the product name: ")
    details = cross_validate_prices(product_name)

    for detail in details:
        print(f"Product Link: {detail['link']}")
        print(f"Extracted Text: {detail['text']}")
        print("="*40)
