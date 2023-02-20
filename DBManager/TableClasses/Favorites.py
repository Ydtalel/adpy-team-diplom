import sqlalchemy as sa
from DBManager.DeclarativeBase import DeclarativeBase


class Favorite(DeclarativeBase.Base):
    __tablename__ = "users_favorites"
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.user_id"), nullable=False, primary_key=True)
    user_fav_id = sa.Column(sa.Integer, sa.ForeignKey("users.user_id"), nullable=False, primary_key=True)
