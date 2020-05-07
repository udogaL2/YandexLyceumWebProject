from data import db_session
from data.users import User


def check_form(form):
    login = form['login']
    email = form['email']
    password1 = form['password1']
    password2 = form['password2']

    session = db_session.create_session()

    if login == '':
        session.commit()
        return False, 'login_400'

    elif password1 == '' or password2 == '':
        session.commit()
        return False, 'password_400'

    elif session.query(User).filter(User.login == login).first():
        session.commit()
        return False, 'login_406'

    elif session.query(User).filter(User.email == email).first():
        session.commit()
        return False, 'email_406'

    elif password1 != password2:
        session.commit()
        return False, 'password_406'

    elif email:
        if '@' not in email:
            session.commit()
            return False, 'email_400'

    session.commit()
    return True, 'ok_200'
