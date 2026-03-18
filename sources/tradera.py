import requests
from bs4 import BeautifulSoup
import hashlib

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}

def sok_tradera(sokterm):
    url = f"https://www.tradera.com/search?q={requests.utils.quote(sokterm)}&sortBy=AddedOn"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        annonser = []
        for item in soup.select("[class*='item-card'], [class*='ItemCard'], [class*='search-result']")[:20]:
            link_el = item.select_one("a[href]")
            if not link_el:
                continue
            href = link_el.get("href", "")
            if not href.startswith("http"):
                href = "https://www.tradera.com" + href
            title_el = item.select_one("h2, h3, [class*='title'], [class*='header']")
            price_el = item.select_one("[class*='price'], [class*='Price']")
            titel = title_el.get_text(strip=True) if title_el else "Okänd titel"
            pris = price_el.get_text(strip=True) if price_el else "Pris saknas"
            aid = "tradera_" + hashlib.md5(href.encode()).hexdigest()[:12]
            annonser.append({"id": aid, "titel": titel, "pris": pris, "url": href, "källa": "Tradera"})
        return annonser
    except Exception as e:
        print(f"Tradera fel: {e}")
        return []
