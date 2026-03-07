import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

BBC_SOURCES = {
    "pidgin": "https://www.bbc.com/pidgin",
    "hausa": "https://www.bbc.com/hausa",
    "yoruba": "https://www.bbc.com/yoruba",
    "swahili": "https://www.bbc.com/swahili",
    "igbo": "https://www.bbc.com/igbo",
    "amharic": "https://www.bbc.com/amharic",
    "somali": "https://www.bbc.com/somali",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

os.makedirs("data/bbc", exist_ok=True)

def get_article_text(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        s = BeautifulSoup(r.content, "lxml")
        
        # Try multiple BBC article text selectors
        content = (
            s.find("article") or
            s.find(attrs={"data-component": "text-block"}) or
            s.find(class_=lambda x: x and "article" in x.lower()) or
            s.find("main")
        )
        
        if content:
            paragraphs = content.find_all("p")
        else:
            paragraphs = s.find_all("p")

        text = " ".join([p.get_text().strip() for p in paragraphs if len(p.get_text()) > 30])
        title = s.find("h1")
        title = title.get_text().strip() if title else ""
        return title, text
    except:
        return "", ""

for lang, base_url in BBC_SOURCES.items():
    print(f"\n🌍 Scraping BBC {lang}...")
    articles = []
    links = set()

    # Scrape multiple pages
    for page_url in [base_url, base_url + "/tori", base_url + "/news", base_url + "/sport"]:
        try:
            res = requests.get(page_url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(res.content, "lxml")
            
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if f"/{lang}/" in href:
                    full_url = "https://www.bbc.com" + href if href.startswith("/") else href
                    if any(x in full_url for x in ["/tori-", "/labarai-", "/habari-", "/sport-", "/world-"]):
                        links.add(full_url)
            time.sleep(0.5)
        except:
            pass

    print(f"  Found {len(links)} article links")

    for link in list(links)[:50]:
        title, text = get_article_text(link)
        if len(text) > 200:
            articles.append({
                "language": lang,
                "headline": title,
                "text": text,
                "url": link,
                "source": "bbc_scraped"
            })
            print(f"  ✅ {title[:60]}")
        time.sleep(0.5)

    if articles:
        df = pd.DataFrame(articles)
        df.to_csv(f"data/bbc/{lang}_bbc.csv", index=False)
        print(f"  💾 Saved {len(articles)} articles")
    else:
        print(f"  ⚠️  No articles saved for {lang}")

print("\n✅ BBC scraping complete!")