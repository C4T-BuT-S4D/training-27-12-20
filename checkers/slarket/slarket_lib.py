import requests
from checklib import rnd_string, rnd_username, rnd_password, Status
from random import randint

PORT = 3001

class CheckMachine:
    @property
    def url(self):
        return f'http://{self.c.host}:{self.port}/rychka'

    def __init__(self, checker):
        self.c = checker
        self.port = PORT
        self._costs = ["ноль", "целковый", "чекушка", "порнушка", "пердушка", "засирушка", "жучок", "мудачок", "хуй на воротничок", "дурачок"]

    def _cost_convert(self, cost):
        return self._costs[cost]

    def _cost_unconvert(self, cost):
        return self._costs.index(cost)


    def _rnd_slave(self, desc, l, r):
        slave = {
            "имя": rnd_username(),
            "описание": desc,
            "цена": randint(l, r),
        }

        for i in range(randint(0, 5)):
            if randint(0, 1) == 0:
                k = rnd_string(5)
                v = rnd_string(10)
                slave[k] = v
            else:
                k = rnd_string(5)
                subslave = {}
                for j in range(randint(1, 3)):
                    ks = rnd_string(4)
                    vs = rnd_string(15)
                    subslave[ks] = vs
                slave[k] = subslave

        return slave

    def _check_ok(self, d, errmsg, status):
        self.c.assert_eq(type(d), type({}), errmsg, status)
        self.c.assert_in("ok", d, errmsg, status)

    def _check_err(self, d, err, errmsg, status):
        self.c.assert_eq(type(d), type({}), errmsg, status)
        self.c.assert_in("err", d, errmsg, status)
        self.c.assert_eq(type(d["err"]), type(""), errmsg, status)
        self.c.assert_eq(d["err"], err, errmsg, status)

    def _check_master_pub(self, d, errmsg, status):
        self.c.assert_eq(type(d), type({}), errmsg, status)

        self.c.assert_in("имя", d, errmsg, status)
        self.c.assert_eq(type(d["имя"]), type(""), errmsg, status)
        self.c.assert_in("баланс", d, errmsg, status)
        self.c.assert_eq(type(d["баланс"]), type(0), errmsg, status)
        self.c.assert_in("слейвы", d, errmsg, status)
        self.c.assert_eq(type(d["слейвы"]), type([]), errmsg, status)

    def _check_master_priv(self, d, errmsg, status):
        self._check_master_pub(d, errmsg, status)
        self.c.assert_in("пароль", d, errmsg, status)
        self.c.assert_eq(type(d["пароль"]), type(""), errmsg, status)

    def _check_dict_all_str(self, d, errmsg, exclude, status):
        self.c.assert_eq(type(d), type({}), errmsg, status)

        for k, v in d.items():
            self.c.assert_eq(k, type(""), errmsg, status)
            if k in exclude:
                continue
            if type(v) == type({}):
                self._check_dict_all_str(d, errmsg, [], status)
            else:
                self.c.assert_eq(v, type(""), errmsg, status)


    def _check_slave(self, d, errmsg, status):
        self.c.assert_eq(type(d), type({}), errmsg, status)

        self.c.assert_in("владелец", d, errmsg, status)
        self.c.assert_eq(d["владелец"], type(""), errmsg, status)
        self.c.assert_in("имя", d, errmsg, status)
        self.c.assert_eq(d["имя"], type(""), errmsg, status)
        self.c.assert_in("описание", d, errmsg, status)
        self.c.assert_eq(d["описание"], type(""), errmsg, status)
        self.c.assert_in("цена", d, errmsg, status)
        self.c.assert_eq(d["цена"], type(0), errmsg, status)

        self._check_dict_all_str(d, errmsg, ["владелец", "имя", "описание", "цена"], status)

    def register(self, s, u, p, err=None, status=Status.MUMBLE):
        url = f"{self.url}/registraciya"

        r = s.post(url, json={
            "ктоНахуй": u,
            "пароль": p,
        })

        d = self.c.get_json(r, "Can't register", status)
        if err is None:
            self._check_ok(d, "Incorrect register response", status)
        else:
            self._check_err(d, err, "Incorrect register response", status)

    def login(self, s, u, p, err=None, status=Status.MUMBLE):
        url = f'{self.url}/login'

        r = s.post(url, json={
            'ктоНахуй': u,
            'пароль': p,
        })

        d = self.c.get_json(r, "Can't login", status)
        if err is None:
            self._check_ok(d, "Incorrect login response", status)
        else:
            self._check_err(d, err, "Incorrect login error", status)

    def get_self(self, s, err=None, status=Status.MUMBLE):
        url = f'{self.url}/polzovateli/ya'

        r = s.get(url)

        d = self.c.get_json(r, "Can't login", status)
        if err is None:
            self._check_ok(d, "Incorrect response on self data", status)
            self._check_master_priv(d["ok"], "Incorrect response on self data", status)
        else:
            self._check_err(d, err, "Incorrect error on self data", status)
        return d

    def get_user(self, s, u, err=None, status=Status.MUMBLE):
        url = f'{self.url}/polzovateli/{u}'

        r = s.get(url)

        d = self.c.get_json(r, "Can't get user", status)
        if err is None:
            self._check_ok(d, "Incorrect response on user data", status)
            self._check_master_pub(d["ok"], "Incorrect response on user data", status)
        else:
            self._check_err(d, err, "Incorrect error on user data", status)
        return d

    def get_users(self, s, err=None, status=Status.MUMBLE):
        url = f'{self.url}/polzovateli'

        r = s.get(url)

        d = self.c.get_json(r, "Can't get users", status)
        if err is None:
            self._check_ok(d, "Incorrect response on user list", status)
            self.c.assert_eq(type(d["ok"]), type([]), "Incorrect response on user list", status)
            for u in d["ok"]:
                self._check_master_pub(u, "Incorrect response on user list", status)
        else:
            self._check_err(d, err, "Incorrect error on user list", status)
        return d

    def catch_slave(self, s, slave, err=None, status=Status.MUMBLE):
        url = f'{self.url}/sleiv/poimat'

        r = s.post(url, json={
            **slave,
            'цена': self._cost_convert(slave['цена']),
            'ценаЛовить': True,
        })
        d = self.c.get_json(r, "Can't catch slave", status)
        if err is None:
            self._check_ok(d, "Incorrect response on catch slave", status)
        else:
            self._check_err(d, err, "Incorrect error on catch slave", status)

    def trade_slave(self, s, receiver_name, slave_name, err=None, status=Status.MUMBLE):
        url = f'{self.url}/sleiv/torganut'

        r = s.post(url, json={
            "кого": slave_name,
            "кому": receiver_name,
        })

        d = self.c.get_json(r, "Can't trade slave", status)
        if err is None:
            self._check_ok(d, "Incorrect response on trade slave", status)
        else:
            self._check_err(d, err, "Incorrect error on trade slave", status)

    def trade_accept(self, s, sender_name, slave_name, err=None, status=Status.MUMBLE):
        url = f'{self.url}/torg/prinyat'

        r = s.post(url, json={
            "кого": slave_name,
            "отКого": sender_name,
        })

        d = self.c.get_json(r, "Can't accept trade", status)
        if err is None:
            self._check_ok(d, "Incorrect response on accept trade", status)
        else:
            self._check_err(d, err, "Incorrect error on accept trade", status)

    def send_money(self, s, receiver_name, amount, err=None, status=Status.MUMBLE):
        url = f'{self.url}/babosi/otpravit'

        r = s.post(url, json={
            "куда": receiver_name,
            "сколько": amount,
        })

        d = self.c.get_json(r, "Can't send money", status)
        if err is None:
            self._check_ok(d, "Incorrect response on send money", status)
        else:
            self._check_err(d, err, "Incorrect error on send money", status)
