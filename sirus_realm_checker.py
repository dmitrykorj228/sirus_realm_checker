import json
from json import JSONDecodeError
from time import sleep
import logging

import requests

TOKEN = "7711822294:AAEN6ywEkaJSV-w2BHB5z8O9dS1sc4AsdX4"
CHAT_ID = "-1002289513470"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_realm_data():
    realm_name = "Soulseeker x1 - 3.3.5a+"
    try:
        import cloudscraper
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'firefox',
                'platform': 'windows',
                'mobile': False
            }
        )
        response = json.loads(scraper.get("https://sirus.su/api/statistic/tooltip.json").text)
        is_online = response['realms'][1]['isOnline']
        if response['realms'][1]['online'] < 10:
            is_online = False
    except (JSONDecodeError, KeyError):
        is_online = False
    except Exception:
        pass
    return {'isOnline': is_online, 'name': realm_name}


def send_tg_message(msg: str):
    full_tg_message = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    is_message_sent = False
    while not is_message_sent:
        try:
            requests.get(full_tg_message)
            is_message_sent = True
        except Exception:
            pass


def wait_for_server_up():
    while True:
        response = get_realm_data()
        is_online = response['isOnline']
        if is_online:
            send_tg_message(f"{server_name}is up now!")
            break
        sleep(15)


while True:
    try:
        sleep_time = 50
        realm_data = get_realm_data()
        server_name = realm_data['name']
        is_online = realm_data['isOnline']
        if not is_online:
            send_tg_message(f"{server_name}is offline!")
            wait_for_server_up()
        sleep(sleep_time)
    except Exception as e:
        logger.exception(e)
