from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.orm import relationship
from shared import db
from data.group.models import group_user_association
from data.position.models import PositionModel


class UserModel(db.Model):
    __tablename__ = 'user'
    id_user = Column(String, primary_key=True, unique=True)
    username = Column(String, nullable=True)
    password = Column(String, nullable=False)
    server = Column(String, nullable=False)
    multiplier = Column(Float, nullable=False)
    batch_size_min = Column(Float, nullable=False)
    batch_size_max = Column(Float, nullable=False)
    initial_balance = Column(Float, nullable=False)
    actual_balance = Column(Float, nullable=True, default=0)
    daily_balance = Column(Float, nullable=True, default=0)
    symbol_extension = Column(String, nullable=True, default="")

    positions = relationship("PositionModel", back_populates="user_position", lazy='joined', post_update=True)
    user_groups = relationship("GroupModel", secondary=group_user_association, back_populates="users")
