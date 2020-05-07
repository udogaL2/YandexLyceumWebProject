from data import db_session
from data.users import User


def reg_user(form):
    session = db_session.create_session()

    user = User(
        login=form['login'],
        email=form['email'],
        title='user'
    )

    user.set_password(form['password1'])
    session.add(user)
    session.commit()

    return True, 'created_201'
