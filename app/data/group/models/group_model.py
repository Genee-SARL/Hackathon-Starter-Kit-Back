from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from shared import db

from data.trader.models import TraderModel

group_user_association = Table('group_user', db.Model.metadata,
                               Column('group_id', String, ForeignKey('group.id_group')),
                               Column('user_id', String, ForeignKey('user.id_user'))
                               )

group_trader_association = Table('group_trader', db.Model.metadata,
                                 Column('group_id', String, ForeignKey('group.id_group')),
                                 Column('trader_id', String, ForeignKey('trader.id_trader'))
                                 )


class GroupModel(db.Model):
    __tablename__ = 'group'
    id_group = Column(String, primary_key=True, unique=True)
    ipaddress = Column(String, nullable=False)
    port = Column(String, nullable=False)

    users = relationship("UserModel", secondary=group_user_association, back_populates="user_groups", lazy='joined')
    traders = relationship("TraderModel", secondary=group_trader_association, backref="groups")