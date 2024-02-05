import os
import time
import sys
import requests
import json
from datetime import datetime

from bs4 import BeautifulSoup

from data.group.services import get_group_ip_by_user_id
from data.trader.services import (
    get_all_position_from_trader,
    get_all_traders_id,
    post_new_position,
    register_daily_drowdown,
    register_daily_drowdown_anchor,
    remove_position,
)
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from data.user.services.user_service import get_all_users, update_user_daily_balance, update_user_balance
from manager.trade import TradeManager


class ScraperManager:
    load_dotenv()
    user_login = os.getenv("MQ5_LOGIN")
    password = os.getenv("MQ5_PASSWORD")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
    )
    options.add_argument(f"user-agent={user_agent}")
    url = "https://www.mql5.com/en"
    trade_manager = TradeManager()

    def login(self, driver, user_login, user_password):
        driver.get(self.url + "/auth_login")
        wait = WebDriverWait(driver, 15)
        login_input = wait.until(ec.presence_of_element_located((By.ID, "Login")))
        login_input.send_keys(str(user_login))
        pwd = wait.until(ec.presence_of_element_located((By.ID, "Password")))
        pwd.send_keys(user_password)
        pwd.send_keys(Keys.ENTER)
        time.sleep(5)
        if driver.current_url != self.url:
            raise ValueError("Échec de Connexion ")
        return wait

    @staticmethod
    def get_trader_positions(results, column):
        array_column = []
        position_table = []
        for col in column:
            array_column.append(col.text)
        time_index = array_column.index("Time")
        symbole_index = array_column.index("Symbol")
        type_index = array_column.index("Type")
        volume_index = array_column.index("Volume")
        rows = results.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) > max(time_index, symbole_index, type_index, volume_index):
                if symbole_index < len(cols):
                    if cols[symbole_index].text != "":
                        position_type = cols[type_index].text
                        if position_type not in ["Buy", "Sell"]:
                            continue
                        position_table.append(
                            {
                                "Symbol": cols[symbole_index].text,
                                "Time": cols[time_index].text,
                                "Type": cols[type_index].text,
                                "Volume": cols[volume_index].text,
                            }
                        )
                    continue
        position_table = sorted(
            position_table, key=lambda x: datetime.strptime(x["Time"], "%Y.%m.%d %H:%M"), reverse=True
        )
        return position_table

    def detect_changes(self, current_position, saved_position, trader_id):
        if not saved_position:
            for position in current_position:
                post_new_position(trader_id, position)
            self.trade_manager.open_orders_for_user(current_position, trader_id)
            return
        if not current_position:
            for position in saved_position:
                remove_position(trader_id, position)
            self.trade_manager.close_orders_for_user(saved_position, trader_id)
            return
        added_positions = [pos for pos in current_position if pos not in saved_position]
        removed_positions = [pos for pos in saved_position if pos not in current_position]
        if added_positions:
            for position in added_positions:
                post_new_position(trader_id, position)
            self.trade_manager.open_orders_for_user(added_positions, trader_id)

        if removed_positions:
            for position in removed_positions:
                remove_position(trader_id, position)
            self.trade_manager.close_orders_for_user(removed_positions, trader_id)

    @staticmethod
    def extract_value(label_text, s_list_info):
        label_div = s_list_info.find("div", class_="s-list-info__label", string=lambda t: label_text in t)
        if label_div:
            value_div = label_div.find_next("div", class_="s-list-info__value")
            if value_div:
                value_text = value_div.text.strip()
                numeric_value = float("".join(c for c in value_text if (c.isdigit() or c == ".")))
                return numeric_value
        return None

    def save_trader_drowdown(self, app):
        with app.app_context():
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
            self.login(driver, self.user_login, self.password)
            trader_data = get_all_traders_id()
            soup = BeautifulSoup(driver.page_source, "html.parser")
            s_list_info = soup.find("div", class_="s-list-info")
            for trader in trader_data:
                driver.get(self.url + "/signals/" + str(trader["id_trader"]) + "?source=Site+Signals+MT5+Tile")
                time.sleep(5)
                equity = self.extract_value("Equity", s_list_info)
                balance = self.extract_value("Balance", s_list_info)
                register_daily_drowdown_anchor(trader.id_trader, balance)

    def check_traders_position(self, app):
        with app.app_context():
            try:
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
                self.login(driver, self.user_login, self.password)
                trader_data = get_all_traders_id()
                for trader in trader_data:
                    driver.get(self.url + "/signals/" + trader.id_trader + "?source=Site+Signals+MT5+Tile")
                    time.sleep(5)
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    s_list_info = soup.find("div", class_="s-list-info")
                    signaldatahidden = soup.find("tr", class_="signalDataHidden")
                    if signaldatahidden:
                        print('Trader not followed', file=sys.stderr)
                        continue
                    balance = self.extract_value("Balance", s_list_info)
                    equity = self.extract_value("Equity", s_list_info)
                    register_daily_drowdown(trader.id_trader, equity - balance)
                    column_table = driver.find_element(By.XPATH, '//*[@id="signal_tab_content_trading"]/table/thead')
                    results = driver.find_element(By.XPATH, '//*[@id="signal_tab_content_trading"]/table/tbody')
                    column = column_table.find_elements(By.TAG_NAME, "th")
                    trader_positions = self.get_trader_positions(results, column)
                    saved_positions = get_all_position_from_trader(trader.id_trader)
                    self.detect_changes(trader_positions, saved_positions, trader.id_trader)
                driver.quit()
            except Exception as e:
                print(e)

    def check_user(self, app, code):
        with app.app_context():
            self.trade_manager.check_user_position(code)
