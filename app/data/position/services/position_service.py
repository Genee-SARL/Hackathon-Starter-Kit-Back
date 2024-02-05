from data.position.models import PositionModel
from data.position.schemas import PositionSchema
from shared import db
import datetime
import json


def create_position(position_data, trader_id, user_id):
    try:
        new_position = PositionModel(
            id_order=position_data['id_order'],
            id_trader=trader_id,
            user_id=user_id,
            time=position_data['time'],
            type=position_data['type'].upper(),
            symbol=position_data['symbol'],
            volume=position_data['volume']
        )
        db.session.add(new_position)
        db.session.commit()
        return {'message': 'Position successfully created'}, 200
    except Exception as e:
        return {'message': str(e)}, 400


def get_position(id_order):
    position = PositionModel.query.get(id_order)
    if position:
        position_dict = position.__dict__
        del position_dict['_sa_instance_state']
        return position_dict, 200
    else:
        return {'message': 'Position not found'}, 404


def get_positions_by_user_and_trader(user_id, trader_position, id_trader):
    positions = PositionModel.query.filter(
        PositionModel.user_id == user_id,
        PositionModel.id_trader == id_trader,
        PositionModel.time == trader_position.time,
        PositionModel.type == trader_position.type,
        PositionModel.symbol == trader_position.symbol
    ).all()
    if positions:
        position_schema = PositionSchema(many=True)
        return position_schema.dump(positions), 200
    else:
        return {'message': 'No positions found'}, 404


def remove_position(id_order):
    position = PositionModel.query.get(id_order)
    if position:
        db.session.delete(position)
        db.session.flush()
        db.session.commit()
        return {'message': 'Position successfully deleted'}, 200
    else:
        return {'message': 'Position not found'}, 404
