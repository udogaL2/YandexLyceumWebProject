import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Project(SqlAlchemyBase):
    __tablename__ = 'Projects'

    id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    author = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    directory = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    img_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    min_disc = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    full_disc = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    condition = sqlalchemy.Column(sqlalchemy.String, nullable=True)
