import requests
import time
import json
from tools import get_config, headers, post_form_headers

CONFIG = get_config('config.ini')

TOKEN = CONFIG['KOVAN']['token']  # 请替换成自己的TOKEN
REFERER = CONFIG['KOVAN']['referer']
BASE_URL = CONFIG['KOVAN']['base_url']
SITE_KEY = CONFIG['KOVAN']['site_key']  # 请替换成自己的SITE_KEY


def create_task():
    url = f"{BASE_URL}/v3/recaptcha/create?token={TOKEN}&siteKey={SITE_KEY}&siteReferer={REFERER}"
    response = requests.get(url, headers=headers)
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


def post_form(recaptcha_response, receive_address):
    faucet_url = 'https://faucets.chain.link/api/faucet'
    data = {"accountAddress": receive_address, "captchaToken": recaptcha_response, "network": "kovan",
            "tokens": ["ETH"]}
    response = requests.post(faucet_url, headers=post_form_headers, data=json.dumps(data))
    return response


def send_request(receive_address: str) -> bool:
    task_id = create_task()
    if not task_id:
        raise Exception("None TaskId")
    recaptcha_response = polling_task(task_id)
    resp = post_form(recaptcha_response, receive_address)
    if resp.status_code == 200:
        print(f"{receive_address} claim 0.1 eth success")
        return True
    else:
        return False


def kovan_claim(receive_address: str):
    count = 0
    while count <= 3:
        success = send_request(receive_address)
        if success:
            print(f"success, {receive_address} claim 0.1 eth.")
            break
        else:
            count += 1
            time.sleep(3)
