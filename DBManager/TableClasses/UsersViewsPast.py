import sqlalchemy as sa
from DBManager.DeclarativeBase import DeclarativeBase

class UsersViewPast(DeclarativeBase.Base):
    __tablename__ = "users_views_past"
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.user_id"), nullable=False, primary_key=True)
    user_viewpast_vkid = sa.Column(sa.String, nullable=False, primary_key=True)
