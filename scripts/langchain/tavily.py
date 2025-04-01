#from tavily import TavilyClient
from langchain_community.tools.tavily_search import TavilySearchResults
import sys
import os
import json

TAVILY_API_KEY = sys.argv[1]
os.environ['TAVILY_API_KEY'] = TAVILY_API_KEY
search = TavilySearchResults(max_results=3)
response = search.run("Santosh Pawar Persistent Pune")
print(json.dumps(response, indent=4))
print("======================================")
for result in response:
    print(json.dumps(result))
    print("---------------------------------------")