from datetime import datetime

from data.position.enums import PositionTypeEnum
from data.trader.models import TraderModel, TraderPositionModel
from shared import db
from sqlalchemy.orm import joinedload
from data.trader.models import TraderModel
from data.trader.schemas import TraderSchema
from data.group.models import GroupModel
from flask import jsonify, make_response

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
            "Volume": "{:.2f}".format(float(position.volume)),
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
            TraderPositionModel.time == position['Time'],
            TraderPositionModel.type == position['Type'].upper(),
            TraderPositionModel.symbol == position['Symbol'],
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


def create_trader(payload):
    print(payload)
    trader_schema = TraderSchema()
    try:
        id_group = payload.pop('id_group', None)

        trader_data = trader_schema.load(payload)
        trader_id = trader_data.id_trader

        existing_trader = TraderModel.query.filter_by(id_trader=trader_id).first()
        if existing_trader:
            new_trader = existing_trader
        else:
            new_trader = trader_data
            db.session.add(new_trader)
            db.session.flush()
        if id_group:
            group = GroupModel.query.get(id_group)
            if group:
                if new_trader not in group.traders:
                    group.traders.append(new_trader)
            else:
                print(f"Warning: Group with id {id_group} not found")

        db.session.commit()

        response = jsonify({'message': 'Trader created or updated successfully'})
        return make_response(response, 201)
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")  # Print the exception message
        response = jsonify({'error': str(e)})
        return make_response(response, 400)


def remove_trader(id_trader, id_group):
    trader = TraderModel.query.get(id_trader)
    if trader:
        group = GroupModel.query.get(id_group)
        if group and trader in group.traders:
            group.traders.remove(trader)
            db.session.commit()

            if not trader.groups:
                db.session.delete(trader)
                db.session.commit()
                return jsonify({'message': 'Trader and associated data successfully deleted'}), 200
            else:
                return jsonify({'message': 'Trader removed from the group'}), 200
        else:
            return jsonify({'message': 'Group not found or Trader not in the group'}), 404
    else:
        return jsonify({'message': 'Trader not found'}), 404
