import requests
import re
url='https://csnades.gg/'
resp=requests.get(url)
print('status', resp.status_code)
html=resp.text
links=re.findall(r'href="([^"]+)"', html)
print('total links', len(links))
internal=[l for l in links if l.startswith('/')]
print('internal count', len(internal))
print('sample internal', sorted(set(internal))[:50])
