from data.group.models import GroupModel
from data.group.schemas import GroupSchema
from data.trader.schemas import CustomTraderSchema
from data.user.models import UserModel
from data.user.schemas import UserSchema, CustomUserSchema
from data.trader.models import TraderModel
from shared import db


def create_group(group_data):
    group_schema = GroupSchema()
    try:
        validated_data = group_schema.load(group_data)
        new_group = GroupModel(**validated_data)
        db.session.add(new_group)
        db.session.commit()
        return group_schema.dump(new_group), 200
    except Exception as e:
        return {'message': str(e)}, 400


def add_trader_to_group(id_group, id_trader):
    group = GroupModel.query.get(id_group)
    trader = TraderModel.query.get(id_trader)
    if group and trader:
        group.traders.append(trader)
        db.session.commit()
        return {'message': 'Trader successfully added to group'}, 200
    else:
        return {'message': 'Group or Trader not found'}, 404


def add_user_to_group(id_group, id_user):
    group = GroupModel.query.get(id_group)
    user = UserModel.query.get(id_user)
    if group and user:
        group.users.append(user)
        db.session.commit()
        return {'message': 'User successfully added to group'}, 200
    else:
        return {'message': 'Group or User not found'}, 404


def remove_user_from_group(id_group, id_user):
    group = GroupModel.query.get(id_group)
    user = UserModel.query.get(id_user)
    if group and user:
        group.users.remove(user)
        db.session.commit()
        return {'message': 'User successfully removed from group'}, 200
    else:
        return {'message': 'Group or User not found'}, 404


def remove_trader_from_group(id_group, id_trader):
    group = GroupModel.query.get(id_group)
    trader = TraderModel.query.get(id_trader)
    if group and trader:
        group.traders.remove(trader)
        db.session.commit()
        return {'message': 'Trader successfully removed from group'}, 200
    else:
        return {'message': 'Group or Trader not found'}, 404


def get_users_in_same_group_with_trader(id_trader):
    trader = TraderModel.query.get(id_trader)
    if trader:
        users = set()
        for group in trader.groups:
            for user in group.users:
                users.add(user)
        return UserSchema(many=True).dump(list(users))
    else:
        return {'message': 'Trader not found'}, 404


def get_group_ip_by_user_id(user_id):
    user = UserModel.query.get(user_id)
    if user:
        group = user.user_groups[0]  # Assuming the user belongs to at least one group
        if group:
            return group.ipaddress, group.port
        else:
            return {'message': 'User does not belong to any group'}, 404
    else:
        return {'message': 'User not found'}, 404


def get_all_groups_with_users_and_traders():
    groups = GroupModel.query.all()
    result = []
    for group in groups:
        group_data = GroupSchema().dump(group)
        group_data['users'] = CustomUserSchema(many=True).dump(group.users)
        group_data['traders'] = CustomTraderSchema(many=True).dump(group.traders)
        result.append(group_data)
    return result


def get_group_with_users_and_traders(group_id):
    group = GroupModel.query.get(group_id)
    if group:
        group_data = GroupSchema().dump(group)
        group_data['users'] = CustomUserSchema(many=True).dump(group.users)
        group_data['traders'] = CustomTraderSchema(many=True).dump(group.traders)
        return group_data
    else:
        return {'message': 'Group not found'}, 404
