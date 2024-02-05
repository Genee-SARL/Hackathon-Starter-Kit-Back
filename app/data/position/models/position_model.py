from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from data.position.enums import PositionTypeEnum
from shared import db


class PositionModel(db.Model):
    __tablename__ = 'position'
    id_order = Column(String, primary_key=True, unique=True)
    id_trader = Column(String, ForeignKey('trader.id_trader'), nullable=False)
    user_id = Column(String, ForeignKey('user.id_user'), nullable=True)
    time = Column(DateTime, nullable=False)
    type = Column(Enum(PositionTypeEnum), nullable=False)
    symbol = Column(String, nullable=False)
    volume = Column(Float, nullable=False)

    user_position = relationship("UserModel", back_populates="positions", lazy='joined', post_update=True)
