from data import db_session
from data.users import User
from werkzeug.security import generate_password_hash


def check_user(form):
    login = form['login']
    password = form['password']

    session = db_session.create_session()

    user = session.query(User).filter(User.login == login).first()
    session.commit()

    if user:
        if user.check_password(password):
            return True, user, 'ok_200'
        else:

            return False, 'error_404'
    else:
        return False, 'error_404'
