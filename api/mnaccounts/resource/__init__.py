"""Base Resource."""

def mnerror(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except SQLAlchemyError as e:
            raise
            abort(400, msg=str(e))

    return wrapper


def mnaccess_policy(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        policy = current_user.get_policy()
        if policy:
            action = policy_action(flask.request, policy)
            if action == 'reject':
                res = {
                    'msg': 'mnPolicyAccess',
                    'args': [current_user.login],
                }
                return res, 403

            elif action == 'null':
                res = {
                    'data': None,
                }
                return res, 200

            else:
                return f(*args, **kwargs)
        else:
            return f(*args, **kwargs)

    return wrapper
