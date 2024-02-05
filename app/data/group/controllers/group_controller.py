""" Routes for the endpoint 'hello_world'"""

from flask import Blueprint

from data.group.services import get_all_groups_with_users_and_traders, get_group_with_users_and_traders

NAME = 'Group'

group_blueprint = Blueprint(f"{NAME}_blueprint", __name__)


@group_blueprint.get(f"/group/all/")
def get_all_group():
    entity = get_all_groups_with_users_and_traders()
    if entity is None:
        return "Groups not found", 404
    return entity, 200


@group_blueprint.get(f"/group/<string:id>")
def get_group_by_id(id):
    entity = get_group_with_users_and_traders(id)
    if entity is None:
        return f"Group {id} not found", 404
    return entity, 200