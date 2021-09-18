import requests
import json
import time
from tools import get_config, headers, proxies

config = get_config('config.ini')


def mumbai_claim(receive_address: str):
    count = 0
    while count <= 3:
        url = 'https://api.faucet.matic.network/transferTokens'
        data = {"network": "mumbai", "address": receive_address, "token": "maticToken"}
        resp = requests.post(url=url, headers=headers, data=json.dumps(data), proxies=proxies).content
        resp = resp.decode('utf-8')
        if 'hash' in json.dumps(resp):
            print(f"{receive_address} success,claim 1 tmatic")
            break
        if 'err' in json.dumps(resp):
            count += 1
            time.sleep(5)
