from time import sleep
import json

import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

TOKEN = "7711822294:AAEN6ywEkaJSV-w2BHB5z8O9dS1sc4AsdX4"
CHAT_ID = "-1002289513470"


def get_realm_data() -> bool:
    driver = uc.Chrome(headless=False, use_subprocess=True)
    driver.get('https://sirus.su/api/statistic/tooltip.json')
    response = json.loads(driver.find_element(By.TAG_NAME, 'body').text)
    driver.close()
    return response


def wait_for_server_up():
    while True:
        response = get_realm_data()
        is_online = response['isOnline']
        if is_online:
            tg_message = f"{server_name}is up now!"
            tg_send_message_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={tg_message}"
            requests.get(tg_send_message_url)
            break
        sleep(10)
    return True


while True:
    status = None
    sleep_time = 30
    realm_data = get_realm_data()['realms'][1]
    server_name = realm_data['name']
    is_online = realm_data['isOnline']
    if not is_online:
        tg_message = f"{server_name}is offline!"
        tg_send_message_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={tg_message}"
        requests.get(tg_send_message_url)
        wait_for_server_up()
    sleep(sleep_time)
