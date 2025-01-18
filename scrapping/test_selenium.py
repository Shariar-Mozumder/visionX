from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def fetch_dynamic_content(url):
    # Configure Chrome options
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--enable-unsafe-swiftshader")
    service = Service("C:/Users/Lenovo/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")  # Replace with your ChromeDriver path

    # Start WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(url)
        content = driver.page_source
        print(f"Fetched content for {url}")
        return content
    finally:
        driver.quit()

# Example usage
# url = "https://www.amazon.com/MSI-GTX-1650-Ventus-OCV3/dp/B0CK9SRJWW"
# html_content = fetch_dynamic_content(url)
