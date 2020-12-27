#!/usr/bin/env python3
import json

from gevent import monkey, sleep

monkey.patch_all()

import sys
from random import randint, choice
import checklib

from gonclub_lib import *


class Checker(BaseChecker):
    uses_attack_data = True
    timeout = 20
    vulns = 2

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.mch = CheckMachine(self)

    def remap(self, l, key='id'):
        d = {}
        for v in l:
            d[v.get(key)] = v
        return d

    def check_response(self, r: requests.Response, public: str, status=checklib.status.Status.MUMBLE):
        try:
            error = r.json()['error']
        except Exception as e:
            error = r.text[:50]
        if r.status_code >= 500:
            self.cquit(status, public, f'Code {r.status_code} on {r.url}, error = {error}')
        if not r.ok:
            self.cquit(status, public, f'Error on {r.url}: {r.status_code}, error = {error}')

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except requests.exceptions.ConnectionError:
            self.cquit(Status.DOWN, 'Connection error', 'Got requests connection error')

    def check(self):
        u, p, _ = self.mch.register_user()
        sess = self.mch.login_user(u, p)

        club_name = rnd_string(20)
        password_or_jobf = rnd_string(7)
        club_resp = None
        new_username = rnd_username()
        club_password = ''
        if randint(0, 1) == 0:
            club_resp = self.mch.create_club(sess, club_name, jobf=password_or_jobf)
            new_username += password_or_jobf
        else:
            club_resp = self.mch.create_club(sess, club_name, password=password_or_jobf)
            club_password = password_or_jobf

        clubs = self.mch.list_latest_clubs(sess)
        club = self.remap(clubs, 'босс').get(u)
        self.assert_neq(club, None, 'Failed to find club in latest')
        self.assert_eq(club.get('название'), club_name, 'Failed to find club in latest')

        nu, np, usess = self.mch.register_user(new_username)
        self.mch.join_club(usess, club.get('ид'), club_password)

        u_clubs = self.mch.list_user_clubs(usess)
        club = self.remap(u_clubs, 'ид').get(club.get('ид'))
        self.assert_neq(club, None, 'Failed to find user club')
        self.assert_eq(club.get('босс'), u, 'Failed to find user club')

        infos = [
            self.mch.get_club_info(usess, club.get('ид')),
            self.mch.get_club_info(sess, club.get('ид'))
        ]
        for info in infos:
            self.assert_eq(info.get('босс'), u, 'Invalid club info returned')
            self.assert_eq(info.get('название'), club_name, 'Invalid club info returned')
            self.assert_in(u, info.get('участники', []), 'Invalid club info returned: failed to find user in participants')
            self.assert_in(nu, info.get('участники', []), 'Invalid club info returned: failed to find user in participants')

        self.cquit(Status.OK)

    def put(self, flag_id, flag, vuln):
        u, p, sess = self.mch.register_user()
        club_name = rnd_string(15)
        club_password = ''
        cu = ''
        cp = ''
        club_username_filter = ''
        if vuln == '1':
            cu = flag
            cp = rnd_password()
            club_password = rnd_string(20)
        else:
            cu = rnd_string(20)
            cp = flag
            club_username_filter = cu[:-2]

        club_resp = self.mch.create_club(sess, club_name, club_password, club_username_filter)
        club_id = club_resp.get('ид', '')
        self.assert_neq(club_id, '', 'Could not create club')
        _, _, csess = self.mch.register_user(cu, cp)
        self.mch.join_club(csess, club_resp.get('ид'), club_password)
        full_info = {
            'u': u,
            'p': p,
            'cu': cu,
            'cp': cp,
            'cid': club_id
        }
        self.cquit(Status.OK, f'{club_name}', json.dumps(full_info))

    def get(self, flag_id, flag, vuln):
        data = json.loads(flag_id)
        u, p, cu, cp, club_id = data['u'], data['p'], data['cu'], data['cp'], data['cid']
        sess = self.mch.login_user(u, p)
        info = self.mch.get_club_info(sess, club_id)
        self.assert_in(cu, info.get('участники', []), 'Invalid club info returned: failed to find user in participants',
                       status=Status.CORRUPT)
        client_sess = self.mch.login_user(cu, cp)
        info = self.mch.get_club_info(client_sess, club_id)
        self.assert_in(u, info.get('участники', []), 'Invalid club info returned: failed to find user in participants',
                       status=Status.CORRUPT)
        self.assert_in(cu, info.get('участники', []), 'Invalid club info returned: failed to find user in participants',
                       status=Status.CORRUPT)
        self.cquit(Status.OK)


if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
