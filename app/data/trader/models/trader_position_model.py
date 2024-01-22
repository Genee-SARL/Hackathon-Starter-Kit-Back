from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from data.position.enums import PositionTypeEnum
from enum import Enum
from shared import db

class TraderPositionModel(db.Model):
    __tablename__ = 'trader_position'
    id_trader = Column(String, ForeignKey('trader.id_trader'), primary_key=True)
    time = Column(DateTime, primary_key=True, nullable=False)
    type = Column(Enum(PositionTypeEnum), primary_key=True, nullable=False)
    symbol = Column(String, primary_key=True, nullable=False)
    volume = Column(Float, server_default='0')
    opened = Column(Boolean, nullable=False, server_default='true')

    trader = relationship("TraderModel", back_populates="positions")