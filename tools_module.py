from langchain.tools import tool
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()
# ________________________________________________________________________________ #
# Search Tool Class Definitions
# ________________________________________________________________________________ #

@dataclass()
class SearchTool:
    """A class to represent a generic web search tool."""

    def web_search(self, message: str) -> str:
        """This tool performs a web search."""
        pass

class TavilySearchTool(SearchTool):
    """A class to represent a Tavily search tool."""
    search: TavilySearch
    search: TavilySearch = TavilySearch(max_results=3)

    def web_search(self, message: str) -> str:
        """This tool performs a web search using Tavily."""
        web_search_results = self.search.invoke(input=message)
        return web_search_results["results"][0]["content"]


# ________________________________________________________________________________ #
# Tool Definitions
# ________________________________________________________________________________ #

@tool
def say_hello(name: str) -> str:
    """This tool is used to greet a user"""
    # print("'Say Hello' tool has been called.")
    return f"Hello {name}, What can I help you with today?"


@tool
def search_tool(search_engine: SearchTool, message: str) -> str:
    """This tool performs a web search using a generic search class."""
    # web_search = TavilySearch(max_results=3)
    # web_search_results = web_search.invoke(input=message)
    return search_engine.web_search(message)


if __name__ == "__main__":
    user_input = input("Enter your search query: ")
    search = search_tool(user_input)
    print("Search Result:", search)