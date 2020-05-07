from data import db_session
from data.projects import Project
from flask_login import current_user
import os


def create_project(form, title_img, photo):
    title_img = title_img.read()
    photo = [i.read() for i in photo]
    session = db_session.create_session()
    if title_img == "b''" or photo[0] == "b''" or form['title'] == '' or form['comment'] == '' or\
            form['description'] == '':
        return False, 'project_404'

    elif not session.query(Project).filter(Project.name == form['title']).first():

        project = Project(
            name=form['title'],
            min_disc=' '.join(form['comment'].split('\n')),
            full_disc=form['description'],
            directory=form['title'],
            author=current_user.id,
            img_count=len(photo),
            condition='considers'
        )

        session.add(project)
        session.commit()

        os.mkdir(os.path.abspath(os.curdir) + '/static/projects/' + form['title'])

        with open(os.path.abspath(os.curdir) + f'/static/projects/{form["title"]}/{form["title"]}_title_img.jpg', 'wb') as r:
            r.write(title_img)
            r.close()

        for i in range(len(photo)):
            with open(os.path.abspath(os.curdir) + f'/static/projects/{form["title"]}/{form["title"]}_photo_' + str(i) + '.jpg', 'wb') as r:
                r.write(photo[i])
        r.close()

        return True, 'created_201'

    else:
        return False, 'project_406'
