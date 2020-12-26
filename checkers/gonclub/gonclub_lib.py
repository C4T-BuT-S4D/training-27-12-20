from checklib import *
import requests

PORT = 9990


class CheckMachine:
    @property
    def url(self):
        return f'http://{self.c.host}:{self.port}'

    @property
    def api_url(self):
        return f'{self.url}/'

    def __init__(self, c: BaseChecker):
        self.c = c
        self.port = PORT

    def register_user(self, username=None, password=None):
        username = username or rnd_username()
        password = password or rnd_password()

        sess = self.c.get_initialized_session()

        r = sess.post(f'{self.url}/zaregatsya', json={'имя': username, 'пароль': password})
        self.c.check_response(r, 'Could not register')
        return username, password, sess

    def login_user(self, username, password):
        sess = self.c.get_initialized_session()
        r = sess.post(f'{self.url}/vhod', json={'имя': username, 'пароль': password})
        self.c.check_response(r, 'Could not login')
        return sess

    def create_club(self, sess: requests.Session, title, password='', jobf=''):
        data = {'название': title, 'пароль': password, 'профессия': jobf}
        r = sess.post(f'{self.url}/novklub', json=data)
        self.c.check_response(r, 'Could not create club')
        return self.c.get_json(r, 'Could not create club')

    def list_latest_clubs(self, sess:requests.Session):
        r = sess.get(f'{self.url}/klybi')
        self.c.check_response(r, 'Could not get latest clubs')
        return self.c.get_json(r, 'Could not get latest clubs')

    def join_club(self, sess:requests.Session, club_id, password=''):
        data = {'клуб': club_id, 'пароль': password}
        r = sess.post(f'{self.url}/vstupit', json=data)
        self.c.check_response(r, 'Could not join club')
        return self.c.get_json(r, 'Could not join club')

    def list_user_clubs(self, sess:requests.Session):
        r = sess.get(f'{self.url}/moikluby')
        self.c.check_response(r, 'Could not get user clubs')
        return self.c.get_json(r, 'Could not get user clubs')

    def get_club_info(self, sess:requests.Session, club_id):
        r = sess.get(f'{self.url}/chezaklub', params={'клид': club_id})
        self.c.check_response(r, 'Could not find club by id')
        return self.c.get_json(r, 'Could not find club by id')
