import requests
from bs4 import BeautifulSoup
import hashlib

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "sv-SE,sv;q=0.9",
}

def sok_blocket(sokterm):
    url = f"https://www.blocket.se/annonser/hela_sverige?q={requests.utils.quote(sokterm)}&sort=date"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        annonser = []
        for card in soup.select("article, [class*='ListItem'], [class*='list-item']")[:20]:
            link_el = card.select_one("a[href]")
            if not link_el:
                continue
            href = link_el.get("href", "")
            if not href.startswith("http"):
                href = "https://www.blocket.se" + href
            title_el = card.select_one("h2, h3, [class*='title'], [class*='Title']")
            price_el = card.select_one("[class*='price'], [class*='Price']")
            titel = title_el.get_text(strip=True) if title_el else "Okänd titel"
            pris = price_el.get_text(strip=True) if price_el else "Pris saknas"
            aid = "blocket_" + hashlib.md5(href.encode()).hexdigest()[:12]
            annonser.append({"id": aid, "titel": titel, "pris": pris, "url": href, "källa": "Blocket"})
        return annonser
    except Exception as e:
        print(f"Blocket fel: {e}")
        return []
