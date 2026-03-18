import yaml
import json
import os
import re
from sources.blocket import sok_blocket
from sources.vinted import sok_vinted
from sources.sellpy import sok_sellpy
from sources.tradera import sok_tradera
from notifier import skicka_telegram

SEEN_FILE = "seen_ads.json"

def ladda_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}

def spara_seen(seen):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(seen, f, ensure_ascii=False, indent=2)

def ladda_bevakningar():
    with open("bevakningar.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)["bevakningar"]

def bygg_sokterm(b):
    delar = [str(b.get("märke", "")), str(b.get("modell", "")), str(b.get("storlek", ""))]
    return " ".join(d for d in delar if d).strip()

def main():
    seen = ladda_seen()
    bevakningar = ladda_bevakningar()
    nya = []

    for b in bevakningar:
        sokterm = bygg_sokterm(b)
        max_pris = b.get("max_pris")
        hits = sok_blocket(sokterm) + sok_vinted(sokterm) + sok_sellpy(sokterm) + sok_tradera(sokterm)

        for annons in hits:
            aid = annons["id"]
            if aid in seen:
                continue
            seen[aid] = True
            if max_pris and annons.get("pris"):
                siffror = re.findall(r'\d+', str(annons["pris"]).replace(" ", ""))
                if siffror and int(siffror[0]) > max_pris:
                    continue
            annons["bevakning"] = sokterm
            nya.append(annons)

    if nya:
        token = os.environ["TELEGRAM_TOKEN"]
        chat_id = os.environ["TELEGRAM_CHAT_ID"]
        for annons in nya:
            skicka_telegram(token, chat_id, annons)

    spara_seen(seen)
    print(f"✅ Klar. {len(nya)} nya annonser.")

if __name__ == "__main__":
    main()
