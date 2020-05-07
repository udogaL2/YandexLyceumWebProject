import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash  # генерация паролей

from .db_session import SqlAlchemyBase


# Марсиане
class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'Users'  # создаем имя будующе таблицы
    # #создаем столбцы таблицы
    id = sqlalchemy.Column(sqlalchemy.Integer, unique=True,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f'{self.login}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def is_admin(self) -> bool:
        return True if self.title == 'admin' else False
