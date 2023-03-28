def _policy_eval(req, pred):
    res = eval(pred)
    assert type(res) is bool
    return res
