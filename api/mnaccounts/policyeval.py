from collections import namedtuple

from . import _policyeval_builtins
_globals = {
    '__builtins__': _policyeval_builtins
}

_request_selected_attributes = ('method', 'path', 'args', 'json')
Request = namedtuple('Request', _request_selected_attributes)

_user_selected_attributes = ('id', 'login', 'email', 'is_active', 'is_anonymous')
User = namedtuple('User', _user_selected_attributes)

def _policy_eval(user_, req_, tag_, pred_):
    user = User(*(getattr(user_, i) for i in _user_selected_attributes))
    req = Request(*(getattr(req_, i) for i in _request_selected_attributes))
    res = eval(pred_, _globals, {'user': user, 'req': req})
    assert type(res) is bool
    return tag_, res
