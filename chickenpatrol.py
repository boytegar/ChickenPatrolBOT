from datetime import datetime
import time
from urllib.parse import parse_qs, unquote
import json
import random
import requests

def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] | {word}")

class ChickenPatrol:

    def __init__(self):

        self.header = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "priority": "u=1, i",
            "sec-ch-ua": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129", "Microsoft Edge WebView2";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "Referer": "https://app.chickenpatrol.xyz/",
            "Origin":"https://app.chickenpatrol.xyz",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
        }
    
    
    def make_request(self, method, url, headers, json=None, data=None):
        retry_count = 0
        while True:
            time.sleep(2)
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, json=json)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=json, data=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=json, data=data)
            else:
                raise ValueError("Invalid method.")
            if response.status_code >= 500:
                if retry_count >= 4:
                    print_(f"Status Code: {response.status_code} | {response.text}")
                    return None
                retry_count += 1
                return None
            elif response.status_code >= 400:
                print_(f"Status Code: {response.status_code} | {response.text}")
                return None
            elif response.status_code >= 200:
                return response
    
    def auth(self, query):
        url = 'https://api.chickenpatrol.xyz/app/auth/authenAuthSignature'
        headers = {
            **self.header
        }
        payload = {"initData": query,"invite":"eDf33rSL"}
        

        response = self.make_request('post', url=url, headers=headers, json=payload)
        if response is not None:
            jsons = response.json()
            return jsons
    
    def get_user(self, token):
        url = 'https://api.chickenpatrol.xyz/app/user'
        headers = {
            **self.header,
            'Authorization': f"Bearer {token}"
        }
        response = self.make_request('get', url=url, headers=headers)
        if response is not None:
            jsons = response.json()
            return jsons
    
    def tap(self, token, tap):
        url = 'https://api.chickenpatrol.xyz/app/user/tap'
        headers = {
            **self.header,
            'Authorization': f"Bearer {token}"
        }
        payload = {"count":tap}
        response = self.make_request('post', url=url, headers=headers, json=payload)
        if response is not None:
            jsons = response.json()
            return jsons
    
    def buy_tcn(self, token):
        url = 'https://api.chickenpatrol.xyz/app/user/buychicktcn'
        headers = {
            **self.header,
            'Authorization': f"Bearer {token}"
        }
        response = self.make_request('get', url=url, headers=headers)
        if response is not None:
            jsons = response.json()
            data = jsons.get('data')
            print_(f"Buy Done : Rank {data.get('rank')}")
            return jsons
    
    def clear_task(self, token, title):
        url = f'https://api.chickenpatrol.xyz/app/task/{title}'
        headers = {
            **self.header,
            'Authorization': f"Bearer {token}"
        }
        response = self.make_request('get', url=url, headers=headers)
        if response is not None:
            print_(f"Task {title} done")
