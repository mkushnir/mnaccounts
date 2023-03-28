import re

from .policyeval import _policy_eval

_re_policy = re.compile(r'(.+?)\s+(accept|reject|null);', re.DOTALL)

_final = ('accept', 'reject', 'null')

def policy_parse(s):
    items = _re_policy.findall(s)
    return items


def policy_eval_all(req, preds):
    return all(_policy_eval(req, i) for i in preds)


def policy_action(req, policy):
    items = policy_parse(policy)
    for idx, (pred, action) in enumerate(items):

        res = _policy_eval(req, pred.strip())
        if res:
            return action
