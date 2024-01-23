
from sqlalchemy import Column, String, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from shared import db

class TraderModel(db.Model):
    __tablename__ = 'trader'
    id_trader = Column(String, primary_key=True, unique=True)
    date_updated = Column(DateTime, nullable=False, default=datetime.now)
    daily_drawdown_anchor = Column(Float, server_default='0')
    daily_drawdown = Column(Float, server_default='0')
    trader_url = Column(String, nullable=False)
    valid = Column(Boolean, nullable=False)
    positions = relationship("TraderPositionModel", back_populates="trader")

    @staticmethod
    def get_all_traders():
        return TraderModel.query.all()
