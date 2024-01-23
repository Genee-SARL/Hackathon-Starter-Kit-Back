from datetime import datetime

from data.position.enums import PositionTypeEnum
from data.trader.models import TraderModel, TraderPositionModel
from shared import db
from sqlalchemy.orm import joinedload

import sys


def get_all_traders_id():
    all_traders = db.session.query(TraderModel).all()
    return all_traders


def get_all_position_from_trader(trader_id):
    trader_with_positions = (
        db.session.query(TraderModel)
        .filter(TraderModel.id_trader == trader_id)
        .options(joinedload(TraderModel.positions))
        .first()
    )

    positions = [
        {
            "Symbol": position.symbol,
            "Time": position.time.strftime("%Y.%m.%d %H:%M"),
            "Type": "Buy" if position.type == PositionTypeEnum.BUY else "Sell",
            "Volume": str(position.volume),
        }
        for position in trader_with_positions.positions
    ]

    return positions


def post_new_position(trader_id, position):
    print(f"Adding new position for trader {trader_id} Position {position}", file=sys.stderr)
    new_position = TraderPositionModel(
        id_trader=trader_id,
        time=position["Time"],
        type=position["Type"].upper(),
        symbol=position["Symbol"],
        volume=position["Volume"],
    )

    db.session.add(new_position)
    db.session.flush()
    db.session.commit()


def remove_position(trader_id, position):
    print(f"Removing position for trader {trader_id} Position {position}", file=sys.stderr)
    position_to_remove = (
        db.session.query(TraderPositionModel)
        .filter(
            TraderPositionModel.id_trader == trader_id,
            TraderPositionModel.time == position.time,
            TraderPositionModel.type == position.type.name,
            TraderPositionModel.symbol == position.symbol,
        )
        .first()
    )

    if position_to_remove is not None:
        db.session.delete(position_to_remove)
        db.session.commit()


def register_daily_drowdown_anchor(trader_id, drowdown):
    print(f"Registering daily drowdown anchor for trader {trader_id} Drowdown {drowdown}", file=sys.stderr)
    db.session.query(TraderModel).filter(TraderModel.id_trader == trader_id).update(
        {TraderModel.daily_drawdown_anchor: drowdown, TraderModel.date_updated: datetime.utcnow()}
    )
    db.session.commit()


def register_daily_drowdown(trader_id, drowdown):
    db.session.query(TraderModel).filter(TraderModel.id_trader == trader_id).update(
        {
            TraderModel.daily_drawdown: drowdown,
        }
    )
    db.session.commit()
