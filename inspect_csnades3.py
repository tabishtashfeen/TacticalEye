import requests
import re
xml=requests.get('https://csnades.gg/sitemap.xml', timeout=30).text
locs=re.findall(r'<loc>([^<]+)</loc>', xml)
print(len(locs))
print(locs[:20])
print(locs[-20:])
