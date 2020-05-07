from data import db_session
from data.projects import Project
from flask_login import current_user


def get_published_projects():
    session = db_session.create_session()
    res = session.query(Project).filter(Project.condition == 'published')
    session.commit()
    return res


def get_considers_projects():
    session = db_session.create_session()
    res = session.query(Project).filter(Project.condition == 'considers')
    session.commit()
    return res


def get_my_projects():
    session = db_session.create_session()
    res = session.query(Project).filter(Project.author == current_user.id)
    session.commit()
    return res


def get_project(id):
    session = db_session.create_session()
    res = session.query(Project).get(id)
    session.commit()
    return res
