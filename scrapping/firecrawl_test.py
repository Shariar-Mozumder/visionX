from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-ec154c531c9c4f4da10ae89d82767d83")

# Crawl a website:
# crawl_status = app.crawl_url(
#   'https://www.applegadgetsbd.com/product/iphone-16-pro-max', 
#   params={
#     'limit': 100, 
#     'scrapeOptions': {'formats': ['markdown', 'html']}
#   },
#   poll_interval=30
# )

# Scrape a website:
def scrap_firecrawl(url):
    try:
        # scrape_result = app.scrape_url(url, params={'formats': ['markdown']})
        # print(scrape_result)
        # return scrape_result.get("markdown")
        crawl_status = app.scrape_url(
            url, 
            params={
                'limit': 100, 
                'scrapeOptions': {'formats': ['markdown']}
            }
            # poll_interval=30
            )
        return crawl_status
    except Exception as e:
        return str(e)

result=scrap_firecrawl("https://duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.apple.com%2Fiphone%2D16%2Dpro%2F&rut=6ee0d506d6745cf84ab3fba6762af250b2a38f89b9655f10341e69a931819fb7")
print(result)
