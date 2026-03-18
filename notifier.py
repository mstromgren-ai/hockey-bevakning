import requests

def skicka_telegram(token, chat_id, annons):
    källa = annons.get("källa", "Okänd")
    titel = annons.get("titel", "Okänd titel")
    pris = annons.get("pris", "Pris saknas")
    url = annons.get("url", "")
    bevakning = annons.get("bevakning", "")

    emoji = {"Blocket": "🟡", "Vinted": "🟢", "Sellpy": "🔵", "Tradera": "🟠"}.get(källa, "⚪")

    text = (
        f"{emoji} *Ny annons – {källa}*\n"
        f"🔍 Sökte: _{bevakning}_\n"
        f"📦 {titel}\n"
        f"💰 {pris}\n"
        f"🔗 [Öppna annons]({url})"
    )

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
        timeout=10
    )
