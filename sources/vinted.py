import requests
import hashlib

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}

def sok_vinted(sokterm):
    url = "https://www.vinted.se/api/v2/catalog/items"
    params = {"search_text": sokterm, "per_page": 20, "order": "newest_first"}
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        r.raise_for_status()
        data = r.json()
        annonser = []
        for item in data.get("items", []):
            pris_info = item.get("price", {})
            pris = f"{pris_info.get('amount', '?')} {pris_info.get('currency_code', 'SEK')}"
            annonser.append({
                "id": f"vinted_{item['id']}",
                "titel": item.get("title", ""),
                "pris": pris,
                "url": f"https://www.vinted.se/items/{item['id']}",
                "källa": "Vinted"
            })
        return annonser
    except Exception as e:
        print(f"Vinted fel: {e}")
        return []
