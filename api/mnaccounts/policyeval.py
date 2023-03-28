from collections import namedtuple

from . import _policyeval_builtins
_globals = {
    '__builtins__': _policyeval_builtins
}

_request_selected_attributes = ('method', 'path')

Rec = namedtuple('Rec', _request_selected_attributes)


def _policy_eval(req_, tag_, pred_):
    req = Rec(*(getattr(req_, i) for i in _request_selected_attributes))
    res = eval(pred_, _globals, {'req': req})
    assert type(res) is bool
    return tag_, res
