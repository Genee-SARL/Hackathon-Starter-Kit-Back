""" Routes for the endpoint 'hello_world'"""

from flask import Blueprint, request

from data.user.services import create_user, remove_user

NAME = 'User'

user_blueprint = Blueprint(f"{NAME}_blueprint", __name__)


@user_blueprint.post(f"/user/")
def get_all_group():
    payload = request.get_json()
    try:
        entity = create_user(payload)
        if entity is None:
            return "Groups not found", 404
        return entity, 200
    except Exception as e:
        return f"Error: {str(e)}", 400


@user_blueprint.post(f"/user/close/<string:id_user>")
def close_user_positions(id_user):
    try:
        entity = close_user_positions(id_user)
        return entity
    except Exception as e:
        return f"Error: {str(e)}", 400


@user_blueprint.delete(f"/user/<string:id_user>")
def delete_group(id_user):
    try:
        entity = remove_user(id_user)
        return entity
    except Exception as e:
        return f"Error: {str(e)}", 400
