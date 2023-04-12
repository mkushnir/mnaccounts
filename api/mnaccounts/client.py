import os
import pickle
import json
from urllib.parse import urlsplit

from mnaclient.base import _MNAccountAPIClientBase



class MNAccountAPIClient(_MNAccountAPIClientBase):
    """"""
    def api_version(self):
        res = self._api_call('get', '/v1/version')
        return res['data']

    def api_init(self):
        res = self._api_call('put', '/v1/init')
        return res['data']

    def api_refresh(self):
        res = self._api_call('put', '/v1/refresh')
        return res['data']

    # user
    def api_user_get(self, user_id=None, login=None, apikey=None):
        if user_id is not None:
            res = self._api_call('get', '/v1/user/{}'.format(user_id))

        else:
            params = {}
            if login is not None:
                params['user.login'] = login

            elif apikey is not None:
                params['user.apikey'] = apikey

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
            params['user_id'] = user_id
        res = self._api_call('get', '/v1/user_target', params=params)
        return res['data']

    # usermanage
    def api_usermanage_put(self, user_id, data):
        res = self._api_call('put', '/v1/user/manage/{}'.format(user_id), data=data)
        return res['data']

    # policymanage
    def api_policymanage_put(self, policy_id=None, data=None):
        if policy_id is not None:
            res = self._api_call('put', '/v1/policy/manage/{}'.format(policy_id), data=data)
        else:
            res = self._api_call('put', '/v1/policy/manage', data=data)

        return res['data']
