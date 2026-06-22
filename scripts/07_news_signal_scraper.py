"""
News Signal Scraper

Output:
data/raw/news/news_signal_raw.csv
data/processed/news_signal.csv
"""

from pathlib import Path
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data/raw/news"
PROCESSED_DIR = PROJECT_ROOT / "data/processed"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


queries = [

"2026 NBA draft workout",

"2026 NBA draft meeting",

"2026 NBA draft rumor",

"2026 NBA draft trade",

"2026 NBA draft medical"

]

rows=[]


HEADERS={

"User-Agent":"Mozilla/5.0"

}


def scrape_google_news(query):

    url=f"https://news.google.com/search?q={query}"

    r=requests.get(url,headers=HEADERS,timeout=30)

    soup=BeautifulSoup(r.text,"html.parser")

    articles=soup.find_all("article")

    for a in articles:

        title=a.get_text(" ",strip=True)

        rows.append({

            "query":query,

            "title":title,

            "scrape_time":datetime.now()

        })


for q in queries:

    try:

        scrape_google_news(q)

        print(q)

    except Exception as e:

        print(q,e)


df=pd.DataFrame(rows)

raw_path=RAW_DIR/"news_signal_raw.csv"

df.to_csv(raw_path,index=False)

print(df.head())