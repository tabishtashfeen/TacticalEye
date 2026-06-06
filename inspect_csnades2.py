import requests
for path in ['/sitemap.xml','/robots.txt','/maps','/guides']:
    try:
        r=requests.get('https://csnades.gg'+path, timeout=10)
        print(path, r.status_code, len(r.text))
        if r.status_code==200:
            print(r.text[:500])
            print('---')
    except Exception as e:
        print(path, 'ERR', e)
