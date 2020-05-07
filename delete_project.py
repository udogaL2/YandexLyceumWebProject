from data import db_session
from data.projects import Project
from flask_login import current_user
import os


def delete_project(id):
    session = db_session.create_session()
    res = session.query(Project).get(id)
    if current_user.id == res.id or current_user.title == 'admin':
        directory = os.path.abspath(os.curdir) + '/static/projects/' + res.directory
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            os.unlink(file_path)
        os.rmdir(directory)
        session.delete(res)
    session.commit()
