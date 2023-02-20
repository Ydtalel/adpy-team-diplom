import sqlalchemy as sa
from DBManager.DeclarativeBase import DeclarativeBase


class User(DeclarativeBase.Base):
    __tablename__ = "users"
    user_id = sa.Column(sa.Integer, primary_key=True)
    user_vk_id = sa.Column(sa.VARCHAR(128), nullable=False)
    name = sa.Column(sa.VARCHAR(256), nullable=False)
    city = sa.Column(sa.Integer)
    gender = sa.Column(sa.Integer, nullable=False)
    age = sa.Column(sa.Integer, nullable=False)
