""" Routes for the endpoint 'hello_world'"""

from flask import Blueprint, request

from data.trader.services import remove_trader, create_trader

NAME = 'Trader'

trader_blueprint = Blueprint(f"{NAME}_blueprint", __name__)


@trader_blueprint.post(f"/trader/")
def post_trader():
    payload = request.get_json()
    try:
        entity = create_trader(payload)
        if entity is None:
            return "Groups not found", 404
        return entity
    except Exception as e:
        return f"Error: {str(e)}", 400


@trader_blueprint.delete(f"/trader/<string:id_trader>/<string:id_group>")
def delete_trader(id_trader, id_group):
    try:
        entity = remove_trader(id_trader, id_group)
        return entity
    except Exception as e:
        return f"Error: {str(e)}", 400
