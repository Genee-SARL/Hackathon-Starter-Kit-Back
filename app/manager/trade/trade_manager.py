import requests
import json
import datetime

from data.position.enums import PositionTypeEnum
from data.position.services import create_position, remove_position, get_positions_by_user_and_trader
from data.group.services import get_users_in_same_group_with_trader, get_group_ip_by_user_id
from data.user.services.user_service import get_all_users, update_user_balance, update_user_daily_balance


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if isinstance(o, PositionTypeEnum):
            return o.value

        return super().default(o)


class TradeManager:

    @staticmethod
    def open_orders_for_user(positions, trader_id):
        users = get_users_in_same_group_with_trader(trader_id)
        for user in users:
            ip, port = get_group_ip_by_user_id(user['id_user'])
            url = f"http://{ip}:{port}/api/position/"
            headers = {'Content-Type': 'application/json'}
            data = {
                "positions": positions,
                "trader_id": trader_id,
                "user": user
            }
            response = requests.post(url, headers=headers, data=DateTimeEncoder().encode(data))
            response_data = response.json()
            if isinstance(response_data, list):
                response_data = [item for sublist in response_data for item in sublist]
            if response.status_code == 200:
                for position in response_data:
                    create_position(position, trader_id, user['id_user'])

    @staticmethod
    def close_orders_for_user(positions, trader_id):
        print("close orders for user")
        users = get_users_in_same_group_with_trader(trader_id)
        for user in users:
            user_positions = []
            ip, port = get_group_ip_by_user_id(user['id_user'])
            url = f"http://{ip}:{port}/api/position/"
            headers = {'Content-Type': 'application/json'}
            for position in positions:
                user_positions.append(get_positions_by_user_and_trader(user['id_user'], position, trader_id))
            data = {
                "positions": user_positions,
                "user": user
            }
            response = requests.delete(url, headers=headers, data=DateTimeEncoder().encode(data))
            response_data = response.json()
            for position in response_data:
                remove_position(position)

    @staticmethod
    def check_user_position(code):
        users = get_all_users()
        for user in users:
            ip, port = get_group_ip_by_user_id(user["id_user"])
            url = f"http://{ip}:{port}/api/user_balance/"
            response = requests.get(url, data=DateTimeEncoder().encode(user), headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                balance = response.json().get('balance')
                if balance is not None:
                    if code == 1:
                        update_user_balance(user["id_user"], balance)
                    else:
                        update_user_daily_balance(user["id_user"], balance)