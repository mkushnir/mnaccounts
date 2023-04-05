import re

from .policyeval import _policy_eval

_re_policy = re.compile(r'(\S+)\s+(.+?)\s+(accept|reject|null)\s*;', re.DOTALL)

_final = ('accept', 'reject', 'null')

def policy_parse(s):
    items = _re_policy.findall(s)
    return items


def policy_eval_all(req, preds):
    return all(_policy_eval(req, i) for i in preds)


def policy_action(user, req, policy, tag_selector=None):
    items = policy_parse(policy)
    for idx, (tag, pred, action) in enumerate(items):
        tag_ = tag.strip()

        if tag_selector is not None and not tag_ in tag_selector:
            continue

        tag, res = _policy_eval(user, req, tag.strip(), pred.strip())
        if res:
            return idx, tag, action

    return None, None, None
