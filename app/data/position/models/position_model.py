from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from data.position.enums import PositionTypeEnum
from shared import db


class PositionModel(db.Model):
    __tablename__ = 'position'
    id_order = Column(String, primary_key=True, unique=True)
    id_trader = Column(String, ForeignKey('trader.id_trader'), primary_key=True, nullable=False)
    user_id = Column(String, ForeignKey('user.id_user'), nullable=False)
    time = Column(DateTime, primary_key=True, nullable=False)
    type = Column(Enum(PositionTypeEnum), primary_key=True, nullable=False)
    symbol = Column(String, primary_key=True, nullable=False)
    volume = Column(Float, nullable=False)

    user_position = relationship("UserModel", back_populates="positions", lazy='joined', post_update=True)
