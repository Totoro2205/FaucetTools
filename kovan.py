import requests
import time
import json
from tools import get_config, headers

CONFIG = get_config('config.ini')

RECEIVE_ADDRESS = CONFIG['CONF']['RECEIVE_ADDRESS']
BASE_URL = CONFIG['CONF']['BASE_URL']
TOKEN = CONFIG['CONF']['TOKEN']
SITE_KEY = CONFIG['CONF']['SITE_KEY']
REFERER = CONFIG['CONF']['REFERER']


def create_task():
    url = f"{BASE_URL}/v3/recaptcha/create?token={TOKEN}&siteKey={SITE_KEY}&siteReferer={REFERER}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('data', {}).get('taskId')


def polling_task(task_id):
    url = f"{BASE_URL}/v3/recaptcha/status?token={TOKEN}&taskId={task_id}"
    count = 0
    while count < 120:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                status = data.get('data', {}).get('status')
                if status == 'Success':
                    return data.get('data', {}).get('response')
        except requests.RequestException as e:
            print('polling task failed', e)
        finally:
            count += 1
            time.sleep(1)


def post_form(recaptcha_response):
    faucet_url = 'https://linkfaucet.protofire.io/eth-faucet'
    data = {"chain": "kovan",
            "g-recaptcha-response": recaptcha_response,
            "address": RECEIVE_ADDRESS}
    response = requests.post(faucet_url, headers=headers, data=json.dumps(data))
    return response


def send_request():
    task_id = create_task()
    recaptcha_response = polling_task(task_id)
    resp = post_form(recaptcha_response)
    if resp.status_code == 200:
        return True
    else:
        return False


def kovan_claim():
    count = 0
    while count <= 3:
        success = send_request()
        if success:
            print(f"success, {RECEIVE_ADDRESS} claim 0.1 eth.")
            break
        else:
            count += 1
            time.sleep(10)
