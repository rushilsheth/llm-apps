import os
import requests
from dotenv import load_dotenv

import html2text


# Brave Search API configuration
_BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"
_BRAVE_SEARCH_PARAMS = {
    "count": 5,  # Number of results to return
    "search_lang": "en",
    "country": "US"
}


class BraveSearchClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("BRAVE_API_KEY")
        if not self.api_key:
            raise ValueError(f"BRAVE_API_KEY environment variable not set, {os.environ.get('BRAVE_API_KEY')}")
        self.search_url = _BRAVE_SEARCH_URL
        self.default_params = _BRAVE_SEARCH_PARAMS
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = True
        
    def search(self, query):
        """
        Perform a search using the Brave Search API
        
        Args:
            query (str): The search query
            
        Returns:
            dict: Search results
        """
        headers = {"Accept": "application/json", "X-Subscription-Token": self.api_key}
        params = {**self.default_params, "q": query}
        
        try:
            response = requests.get(self.search_url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error performing Brave search: {e}")
            return {"error": str(e)}
    
    def get_sources(self, query):
        """
        Get source content from search results
        
        Args:
            query (str): The search query
            
        Returns:
            list: List of dictionaries containing source information
        """
        search_results = self.search(query)
        sources = []
        
        if "error" in search_results:
            return [{"title": "Error", "url": "", "content": f"Search error: {search_results['error']}"}]
        
        if "web" not in search_results or "results" not in search_results["web"]:
            return [{"title": "No Results", "url": "", "content": "No results found"}]
        
        for result in search_results["web"]["results"]:
            source = {
                "title": result.get("title", "No Title"),
                "url": result.get("url", ""),
                "description": result.get("description", "No description available")
            }
            
            # Try to fetch the actual content from the webpage
            try:
                content_response = requests.get(source["url"], timeout=5)
                if content_response.status_code == 200:
                    # Convert HTML to plain text
                    source["content"] = self.html_converter.handle(content_response.text)
                else:
                    source["content"] = source["description"]
            except Exception as e:
                print(f"Error fetching content from {source['url']}: {e}")
                source["content"] = source["description"]
            
            sources.append(source)
            
            # Limit content length to avoid token limits with the LLM
            if len(source["content"]) > 8000:
                source["content"] = source["content"][:8000] + "..."
        
        return sources