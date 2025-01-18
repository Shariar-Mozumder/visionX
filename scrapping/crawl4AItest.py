import asyncio
from crawl4ai import *

async def main(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url,
        )
        print(result.markdown)
        return result.markdown

async def fetch_content(url):
    result=await main(url)
    return result

# if __name__ == "__main__":
#     url="https://duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.apple.com%2Fshop%2Fbuy%2Diphone%2Fiphone%2D16%2Dpro&rut=c8e0aa132246cb9659097e067cca7b03f82606561796da8124750a046917be44"
#     asyncio.run(main(url))


# import asyncio
# from crawl4ai import AsyncWebCrawler

# async def fetch_product_info_sequential(urls):
#     html_list=[]
#     async with AsyncWebCrawler() as crawler:
#         for url in urls:
#             result = await crawler.arun(url=url)
#             html_list.append(result)
#             print(result.markdown)

# def fetch_contents(urls):
#     # urls = [
#     #     "https://www.amazon.sa/-/en/Apple-iPhone-Pro-Max-256/dp/B0DGJN6RDB",
#     #     "https://www.example.com/product2",
#     #     "https://www.example.com/product3"
#     # ]
#     asyncio.run(fetch_product_info_sequential(urls))

# if __name__ == "__main__":
#     asyncio.run(main())
# from crawl4ai.web_crawler import WebCrawler

# def fetch_data_sync(urls):
#     with WebCrawler() as crawler:
#         return crawler.fetch(urls)

# async def fetch_product_info_sequential(urls):
#     # html_list = []
#     # async with AsyncWebCrawler() as crawler:
#     #     for url in urls:
#     #         result = await crawler.arun(url=url)
#     #         html_list.append(result)
#     #         print(result.markdown)
#     # return html_list
#     html_list = []
    
#     crawler = WebCrawler()
#     try:
#         for url in urls:
#             result = crawler.fetch_page(url)
#             html_list.append(result.markdown)
#             print(result.markdown) # Adjust this if the `fetch` method is asynchronous
#     # finally:
#     #     crawler.
#     except Exception as e:
#         print(str(e))
        
#     return html_list

# async def fetch_contents(urls):
#     return await fetch_product_info_sequential(urls)

# if __name__ == "__main__":
#     urls = [
#         "https://www.amazon.sa/-/en/Apple-iPhone-Pro-Max-256/dp/B0DGJN6RDB",
#         "https://www.example.com/product2",
#         "https://www.example.com/product3"
#     ]
#     results=asyncio.run( fetch_contents(urls))


# from dotenv import load_dotenv
# from phi.agent import Agent
# from phi.tools.crawl4ai_tools import Crawl4aiTools
# from phi.model.groq import Groq
# load_dotenv()

# agent = Agent(
#     model=Groq(id="llama3-8b-8192"),
#     tools=[Crawl4aiTools(max_length=None)], 
#     description="You are a web-scraper specializing in fetching product prices and features from reliable e-commerce websites based on the given link.",
#     instructions=[
#         "You are a product price agent specializing in finding products and their prices from reliable e-commerce websites based on the given link.",
#         "Always respond in JSON format.",
#         "Ensure each product has the following fields: product (name), price, source (with hyperlink), and features.",
#         "Price is mandatory; do not fetch or include products without prices. If the price is unknown or not available, ignore the products.",
#         "Search for products only on trusted platforms such as Google Shopping, Amazon, Flipkart, Myntra, Meesho, Nike, and other reputable websites.",
#         "Verify that each product is in stock and available for purchase.",
#         "Do not include counterfeit or unverified products.",
#         "Prioritize finding products that satisfy as many user requirements as possible, but ensure a minimum match of 50%.",
#         "Clearly mention the key attributes of each product (e.g., price, brand, features) in the response.",
#         "Format the response neatly in JSON format as shown in this example:",
#         '''
#         [
#             {
#                 "product": "abcd",
#                 "price": "$xx.xx",
#                 "source": "[Amazon](https://abcd)",
#                 "features": "- 6 hours battery life\\n- Charging case provides additional 2 hours playtime\\n- Wireless earbuds for freedom and convenience\\n- High-quality audio with clear and crisp sound"
#             },
#             {
#                 "product": "Lenovo TWS X5 Wireless Earbuds",
#                 "price": "$79.99",
#                 "source": "[Ebay](https://abcd)",
#                 "features": "- 8 hours battery life\\n- Fast charging gives you 2 hours of playback with just 15 minutes of charging\\n- Committed to delivering high-quality audio\\n- Compact and lightweight design for easy portability"
#             }
#         ]
#         '''
#     ],
#     # show_tool_calls=True,
#     markdown=True,
#     show_tool_calls=True)
# agent.print_response("https://www.amazon.sa/-/en/Apple-iPhone-Pro-Max-256/dp/B0DGJN6RDB")


# from crawl4ai import WebCrawler

# import html5lib
# # Instance of WebCrawler
# crawler = WebCrawler()
# # Warm up the crawler (load necessary models)
# crawler.warmup()
# # Run the crawler on a URL
# result = crawler.run(url='https://duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.apple.com%2Fiphone%2D16%2Dpro%2F&rut=6ee0d506d6745cf84ab3fba6762af250b2a38f89b9655f10341e69a931819fb7')
# # Print the extracted content
# print(result)


# import asyncio
# from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

# async def main():
#     # Configure browser
#     browser_config = BrowserConfig(headless=True, verbose=True)

#     # Set crawl run configurations
#     crawl_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

#     # Use AsyncWebCrawler
#     async with AsyncWebCrawler(browser_config=browser_config) as crawler:
#         result = await crawler.arun(
#             url="https://duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.apple.com%2Fiphone%2D16%2Dpro%2F&rut=6ee0d506d6745cf84ab3fba6762af250b2a38f89b9655f10341e69a931819fb7",
#             config=crawl_config
#         )
#         print("Success:", result.markdown)

# asyncio.run(main())
