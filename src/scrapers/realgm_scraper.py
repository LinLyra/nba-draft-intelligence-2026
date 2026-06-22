import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

def fetch_html(url: str) -> str:

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Referer": "https://basketball.realgm.com/",
        "Connection": "keep-alive"
    }
    
    print(f"[*] Fetching via masked requests: {url}")
    

    time.sleep(3) 
    
    response = requests.get(url, headers=headers, timeout=15)
    
    if response.status_code == 403:
        raise RuntimeError(f"RealGM returned 403 Forbidden. IP might be temporarily flagged. Status: {response.status_code}")
    elif response.status_code != 200:
        raise RuntimeError(f"Failed to fetch data, status code: {response.status_code}")
        
    return response.text

def scrape_realgm_future_picks():
    url = "https://basketball.realgm.com/nba/draft/future_drafts/detailed"
    
   
    html_content = fetch_html(url)

    tables = pd.read_html(html_content)
    print(f"[✓] Successfully parsed {len(tables)} tables.")
