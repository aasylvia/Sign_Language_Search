
import requests

# Replace with your actual API key and Search Engine ID
API_KEY = 'AIzaSyCmvjYWpszU-1A0u716zJ7V513arp6GPE0'
SEARCH_ENGINE_ID = '37b47b1ff884d4938'

def search_query(query):
    """This function sends a search query to the Google Custom Search API and returns the results."""
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
    
    # Make the request to the Google Custom Search API
    response = requests.get(url)
    
    # Check if the response status code is OK (200)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Test the function with a sample search query
results = search_query("Sign language")

# Check if we got valid results
if results:
    # Print out the titles and links of the search results
    for item in results.get("items", []):
        print(f"Title: {item['title']}")
        print(f"Link: {item['link']}")
        print(f"Snippet: {item['snippet']}\n")
