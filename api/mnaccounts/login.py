from flask_login import LoginManager, login_user
from flask_bcrypt import Bcrypt


login_manager = LoginManager()
bcrypt = None


def _account():
    pass


def init(app):
    global bcrypt

    login_manager.init_app(app)

    app.add_url_rule(
        '/account',
        view_func=_account,
        methods=['GET', 'POST', 'DELETE'])

    bcrypt = Bcrypt(app)
