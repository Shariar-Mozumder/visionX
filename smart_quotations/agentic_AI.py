# from phi.app import App
from phi.agent import Agent
# from phi.task import Task
from requests import get
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from scrapping.test_selenium import fetch_dynamic_content
import platform
import asyncio
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Define the Phidata App
# app = App(name="smart_quotation_app", description="Smart Quotation using Phidata agents")

# Define Agents
class SearchAgent(Agent):
    def run(self, query: str, num_results=10):
        """Search for product links on DuckDuckGo."""
        print(f"SearchAgent: Searching for '{query}'")
        base_url = "https://duckduckgo.com/html/"
        headers = {"User-Agent": "Mozilla/5.0"}
        params = {"q": query}
        links = []
        trusted_domains = [
            "amazon",
            "ebay",
            "flipkart",
            "alibaba",
            "aliexpress",
            "etsy",
            "ozon",
            "rakuten",
            "samsung",
            "walmart",
            "cisco",
            "wildberries",
            "shopify",
            "nike",
            "apple",
            "asos",
            
        ]

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




# class ScraperAgent(Agent):
#     def run(self, links: list):
#         """Scrape product prices from the provided links."""
#         print("ScraperAgent: Scraping prices...")
#         headers = {
#             "User-Agent": (
#                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
#                 "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#             )
#         }
#         prices = {}

#         # Extended patterns to include currency names and abbreviations
#         patterns = [
#             r"₹\d{1,3}(,\d{3})*(\.\d+)?",                # Indian Rupee symbol (₹)
#             r"\$\d{1,3}(,\d{3})*(\.\d+)?",               # USD symbol ($)
#             r"£\d{1,3}(,\d{3})*(\.\d+)?",                # GBP symbol (£)
#             r"\d{1,3}(,\d{3})*(\.\d+)?\s?(USD|Dollars)", # USD with text
#             r"\d{1,3}(,\d{3})*(\.\d+)?\s?(INR|Rupees)",  # INR with text
#             r"\d{1,3}(,\d{3})*(\.\d+)?\s?(GBP|Pounds)",  # GBP with text
#             r"\d{1,3}(,\d{3})*(\.\d+)?\s?(EUR|Euros)",   # EUR with text
#         ]

#         for link in links:
#             try:
#                 print(f"Scraping: {link}")
#                 # response = get(link, headers=headers, timeout=10)
#                 # if response.status_code != 200:
#                 #     print(f"Failed to fetch {link}: HTTP {response.status_code}")
#                 #     continue
#                 html_content=fetch_dynamic_content(link)

#                 soup = BeautifulSoup(html_content, "html.parser")

#                 # # Debugging: Check soup content
#                 # print(f"Soup content length: {len(soup.text)}")
#                 # if len(soup.text.strip()) == 0:
#                 #     print(f"Empty content for {link}. Skipping...")
#                 #     continue

#                 # Search for patterns in the text
#                 for pattern in patterns:
#                     match = re.search(pattern, soup.text, re.IGNORECASE)
#                     #pattern or soup not performing well for price, selenium is performing well
#                     if match:
#                         prices[link] = match.group()
#                         break
#             except Exception as e:
#                 print(f"ScraperAgent: Error scraping {link}: {e}")

#         print(f"ScraperAgent: Scraped prices for {len(prices)} links")
#         return prices

from smart_quotations.agents import web_search,web_search1,data_analyst_agent
from scrapping.firecrawl_test import scrap_firecrawl
from scrapping.crawl4AItest import fetch_content
import asyncio

# async def call_fetch_contents(urls):
#     """Call the async function fetch_contents from a sync function."""
#     return await fetch_contents(urls)


class ScraperAgent:
    async def run(self, links: list):
        # """Scrape product prices from the provided links."""
        # print("ScraperAgent: Scraping prices...")
        # headers = {
        #     "User-Agent": (
        #         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        #         "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        #     )
        # }
        # prices = {}
        product_details=[]
        # try:
        # # Use ProactorEventLoop on Windows for better compatibility
        #     if asyncio.get_event_loop().is_closed():
        #         asyncio.set_event_loop(asyncio.new_event_loop())
        #     loop = asyncio.ProactorEventLoop()
        #     asyncio.set_event_loop(loop)
        #     html_contents=loop.run_until_complete(fetch_content(links[0]))
        # except Exception as e:
        #     print(f"Error: {e}")
        # finally:
        #     loop.close()
        # html_contents=await fetch_content(links[0])
        # html_contents=asyncio.run(await fetch_contents(links))

        for link in links:
            try:
                # print(f"Scraping: {link}")
                # html_content = fetch_dynamic_content(link)
                # soup = BeautifulSoup(html_content, "html.parser")
                
                # html_content=scrap_firecrawl(link)
                html_content=await fetch_content(link)
                if len(html_content)<10:
                    continue
                results=web_search1(html_content)
                product_details.append(results)
                # Check which site is being scraped
                # if "amazon" in link:
                #     price = self.parse_amazon_price(soup)
                # elif "ebay" in link:
                #     price = self.parse_ebay_price(soup)
                # elif "flipkart" in link:
                #     price = self.parse_flipkart_price(soup)
                # else:
                #     price = "Site not supported"

                # if price:
                #     prices[link] = price
                # else:
                #     print(f"No price found for {link}")

            except Exception as e:
                print(f"ScraperAgent: Error scraping : {e}")

        # print(f"ScraperAgent: Scraped prices for {len(prices)} links")
        return product_details

    def parse_amazon_price(self, soup):
        """Parse price from Amazon HTML."""
        try:
            price_div = soup.find(id="desktop_unifiedPrice") or soup.find(id="unifiedPrice_feature_div")
            if price_div:
                price_text = price_div.get_text(strip=True)
                return re.search(r"₹\d[\d,]*(\.\d+)?|\$\d[\d,]*(\.\d+)?", price_text).group()
        except Exception as e:
            print(f"Error parsing Amazon price: {e}")
        return None

    def parse_ebay_price(self, soup):
        """Parse price from eBay HTML."""
        try:
            price_div = soup.find("div", class_="x-price-primary")
            shipping_div = soup.find("div", class_="x-shipping-cost")
            if price_div:
                price = price_div.get_text(strip=True)
                shipping = shipping_div.get_text(strip=True) if shipping_div else ""
                return f"{price} {shipping}".strip()
        except Exception as e:
            print(f"Error parsing eBay price: {e}")
        return None

    def parse_flipkart_price(self, soup):
        """Parse price from Flipkart HTML."""
        try:
            price_div = soup.find("div", class_="Nx9bqj")
            discount_div = soup.find("div", class_="UkUFwK")
            if price_div:
                price = price_div.get_text(strip=True)
                discount = discount_div.get_text(strip=True) if discount_div else ""
                return f"{price} {discount}".strip()
        except Exception as e:
            print(f"Error parsing Flipkart price: {e}")
        return None
    
    
# class WebSearchAgent:
#     def __init__(self):
#         self.extractor = PhiDataExtractor()  # Assuming PhiData provides an extractor class

#     def run(self, links: list):
#         """Extract prices and details using PhiData."""
#         print("WebSearchAgent: Extracting prices...")
#         results = {}

#         for link in links:
#             try:
#                 print(f"Processing: {link}")
#                 # Use PhiData to extract structured information
#                 data = self.extractor.extract(link)
#                 if data:
#                     results[link] = {
#                         "price": data.get("price"),
#                         "shipping": data.get("shipping"),
#                         "discount": data.get("discount"),
#                     }
#                 else:
#                     print(f"No data found for {link}")
#             except Exception as e:
#                 print(f"WebSearchAgent: Error processing {link}: {e}")

#         print(f"WebSearchAgent: Extracted data for {len(results)} links")
#         return results

class AnalysisAgent(Agent):
    def run(self, prices: dict):
        """Analyze market data and rank vendors."""
        print("AnalysisAgent: Analyzing market data...")
        parsed_prices = {}
        for link, price in prices.items():
            try:
                numeric_price = float(re.sub(r"[^\d.]", "", price))
                parsed_prices[link] = numeric_price
            except ValueError:
                continue

        # Sort prices
        sorted_prices = sorted(parsed_prices.items(), key=lambda x: x[1])
        print("AnalysisAgent: Analysis complete")
        return sorted_prices


class ReportAgent(Agent):
    def run(self, product_details):
        """Generate a detailed report using a free LLM."""
        from transformers import pipeline

        # Use a free LLM like Mistral or LLaMA
        print("ReportAgent: Generating report...")
        report=data_analyst_agent(product_details)
        # summarizer = pipeline("text-generation", model="mistralai/Mistral-Instruct-v1-7B")

        # context = f"Product: {product_name}\n\nVendor Prices:\n"
        # for link, price in sorted_prices:
        #     context += f"{price} - {link}\n"

        # context += "\nProvide a detailed analysis of the above data."
        # report = summarizer(context, max_length=300)[0]["generated_text"]

        # print("ReportAgent: Report generated")
        return report


# Main Agent to orchestrate tasks
from utils import extract_product_details,extract_Report_details
class SmartQuotationAgent(Agent):
    async def run(self, product_name: str):
        """Orchestrate all tasks to produce the smart quotation."""
        print("SmartQuotationAgent: Starting the workflow...")

        # Step 1: Search for product links
        search_agent = SearchAgent()
        links = search_agent.run(product_name)

        if not links:
            return "No product links found."

        # Step 2: Scrape prices
        scraper_agent = ScraperAgent()
        product_details = await scraper_agent.run(links)

        if not product_details:
            return "No Product details found."
        product_details_json=extract_product_details(product_details)
        print(product_details)

        # Step 3: Analyze market data
        # analysis_agent = AnalysisAgent()
        # sorted_prices = analysis_agent.run(product_details)

        # Step 4: Generate the report
        report_agent = ReportAgent()
        report = report_agent.run(product_details_json)
        report_json=extract_Report_details(report)
        output={
            "Links":links,
            "Product_Details":product_details_json,
            "Report":report_json
        }
        return output


# Register the main agent with the app
# app.add_agent(SmartQuotationAgent(name="smart_quotation"))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import json

app = FastAPI()

class ProductRequest(BaseModel):
    product_name: str
    # location: str

@app.post("/generate-quotation/")
async def generate_quotation(request: ProductRequest):
    agent = SmartQuotationAgent()
    product_name=request.product_name
    if product_name is None:
        return {404,"No input available."}
    result = await agent.run(product_name)
    # Load the string as JSON
    # try:
    #     data = json.loads(result)
        
    #     # Format JSON with indentation
    #     formatted_json = json.dumps(data, indent=4)
    #     print(formatted_json)
    #     return formatted_json
    # except json.JSONDecodeError as e:
    #     print(f"Invalid JSON: {e}")
    return result
    

# Entry point
if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    uvicorn.run("agentic_AI:app", host="0.0.0.0", port=8000, reload=False)
    # product_name = input("Enter the product name: ")
    # agent = SmartQuotationAgent()
    # result = agent.run(product_name)
    # print("\nSmart Quotation Report:")
    # print(result)
