import requests
import json
import re

def scrape_csnades():
    nades = []

    # We will scrape standard popular nades from HTML
    url = "https://csnades.gg/"
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text

        # very simple extraction for demo purposes
        matches = re.finditer(r'href="([^"]+)"', html)
        for match in matches:
            href = match.group(1)
            if "/smokes/" in href or "/molotovs/" in href or "/flashbangs/" in href:
                nade_url = f"https://csnades.gg{href}" if href.startswith('/') else href
                if nade_url.startswith("https://csnades.gg/"):
                    nades.append({"url": nade_url})

    # ensure unique
    nades = [dict(t) for t in {tuple(d.items()) for d in nades}]

    with open("nades_to_train.json", "w") as f:
        json.dump(nades, f, indent=4)
    print(f"Found {len(nades)} lineup references to process for training.")

if __name__ == "__main__":
    scrape_csnades()
