import os
from bs4 import BeautifulSoup
from requests import get
from urllib.parse import urljoin
import requests
from dotenv import load_dotenv
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
google_cx=os.getenv('CX')

"""Search for product links on DuckDuckGo."""
def Duckduck_search( query: str, num_results=10):
        print(f"SearchAgent: Searching for '{query}'")
        base_url = "https://duckduckgo.com/html/"
        headers = {"User-Agent": "Mozilla/5.0"}
        params = {"q": query}
        links = []
        
        response = get(base_url, params=params, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        for a in soup.find_all("a", href=True, class_="result__a"):
            full_url = urljoin(base_url, a["href"])
            # if any(domain in full_url for domain in trusted_domains):
            links.append(full_url)
            if len(links) >= num_results:
                break

        print(f"SearchAgent: Found {len(links)} links")
        return links


def google_search(query: str, num_results=10):
    """
    Perform a Google search using the Custom Search JSON API.
    
    Args:
        query (str): Search query.
        api_key (str): API key for the Google Custom Search JSON API.
        cx (str): Custom search engine ID.
        num_results (int): Number of results to retrieve.
    
    Returns:
        list: List of result links.
    """
    print(f"SearchAgent: Searching for '{query}'")
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": google_api_key,
        "cx": google_cx,
        "num": min(num_results, 10),  # Max 10 results per request.
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        results = response.json()
        links = [item["link"] for item in results.get("items", [])]
        print(f"SearchAgent: Found {len(links)} links")
        return links
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []
    except KeyError:
        print("Error: Unexpected response format.")
        return []

# results=Duckduck_search(query="Redmi 12C")
# results=google_search(query="Redmi 12C",api_key=google_api_key,cx=google_cx,num_results=10)
