#!/usr/bin/env python
import urllib.request
url='https://vunjabei-clothing-system.onrender.com/api/products/'
print('Requesting', url)
try:
    with urllib.request.urlopen(url, timeout=15) as r:
        print('STATUS', r.status)
        body = r.read(5000).decode('utf-8', errors='replace')
        print('BODY SNIPPET:\n')
        print(body[:2000])
except Exception as e:
    print('ERROR', repr(e))
