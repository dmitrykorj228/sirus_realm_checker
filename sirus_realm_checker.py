from time import sleep
import json
import logging

import psutil
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

TOKEN = "7711822294:AAEN6ywEkaJSV-w2BHB5z8O9dS1sc4AsdX4"
CHAT_ID = "-1002289513470"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_realm_data():
    realm_name = "Soulseeker x1 - 3.3.5a+"
    kill_old_browser()
    driver = uc.Chrome(headless=False, use_subprocess=True)
    try:
        driver.get('https://sirus.su/api/statistic/tooltip.jsonz')
        response = json.loads(driver.find_element(By.TAG_NAME, 'body').text)
        is_online = response['realms'][1]['isOnline']
    except Exception as e:
        print(type(e).__name__)
        is_online = False
    finally:
        driver.close()
    return {'isOnline': is_online, 'name': realm_name}


def send_tg_message(msg: str):
    full_tg_message = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    requests.get(full_tg_message)


def wait_for_server_up():
    while True:
        response = get_realm_data()
        is_online = response['isOnline']
        if is_online:
            send_tg_message(f"{server_name}is up now!")
            break
        sleep(10)


def kill_old_browser():
    for process in psutil.process_iter():
        if 'firefox' in str(process.name):
            process.kill()
            logger.info("Killed old browser")


while True:
    try:
        status = None
        sleep_time = 25
        realm_data = get_realm_data()
        server_name = realm_data['name']
        is_online = realm_data['isOnline']
        if not is_online:
            send_tg_message(f"{server_name}is offline!")
            wait_for_server_up()
        sleep(sleep_time)
    except Exception as e:
        logger.exception(e)
