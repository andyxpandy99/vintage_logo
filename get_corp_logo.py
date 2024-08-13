import requests
from bs4 import BeautifulSoup
import time

def get_wikipedia_url(company_name):
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": company_name,
        "prop": "info",
        "inprop": "url"
    }

    response = requests.get(base_url, params=params)
    time.sleep(0.1)  # Add a delay of 0.1 seconds between requests to Wikipedia API
    data = response.json()

    pages = data.get("query", {}).get("pages", {})
    for page_id, page_info in pages.items():
        if "missing" in page_info:
            return None  # Page does not exist
        return page_info.get("fullurl")

def get_company_logo_url(wikipedia_url):
    response = requests.get(wikipedia_url)
    time.sleep(0.1)  # Add a delay of 0.1 seconds between requests to Wikipedia pages
    soup = BeautifulSoup(response.content, 'html.parser')

    infobox = soup.find('table', {'class': 'infobox vcard'})
    if not infobox:
        return None

    logo_image = infobox.find('td', class_=lambda x: x and x.startswith('infobox-image'))
    if not logo_image:
        return None

    logo_link = logo_image.find('a', {'class': 'mw-file-description'})
    if not logo_link:
        return None

    logo_url = logo_link.get('href')
    if not logo_url:
        return None

    full_logo_url = f"https://en.wikipedia.org{logo_url}"
    return full_logo_url