import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re
import time
from urllib.parse import urljoin

from requests.exceptions import HTTPError

def get_product_links(query, num_results=15, retries=3, delay=5):
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
# Step 1: Search for product on Google
# def get_product_links(query, num_results=5):
#     """Get top e-commerce links for a product using Google Search."""
#     links = []
#     for result in search(query, num_results=num_results):
#         if "amazon" in result or "ebay" in result or "flipkart" in result:
#             links.append(result)
#     return links


def duckduckgo_search(query, num_results=15, retries=3, delay=5):
    """
    Search DuckDuckGo and return a list of full URLs.
    
    Args:
        query (str): Search query.
        num_results (int): Number of top results to return.
        retries (int): Number of retries in case of HTTP errors.
        delay (int): Delay in seconds between retries.
    
    Returns:
        list: List of complete URLs.
    """
    base_url = "https://duckduckgo.com/html/"
    params = {"q": query}
    headers = {"User-Agent": "Mozilla/5.0"}
    
    links = []
    attempts = 0

    while attempts < retries:
        try:
            print(f"Attempt {attempts + 1}: Searching for '{query}'")
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            for a in soup.find_all("a", href=True, class_="result__a"):
                # Resolve relative links to absolute links
                full_url = urljoin(base_url, a["href"])
                if full_url.startswith("http"):  # Ensure it's a valid link
                    links.append(full_url)
                if len(links) >= num_results:
                    return links

            if not links:
                print("No relevant links found. Retrying...")
            else:
                return links
            break  # Exit loop if successful
            

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
            attempts += 1

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise e  # Re-raise other exceptions

    raise Exception("Failed to fetch results after multiple retries.")


# Step 2: Extract price from a webpage
def scrape_price(url):
    """Scrape product price from a webpage."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Identify price patterns (example for Amazon)
        patterns = [
            r"₹\d{1,3}(,\d{3})*(\.\d+)?",  # Indian Rupee
            r"\$\d{1,3}(,\d{3})*(\.\d+)?",  # USD
            r"£\d{1,3}(,\d{3})*(\.\d+)?"    # GBP
        ]
        
        for pattern in patterns:
            match = re.search(pattern, soup.text)
            if match:
                return match.group()
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    return None

# Step 3: Cross-validate prices
def cross_validate_prices(product_name, num_results=15):
    """Find and validate product prices across multiple websites."""
    # links = get_product_links(product_name, num_results)
    links = duckduckgo_search(product_name, num_results)
    prices = {}
    
    for link in links:
        price = scrape_price(link)
        if price:
            prices[link] = price
    
    return prices

# Step 4: Get the best price
def get_best_price(prices):
    """Identify the lowest price."""
    parsed_prices = {}
    for link, price in prices.items():
        try:
            numeric_price = float(re.sub(r"[^\d.]", "", price))  # Extract numeric value
            parsed_prices[link] = numeric_price
        except ValueError:
            continue
    
    # Sort by price
    best_price = min(parsed_prices.items(), key=lambda x: x[1], default=None)
    return best_price

# Main Function
if __name__ == "__main__":
    product_name = input("Enter the product name: ")
    print("Searching for product prices...")
    
    prices = cross_validate_prices(product_name)
    if not prices:
        print("No prices found.")
    else:
        print("Prices found:")
        for link, price in prices.items():
            print(f"{price} - {link}")
        
        best_price = get_best_price(prices)
        if best_price:
            print("\nBest Price:")
            print(f"{best_price[1]} - {best_price[0]}")
        else:
            print("Unable to determine the best price.")
