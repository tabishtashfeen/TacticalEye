import requests,re
xml=requests.get('https://csnades.gg/sitemap.xml', timeout=30).text
locs=re.findall(r'<loc>([^<]+)</loc>', xml)
from collections import Counter
cats=Counter()
for u in locs:
    if '/smokes/' in u: cats['smokes']+=1
    if '/molotovs/' in u: cats['molotovs']+=1
    if '/flashbangs/' in u: cats['flashbangs']+=1
    if '/hegrenades/' in u: cats['hegrenades']+=1
    if '/grenades/' in u: cats['grenades']+=1
    if '/nades/' in u: cats['nades']+=1
print(cats)
print('total nades', sum(cats.values()))
