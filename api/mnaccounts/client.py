import os
import pickle
import json
from urllib.parse import urlparse

import requests
from requests.auth import AuthBase

from .account import bcrypt



class MNAccountClient:
    """"""
    def __init__(self, base_url):
        self._session = requests.Session()
        self._base_url = base_url

    def _api_call(self, method, endpoint, params=None, data=None):
        headers = {
            'Accept': 'application/json',
        }

        if data is not None:
            headers['Content-Type'] = 'application/json'

        url = '{}{}'.format(self._base_url, endpoint)

        response = self._session.request(
            method,
            url,
            params=params,
            headers=headers,
            json=data)

        if response.status_code == 200:
            data = response.json()
            return data['data']

        elif response.status_code == 304:
            return None

        else:
            data = response.json()
            raise Exception('api failure: code {} data {}'.format(
                response.status_code, data))

    def account_get(self, ticket, login, target):
        params = {
            'ticket': ticket,
            'login': login,
            'target': target,
        }

        return self._api_call('get', '/account', params=params)

    def account_post(self, login, password, target):
        data = {
            'login': login,
            'password': password,
            'target': target,
        }

        return self._api_call('post', '/account', data=data)

    def account_delete(self, ticket):
        data = {
            'ticket': ticket,
        }

        return self._api_call('delete', '/account', data=data)


class _HTTPAPIKeyAuth(AuthBase):
    def __init__(self, token):
        self._token = token

    def __eq__(self, other):
        return self._token == getattr(other, '_token', None)

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        r.headers['Authorization'] = 'apikey {}'.format(self._token)
        return r


class _HTTPBearerAuth(AuthBase):
    def __init__(self, token):
        self._token = token

    def __eq__(self, other):
        return self._token == getattr(other, '_token', None)

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer {}'.format(self._token)
        return r


class MNAccountAPIClient:
    """"""
    _session_cookie_file = '.mnaccountapiclient.cookie'
    # copy-paste form PNDLMEArchiveClient

    def __init__(self, auth_url, creds):
        self._session = requests.Session()

        if os.path.exists(self._session_cookie_file):
            with open(self._session_cookie_file, 'rb') as f:
                saved_cookie = pickle.load(f)
                self._session.cookies.update(saved_cookie)

        self._auth_url = auth_url
        self._creds = creds
        self._login()
        self._discover_api_url()

    def _call(self, url, method, endpoint, params=None, data=None, retry_on_401=True):
        headers = {
            'Accept': 'application/json',
        }

        if data is not None:
            headers['Content-Type'] = 'application/json'

        url = '{}{}'.format(url, endpoint)

        response = self._session.request(
            method,
            url,
            params=params,
            headers=headers,
            json=data,
            cookies=self._session.cookies)

        with open(self._session_cookie_file, 'wb') as f:
            pickle.dump(self._session.cookies, f)

        if response.status_code == 200:
            return response.json()

        elif response.status_code == 304:
            return None

        elif response.status_code == 401:
            if retry_on_401:
                self._login(force=True)
                return self._call(
                    url, method, endpoint, params, data, retry_on_401=False)
            else:
                res = response.json()
                raise Exception('api failure: code {} data {}'.format(
                    response.status_code, res))

        else:
            res = response.json()
            raise Exception('api failure: code {} data {}'.format(
                response.status_code, res))

    def _auth_call(self, method, endpoint, params=None, data=None, retry_on_401=True):
        return self._call(self._auth_url, method, endpoint, params, data, retry_on_401)

    def _api_call(self, method, endpoint, params=None, data=None, retry_on_401=True):
        return self._call(self._api_url, method, endpoint, params, data, retry_on_401)

    def _login(self, force=False):
        if ('session' in self._session.cookies) and not force:
            return

        data = {
            'login': self._creds[0],
            'password': self._creds[1],
            'target': self._creds[2],
        }

        self._auth_call('post', '/account', data=data)

    def _discover_api_url(self):
        tmpurl = urlparse(self._auth_url)
        self._api_url = '{}://{}'.format(tmpurl.scheme, tmpurl.netloc)
        data = self.api_user_get(login=self._creds[0])
        user = data[0]
        data = self.api_user_target_get(user_id=user['id'])
        t = [i for i in data if i['label'] == self._creds[2]]
        url = urlparse(t[0]['url'])
        self._api_url = '{}://{}'.format(url.scheme, url.netloc)

    def api_version(self):
        res = self._api_call('get', '/v1/version')
        return res['data']

    def api_init(self):
        res = self._api_call('put', '/v1/init')
        return res['data']

    # user
    def api_user_get(self, user_id=None, login=None):
        if user_id is not None:
            res = self._api_call('get', '/v1/user/{}'.format(user_id))
        else:
            params = {}
            if login is not None:
                params['user.login'] = login
            res = self._api_call('get', '/v1/user', params)
        return res['data']

    def api_user_post(self, data):
        res = self._api_call('post', '/v1/user', data=data)
        return res['data']

    def api_user_put(self, data):
        res = self._api_call('put', '/v1/user/{}'.format(data['id']), data=data)
        return res['data']

    def api_user_delete(self, user_id):
        res = self._api_call('delete', '/v1/user/{}'.format(user_id))
        return res['data']

    # target
    def api_target_get(self, target_id=None):
        if target_id is not None:
            res = self._api_call('get', '/v1/target/{}'.format(target_id))
        else:
            res = self._api_call('get', '/v1/target')
        return res['data']

    def api_target_post(self, data):
        res = self._api_call('post', '/v1/target', data=data)
        return res['data']

    def api_target_put(self, data):
        res = self._api_call('put', '/v1/target/{}'.format(data['id']), data=data)
        return res['data']

    def api_target_delete(self, target_id):
        res = self._api_call('delete', '/v1/target/{}'.format(target_id))
        return res['data']

    # policy
    def api_policy_get(self, policy_id=None):
        if policy_id is not None:
            res = self._api_call('get', '/v1/policy/{}'.format(policy_id))
        else:
            res = self._api_call('get', '/v1/policy')
        return res['data']

    def api_policy_post(self, data):
        res = self._api_call('post', '/v1/policy', data=data)
        return res['data']

    def api_policy_put(self, data):
        res = self._api_call('put', '/v1/policy/{}'.format(data['id']), data=data)
        return res['data']

    def api_policy_delete(self, policy_id):
        res = self._api_call('delete', '/v1/policy/{}'.format(policy_id))
        return res['data']

    # user_target_policy
    def api_user_target_policy_get(self, user_target_policy_id=None):
        if user_target_policy_id is not None:
            res = self._api_call('get', '/v1/user_target_policy/{}'.format(user_target_policy_id))
        else:
            res = self._api_call('get', '/v1/user_target_policy')
        return res['data']

    def api_user_target_policy_post(self, data):
        res = self._api_call('post', '/v1/user_target_policy', data=data)
        return res['data']

    def api_user_target_policy_put(self, data):
        res = self._api_call('put', '/v1/user_target_policy/{}'.format(data['id']), data=data)
        return res['data']

    def api_user_target_policy_delete(self, user_target_policy_id):
        res = self._api_call('delete', '/v1/user_target_policy/{}'.format(user_target_policy_id))
        return res['data']

    # user_target
    def api_user_target_get(self, user_id=None):
        params = {}
        if user_id is not None:
            params['user.id'] = user_id
        res = self._api_call('get', '/v1/user_target', params=params)
        return res['data']

    def api_user_target_policy_post(self, data):
        res = self._api_call('post', '/v1/user_target_policy', data=data)
        return res['data']

    def api_user_target_policy_put(self, data):
        res = self._api_call('put', '/v1/user_target_policy/{}'.format(data['id']), data=data)
        return res['data']

    def api_user_target_policy_delete(self, user_target_policy_id):
        res = self._api_call('delete', '/v1/user_target_policy/{}'.format(user_target_policy_id))
        return res['data']
