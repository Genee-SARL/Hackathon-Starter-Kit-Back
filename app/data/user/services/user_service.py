import requests
import json
import datetime
from data.group.services import get_group_ip_by_user_id
from data.position.enums import PositionTypeEnum
from data.position.services import remove_position
from data.user.models import UserModel
from data.user.schemas import UserSchema
from shared import db
from flask import jsonify, make_response

from data.group.models import GroupModel


def create_user(payload):
    print(payload)
    user_schema = UserSchema()
    try:
        id_group = payload.pop('id_group', None)

        user_data = user_schema.load(payload)
        new_user = UserModel(**user_data)  # This should now work
        new_user.actual_balance = new_user.initial_balance
        new_user.daily_balance = new_user.initial_balance
        db.session.add(new_user)
        db.session.flush()
        if id_group:
            group = GroupModel.query.get(id_group)
            if group:
                group.users.append(new_user)
            else:
                print(f"Warning: Group with id {id_group} not found")

        db.session.commit()

        response = jsonify({'message': 'User created successfully'})
        return make_response(response, 201)
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")  # Print the exception message
        response = jsonify({'error': str(e)})
        return make_response(response, 400)


def get_user(id_user):
    user = UserModel.query.get(id_user)
    if user:
        user_dict = user.__dict__
        return user_dict, 200
    else:
        return {'message': 'User not found'}, 404


def get_all_users():
    users = db.session.query(UserModel).all()
    user_schema = UserSchema(many=True)
    return user_schema.dump(users)


def update_user_balance(id_user, new_balance):
    user = UserModel.query.get(id_user)
    if user:
        user.actual_balance = new_balance
        db.session.commit()
        return {'message': 'User balance successfully updated'}, 200
    else:
        return {'message': 'User not found'}, 404


def update_user_daily_balance(id_user, new_balance):
    user = UserModel.query.get(id_user)
    if user:
        user.daily_balance = new_balance
        db.session.commit()
        return {'message': 'User balance successfully updated'}, 200
    else:
        return {'message': 'User not found'}, 404


def remove_user(id_user):
    user = UserModel.query.get(id_user)
    if user:
        for group in user.user_groups:
            group.users.remove(user)
            if not group.users:
                db.session.delete(group)

        for position in user.positions:
            db.session.delete(position)

        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User and associated data successfully deleted'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if isinstance(o, PositionTypeEnum):
            return o.value
        if hasattr(o, '__dict__'):
            obj_dict = o.__dict__.copy()
            obj_dict.pop('_sa_instance_state', None)
            obj_dict.pop('user_position', None)
            obj_dict.pop('users', None)
            obj_dict.pop('traders', None)
            return obj_dict

        return super().default(o)


def close_user_positions(id_user):
    user = UserModel.query.get(id_user)
    if user:
        ip, port = get_group_ip_by_user_id(id_user)
        url = f"http://{ip}:{port}/api/position/"
        headers = {'Content-Type': 'application/json'}
        data = {
            "positions": user.positions,
            "user": user,
        }
        response = requests.delete(url, headers=headers, data=CustomEncoder().encode(data))
        if response.status_code == 200:
            for position in user.positions:
                remove_position(position.id_order)
            return jsonify({'message': 'User positions successfully closed'}), 200
        else:
            return response.json(), response.status_code
    else:
        return jsonify({'message': 'User not found'}), 404