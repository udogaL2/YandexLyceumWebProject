from flask import Flask, redirect, render_template, request, url_for, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session
import os

# Вспомогательные функции
from get_error import get_error
from check_form import check_form
from reg_user import reg_user
from check_log_form import check_user
from create_project import create_project
from get_projects import get_considers_projects, get_project, get_my_projects, get_published_projects
from delete_project import delete_project
from publish_project import publish_project

#
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/users.sqlite")


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.errorhandler(404)
def error(e):
    return render_template('404.html')


@app.route('/')
def transfer():
    return redirect('/home')


@app.route('/home')
def main():
    return render_template('home.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template('login.html', message='')
    elif request.method == 'POST':
        ans = check_user(request.form)
        if ans[0]:
            login_user(ans[1], remember=True)
            return redirect('/home')
        else:
            return render_template('login.html', message=get_error(ans[1]))


@app.route('/registration', methods=["POST", "GET"])
def register():
    if request.method == 'GET':
        return render_template('register.html', message='')
    elif request.method == 'POST':
        ans = check_form(request.form)
        if ans[0]:
            if reg_user(request.form)[0]:
                return redirect('/login')
        else:
            return render_template('register.html', message=get_error(ans[1]))


@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template('projects.html', projects=get_my_projects(), title='Мои проекты')
    else:
        return render_template('projects.html', projects=[], title='Мои проекты')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/create', methods=["POST", "GET"])
def create():
    if request.method == 'GET':
        return render_template('create_prct.html', message='')
    elif request.method == 'POST':
        title_img = request.files['title_img']
        photo = request.files.getlist('photo[]')

        ans = create_project(request.form, title_img, photo)
        if ans[0]:
            return redirect("/")
        else:
            return render_template('create_prct.html', message=get_error(ans[1]))


@app.route('/projects')
def projects():
    return render_template('projects.html', projects=get_published_projects(), title='Проекты')


@app.route('/project/<int:id>', methods=["POST", "GET"])
def project(id):
    if request.method == 'GET':
        project = get_project(id)
        if project:
            return render_template('project.html', project=project, author=load_user(project.author))
        else:
            return render_template('project.html', project=project)
    elif request.method == 'POST':
        if current_user.title == 'admin':
            publish_project(id)
        return redirect('/projects')


@app.route('/project/<project>/<int:img>')
def image(project, img):
    return f'''
            <img src="../../static/projects/{project}/{{project.directory}}_photo_{img}.jpg" alt="Изображение не найдено">
            '''


@app.route('/delete/<int:id>')
def delete(id):
    delete_project(id)
    return redirect('/home')


@app.route('/post')
def post():
    if current_user.is_authenticated:
        if current_user.title == 'admin':
            return render_template('projects.html', projects=get_considers_projects(), title='Публикация проектов')
        else:
            abort(404)
    else:
        abort(404)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
