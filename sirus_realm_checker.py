from time import sleep
import json
import logging
import tempfile
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

TOKEN = "7711822294:AAEN6ywEkaJSV-w2BHB5z8O9dS1sc4AsdX4"
CHAT_ID = "-1002289513470"

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_realm_data():
    service = Service(executable_path='/usr/bin/geckodriver')
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(service=service, options=options)
    driver.get('https://sirus.su/api/statistic/tooltip.json')
    response = json.loads(driver.find_element(By.TAG_NAME, 'body').text)
    driver.close()
    realm_name = "Soulseeker x1 - 3.3.5a+"
    try:
        is_online = response['realms'][1]['isOnline']
    except KeyError:
        is_online = False
    finally:
        temp_folder = tempfile.gettempdir()
        logger.info(f"Cleaning temp directory: {temp_folder}") 
        # shutil.rmtree(temp_folder)
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
