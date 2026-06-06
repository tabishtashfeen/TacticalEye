import json
import re
import requests
import xml.etree.ElementTree as ET

BASE_URL = "https://csnades.gg"
SITEMAP_URL = f"{BASE_URL}/sitemap.xml"
NADE_SEGMENTS = ("/smokes/", "/molotovs/", "/flashbangs/", "/hegrenades/")


def fetch_sitemap_urls():
    response = requests.get(SITEMAP_URL, timeout=20)
    response.raise_for_status()
    root = ET.fromstring(response.text)
    urls = [elem.text for elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    if not urls:
        urls = [elem.text for elem in root.findall('.//loc')]
    return [url.strip() for url in urls if url and url.strip()]


def filter_nade_urls(urls):
    filtered = []
    for url in urls:
        if any(segment in url for segment in NADE_SEGMENTS):
            if url.startswith("/"):
                url = f"{BASE_URL}{url}"
            if url.startswith(BASE_URL):
                filtered.append({"url": url})
    return filtered


def scrape_csnades():
    nades = []
    try:
        urls = fetch_sitemap_urls()
        print(f"Loaded {len(urls)} URLs from sitemap.")
    except Exception as exc:
        print(f"Failed to load sitemap: {exc}")
        print("Falling back to homepage crawl.")
        homepage = requests.get(BASE_URL, timeout=20)
        homepage.raise_for_status()
        urls = [match.group(1) for match in re.finditer(r'href="([^"]+)"', homepage.text)]

    nades = filter_nade_urls(urls)
    nades = [dict(t) for t in {tuple(sorted(d.items())) for d in nades}]
    nades.sort(key=lambda item: item["url"])

    with open("nades_to_train.json", "w", encoding="utf-8") as f:
        json.dump(nades, f, indent=4)

    print(f"Found {len(nades)} lineup references to process for training.")


if __name__ == "__main__":
    scrape_csnades()
