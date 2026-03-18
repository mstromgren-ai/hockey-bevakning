import requests
import xml.etree.ElementTree as ET
import hashlib
import re

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; HockeyBevakning/1.0)"}

def sok_blocket(sokterm):
    url = f"https://www.blocket.se/annonser/hela_sverige?q={requests.utils.quote(sokterm)}&format=rss"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        root = ET.fromstring(r.content)
        annonser = []
        for item in root.findall(".//item"):
            title = item.findtext("title", "")
            link = item.findtext("link", "")
            desc = item.findtext("description", "")
            pris_match = re.search(r'[\d\s]+\s*kr', desc)
            pris = pris_match.group(0).strip() if pris_match else "Pris saknas"
            aid = "blocket_" + hashlib.md5(link.encode()).hexdigest()[:12]
            annonser.append({"id": aid, "titel": title, "pris": pris, "url": link, "källa": "Blocket"})
        return annonser
    except Exception as e:
        print(f"Blocket fel: {e}")
        return []
