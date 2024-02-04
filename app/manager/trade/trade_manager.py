import requests
import json
from data.position.services import create_position, remove_position, get_positions_by_user_and_trader
from data.group.services import get_users_in_same_group_with_trader, get_group_ip_by_user_id


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
            response = requests.post(url, headers=headers, data=json.dumps(data))
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
            response = requests.delete(url, headers=headers, data=json.dumps(data))
            response_data = response.json()
            for position in response_data:
                print(position)
                remove_position(position)
