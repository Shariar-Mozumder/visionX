# from phi.tools import Tool
# import requests

# class LocalOllamaTool(Tool):
#     def __init__(self, api_url="http://localhost:11434/api/v1/completions", model_name="qwen2.5:3b"):
#         """
#         Tool to interact with the local Ollama model.
#         :param api_url: The URL for the Ollama API.
#         :param model_name: The name of the local model to use.
#         """
#         super().__init__(name="LocalOllamaTool", description="Tool for interacting with the local Ollama model.")
#         self.api_url = api_url
#         self.model_name = model_name

#     def run(self, inputs: dict) -> str:
#         """
#         Interact with the local Ollama model.
#         :param inputs: A dictionary containing the "prompt" key.
#         :return: The generated response.
#         """
#         prompt = inputs.get("prompt", "")
#         if not prompt:
#             raise ValueError("Prompt is required for LocalOllamaTool")

#         payload = {
#             "model": self.model_name,
#             "prompt": prompt
#         }

#         # Query the Ollama API
#         response = requests.post(self.api_url, json=payload)
#         if response.status_code == 200:
#             return response.json().get("completion", "")
#         else:
#             raise RuntimeError(f"Error querying Ollama model: {response.text}")
        
# from phi.agent import Agent
# from phi.tools.duckduckgo import DuckDuckGo
# from phi.tools.googlesearch import GoogleSearch
# # from phi.tools import OllamaTool
# api_url="http://localhost:11434/api/v1/completions"
# # Initialize the Local Ollama Tool
# ollama_tool = LocalOllamaTool(api_url=api_url,model_name="qwen2.5:3b")  # Replace "qwen2.5:3b" with your model name if different
# # ollama_tools = OllamaTool(model="llama-2", base_url="http://localhost:11434")
# # Define the Agent
# data_analyst_agent = Agent(
#     # model=ollama_tools,
#     tools=[ollama_tool, DuckDuckGo(), GoogleSearch()],
#     description="You are a Research, Report and Analysis Agent Who can do price research, vendor ranking, market analysis and giving report from the given product details list.",
#     instructions=[
#         "You are here to research, analyze and report the Smart Quotations: price research, vendor ranking, market analysis",
#         "Data you are given may be unstructured, please adjust and keep the lists data of product, price, source, and features",
#         "Show me a research data of vendor Rankings.",
#         "Choose an appropriate Reporting Template with proper and necessary data in JSON format.",
#         "Show me the result as a only in JSON Format no title, no noting, I want to see it in JSON in my API",
#     ],
#     show_tool_calls=True,
#     markdown=True,
# )



import requests


class LocalOllamaTool:
    def __init__(self, api_url="http://localhost:11434/api/generate", model_name="qwen2.5:3b"):
        """
        Initialize the Local Ollama Tool.
        :param api_url: The base URL for the local Ollama API.
        :param model_name: The name of the model to use for completions.
        """
        self.api_url = api_url
        self.model_name = model_name

    def run(self, prompt: str) -> str:
        """
        Send a prompt to the local Ollama API and get a response.
        :param prompt: The input prompt for the model.
        :return: The generated text response.
        """
        if not prompt:
            raise ValueError("Prompt is required for LocalOllamaTool")

        # Define the payload
        payload = {
            "model": self.model_name,
            "prompt": prompt
        }

        # Send the request to the Ollama API
        response = requests.post(self.api_url, json=payload)

        if response.status_code == 200:
            # Parse and return the completion
            return response.json().get("completion", "")
        else:
            # Handle errors
            raise RuntimeError(f"Error querying Ollama model: {response.text}")


class DuckDuckGoTool:
    def __init__(self):
        self.base_url = "https://api.duckduckgo.com/"

    def search(self, query: str) -> str:
        """
        Searches DuckDuckGo and retrieves a brief result.
        """
        params = {"q": query, "format": "json", "no_html": 1}
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            # Return an abstract or related topics if available
            return data.get("AbstractText", "No relevant information found.")
        else:
            raise RuntimeError(f"Error querying DuckDuckGo: {response.text}")
class DataAnalystAgent:
    def __init__(self, ollama_tool, duckduckgo_tool=None, google_tool=None):
        self.ollama_tool = ollama_tool
        self.duckduckgo_tool = duckduckgo_tool
        self.google_tool = google_tool

    def process(self, prompt: str, use_search: bool = False, search_engine: str = "duckduckgo") -> str:
        """
        Processes a query using the Ollama tool and optionally uses a search engine.
        """
        # Step 1: Use the local Ollama tool
        ollama_response = self.ollama_tool.run(prompt)

        # Step 2: Use a search engine if requested
        if use_search:
            if search_engine == "duckduckgo" and self.duckduckgo_tool:
                search_results = self.duckduckgo_tool.search(prompt)
                ollama_response += f"\n\nDuckDuckGo Search Results: {search_results}"
            elif search_engine == "google" and self.google_tool:
                search_results = self.google_tool.search(prompt)
                ollama_response += f"\n\nGoogle Search Results: {search_results}"
            else:
                ollama_response += "\n\nNo valid search engine found."

        return ollama_response


# Initialize the Tools
ollama_tool = LocalOllamaTool(api_url="http://localhost:11434/api/generate", model_name="qwen2.5:3b")
duckduckgo_tool = DuckDuckGoTool()
# google_tool = GoogleSearchTool(api_key="YOUR_GOOGLE_API_KEY", cse_id="YOUR_CSE_ID")

# Create the Agent
data_analyst_agent = DataAnalystAgent(
    ollama_tool=ollama_tool,
    duckduckgo_tool=duckduckgo_tool,
    # google_tool=google_tool,
)

# Test the Agent
query = "Why is the sky blue?"
response = data_analyst_agent.process(query, use_search=True, search_engine="duckduckgo")
print(response)
