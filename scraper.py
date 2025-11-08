import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www.canlitv.me"
LIVE_URL = f"{BASE_URL}/live"

def get_channel_links():
    r = requests.get(LIVE_URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    return [BASE_URL + a["href"] for a in soup.select("a[href^='/live/']")]

def extract_m3u8_from_iframe(iframe_url):
    try:
        r = requests.get(iframe_url, headers={"User-Agent": "Mozilla/5.0"})
        m3u8_match = re.search(r'(https?://[^"\']+\.m3u8)', r.text)
        return m3u8_match.group(1) if m3u8_match else None
    except:
        return None

def extract_m3u8_from_channel(channel_url):
    r = requests.get(channel_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    iframe = soup.find("iframe")
    if iframe and "src" in iframe.attrs:
        return extract_m3u8_from_iframe(iframe["src"])
    return None

def build_playlist():
    links = get_channel_links()
    with open("playlist.m3u8", "w") as f:
        f.write("#EXTM3U\n")
        for link in links:
            name = link.split("/")[-1].split("-")[0].upper()
            m3u8 = extract_m3u8_from_channel(link)
            if m3u8:
                f.write(f"#EXTINF:-1,{name}\n{m3u8}\n")

if __name__ == "__main__":
    build_playlist()
