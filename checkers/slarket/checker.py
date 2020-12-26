#!/usr/bin/env python3

from gevent import monkey

monkey.patch_all()

import sys
import os
import requests
import json

from checklib import *
from time import sleep
from random import randint

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from slarket_lib import *


class Checker(BaseChecker):
    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.mch = CheckMachine(self)

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except requests.exceptions.ConnectionError:
            self.cquit(Status.DOWN, 'Connection error', 'Got requests connection error')

    def check(self):

        anon = get_initialized_session()

        _users = 3
        s = [get_initialized_session() for _ in range(_users)]
        u = [rnd_username() for _ in range(_users)]
        p = [rnd_password() for _ in range(_users)]

        _slaves = 2
        cheap_slaves = [self.mch._rnd_slave(rnd_string(10), 0, 3) for _ in range(_slaves)]
        expensive_slaves = [self.mch._rnd_slave(rnd_string(10), 8, 9) for _ in range(_slaves)]

        for i in range(_users):
            self.mch.register(s[i], u[i], p[i])
            self.mch.login(s[i], u[i], p[i])

        self.mch.register(s[1], u[0], p[0], 'Такий користувач вже є')
        self.mch.login(s[1], u[0], rnd_password(), 'Mật khẩu không hợp lệ')
        self.mch.login(s[0], rnd_username(), p[0], 'Такога карыстальніка няма!')

        self.mch.get_self(anon, 'Ты с логином раз на раз выйди сначала')
        d = self.mch.get_self(s[0])
        self.assert_eq(d, {
            'ok': {
                'имя': u[0],
                'пароль': p[0],
                'баланс': 5,
                'слейвы': []
            }
        }, 'Incorrect data on self data')

        d = self.mch.get_user(s[1], u[0])
        self.assert_eq(d, {
            'ok': {
                'имя': u[0],
                'баланс': 5,
                'слейвы': []
            }
        }, 'Incorrect data on user data')

        self.mch.get_user(anon, u[1], 'Ты с логином раз на раз выйди сначала')
        self.mch.get_user(s[0], rnd_username(), 'Такога карыстальніка няма!')

        self.mch.get_users(s[2])
        self.mch.get_users(anon, 'Ты с логином раз на раз выйди сначала')

        self.mch.catch_slave(s[2], cheap_slaves[0])
        d = self.mch.get_user(s[0], u[2])
        self.assert_eq(d, {
            'ok': {
                'имя': u[2],
                'баланс': 5,
                'слейвы': [{
                    **cheap_slaves[0],
                    'описание': '***',
                    'владелец': u[2],

                }]
            }
        }, "Can't catch slave")

        self.mch.catch_slave(anon, cheap_slaves[1], 'Ты с логином раз на раз выйди сначала')

        d = self.mch.get_self(s[2])
        self.assert_eq(d, {
            'ok': {
                'имя': u[2],
                'пароль': p[2],
                'баланс': 5,
                'слейвы': [{
                    **cheap_slaves[0],
                    'владелец': u[2],
                }]
            }
        }, "Can't catch slave")

        self.mch.send_money(s[0], u[1], randint(6, 100), 'ДЕНЕГ НЕТ, НО ВЫ ДЕРЖИТЕСЬ')
        self.mch.send_money(anon, u[2], randint(1, 5), 'Ты с логином раз на раз выйди сначала')
        send_cnt = randint(1, 2)
        self.mch.send_money(s[1], u[0], send_cnt)

        d = self.mch.get_self(s[0])
        self.assert_eq(d, {
            'ok': {
                'имя': u[0],
                'пароль': p[0],
                'баланс': 5 + send_cnt,
                'слейвы': []
            }
        }, "Can't send money")

        d = self.mch.get_user(s[0], u[1])
        self.assert_eq(d, {
            'ok': {
                'имя': u[1],
                'баланс': 5 - send_cnt,
                'слейвы': []
            }
        }, "Can't send money")

        self.mch.catch_slave(s[1], cheap_slaves[1])
        self.mch.catch_slave(s[1], expensive_slaves[0])
        self.mch.catch_slave(s[1], expensive_slaves[1])

        d = self.mch.get_self(s[1])
        self.assert_eq(d, {
            'ok': {
                'имя': u[1],
                'пароль': p[1],
                'баланс': 5 - send_cnt,
                'слейвы': [{
                    **cheap_slaves[1],
                    'владелец': u[1],
                }, {
                    **expensive_slaves[0],
                    'владелец': u[1],
                }, {
                    **expensive_slaves[1],
                    'владелец': u[1],
                }]
            }
        }, "Can't catch slave")

        self.mch.trade_slave(s[1], u[2], cheap_slaves[1]['имя'])
        self.mch.trade_slave(s[1], u[0], expensive_slaves[0]['имя'])
        self.mch.trade_slave(s[2], u[1], rnd_username(), 'Такого слейва нема')
        self.mch.trade_slave(anon, u[2], cheap_slaves[0]['имя'], 'Ты с логином раз на раз выйди сначала')

        self.mch.trade_accept(s[2], u[1], cheap_slaves[1]['имя'])
        d = self.mch.get_self(s[2])
        self.assert_eq(d, {
            'ok': {
                'имя': u[2],
                'пароль': p[2],
                'баланс': 5 - cheap_slaves[1]['цена'],
                'слейвы': [{
                    **cheap_slaves[0],
                    'владелец': u[2],
                }, {
                    **cheap_slaves[1],
                    'владелец': u[1],
                }]
            }
        }, "Can't accept trade")

        self.mch.trade_accept(s[0], u[1], expensive_slaves[0]['имя'], 'Налево пойдешь - целковый найдешь')
        self.mch.trade_accept(s[0], u[1], rnd_username(), 'Короче, Меченый, я тебя спас и в благородство играть не буду: выполнишь для меня пару заданий — и мы в расчете')
        self.mch.trade_accept(anon, u[0], cheap_slaves[0]['имя'], 'Ты с логином раз на раз выйди сначала')

        self.cquit(Status.OK)

    def put(self, flag_id, flag, vuln):

        s = get_initialized_session()
        u = rnd_username()
        p = rnd_password()
        slave = self.mch._rnd_slave(flag, 1, 4)

        self.mch.register(s, u, p)
        self.mch.login(s, u, p)

        self.mch.catch_slave(s, slave)

        self.cquit(Status.OK, json.dumps({'user': u, 'slave': slave['имя']}), json.dumps({
            'user': u,
            'password': p,
            'slave': slave
        }))

    def get(self, flag_id, flag, vuln):

        s_receiver = get_initialized_session()
        s_sender = get_initialized_session()

        d = json.loads(flag_id)
        u_sender = d['user']
        p_sender = d['password']
        slave = d['slave']

        u_receiver = rnd_username()
        p_receiver = rnd_password()

        self.mch.register(s_receiver, u_receiver, p_receiver)
        self.mch.login(s_receiver, u_receiver, p_receiver)

        self.mch.login(s_sender, u_sender, p_sender, status=Status.CORRUPT)
        self.mch.trade_slave(s_sender, u_receiver, slave['имя'], status=Status.CORRUPT)
        self.mch.trade_accept(s_receiver, u_sender, slave['имя'], status=Status.CORRUPT)

        d = self.mch.get_self(s_receiver)

        self.assert_eq(d, {
            'ok': {
                'имя': u_receiver,
                'пароль': p_receiver,
                'баланс': 5 - slave['цена'],
                'слейвы': [{
                    **slave,
                    'владелец': u_sender,
                }]
            }
        }, "Can't accept trade")

        self.cquit(Status.OK)


if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
