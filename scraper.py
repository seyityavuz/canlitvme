import requests
from bs4 import BeautifulSoup
import re
import logging
from time import sleep
from urllib.parse import urlencode

# 🔐 Token parametreleri (güncel token buraya yazılır)
TOKEN_PARAMS = {
    "tkn": "nb_yJgKgr3KkyX8jegf53w",
    "tms": "{i}",
    "hst": "www.canlitv.me",
    "ip": "95.65.213.102",
    "utkn": "{i}"
}

HEADERS = {"User-Agent": "Mozilla/5.0"}
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def build_token_url():
    query = urlencode(TOKEN_PARAMS)
    return f"https://cdn900.canlitv.me/sabantv.m3u8?{query}"

def get_channel_links():
    try:
        # Örnek sayfa: sabantv üzerinden diğer canlı kanallara ulaşılabiliyorsa
        r = requests.get("https://www.canlitv.me/sabantv", headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        links = ["https://www.canlitv.me" + a["href"] for a in soup.select("a[href^='/canli/']")]
        logging.info(f"{len(links)} kanal bulundu.")
        return links
    except Exception as e:
        logging.error(f"Kanal listesi alınamadı: {e}")
        return []

def extract_m3u8_from_iframe(iframe_url):
    try:
        r = requests.get(iframe_url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        match = re.search(r'(https?://[^"\']+\.m3u8[^"\']*)', r.text)
        return match.group(1) if match else None
    except Exception as e:
        logging.warning(f"iframe okunamadı: {iframe_url} → {e}")
        return None

def extract_m3u8_from_channel(channel_url):
    try:
        r = requests.get(channel_url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        iframe = soup.find("iframe")
        if iframe and "src" in iframe.attrs:
            return extract_m3u8_from_iframe(iframe["src"])
    except Exception as e:
        logging.warning(f"Kanal sayfası okunamadı: {channel_url} → {e}")
    return None

def build_playlist():
    links = get_channel_links()
    if not links:
        logging.error("Hiçbir kanal bağlantısı alınamadı. Dosya oluşturulmadı.")
        return

    with open("playlist.m3u8", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        success_count = 0
        for link in links:
            name = link.split("/")[-1].split("-")[0].upper()
            m3u8 = extract_m3u8_from_channel(link)
            if m3u8:
                f.write(f"#EXTINF:-1,{name}\n{m3u8}\n")
                success_count += 1
            else:
                logging.info(f"{name} için m3u8 bulunamadı.")
            sleep(0.5)

    logging.info(f"Toplam {success_count} yayın playlist'e eklendi.")

if __name__ == "__main__":
    build_playlist()
