import requests
from bs4 import BeautifulSoup
import hashlib

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "sv-SE,sv;q=0.9",
}

def sok_sellpy(sokterm):
    url = f"https://www.sellpy.se/search?q={requests.utils.quote(sokterm)}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        annonser = []
        for card in soup.select("a[href*='/item/']")[:20]:
            href = card.get("href", "")
            if not href.startswith("http"):
                href = "https://www.sellpy.se" + href
            title_el = card.select_one("[class*='title'], [class*='name'], h2, h3, p")
            price_el = card.select_one("[class*='price'], [class*='Price']")
            titel = title_el.get_text(strip=True) if title_el else "Okänd titel"
            pris = price_el.get_text(strip=True) if price_el else "Pris saknas"
            aid = "sellpy_" + hashlib.md5(href.encode()).hexdigest()[:12]
            if titel and href:
                annonser.append({"id": aid, "titel": titel, "pris": pris, "url": href, "källa": "Sellpy"})
        return annonser
    except Exception as e:
        print(f"Sellpy fel: {e}")
        return []
