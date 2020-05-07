from data import db_session
from data.projects import Project
from flask_login import current_user


def publish_project(id):
    session = db_session.create_session()
    res = session.query(Project).get(id)
    if current_user.title == 'admin':
        res.condition = 'published'
    session.commit()
