

from user import load_user
from authenticated import _build_authentication_headers
import requests
import json

def get_wallet(user):
    key = user['key']
    secret = user['secret']

    API = "https://api.bitfinex.com/v2"
    endpoint = "auth/r/wallets"
    payload = {}
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        **_build_authentication_headers(key, secret, endpoint, payload)
    }
    
    response = requests.post(f"{API}/{endpoint}", json=payload, headers=headers)
    if response.status_code != 200:
        print(user['name'], response.status_code)
        return {}
    
    return response.json()


if __name__ == '__main__':
    users = load_user("database.json")
    
    for user in users:
        # print(user)
        data = get_wallet(user)
        for i in data:
            print(i)



