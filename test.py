
from datetime import datetime
import os, json, hmac, hashlib
import requests

API_KEY, API_SECRET = (
    "YOUR_BFX_API_KEY",
    "YOUR_BFX_API_SECRET"
)

def _build_authentication_headers(endpoint, payload = None):
    nonce = str(round(datetime.now().timestamp() * 1_000))

    message = f"/api/v2/{endpoint}{nonce}"

    if payload != None:
        message += json.dumps(payload)

    signature = hmac.new(
        key=API_SECRET.encode("utf8"),
        msg=message.encode("utf8"),
        digestmod=hashlib.sha384
    ).hexdigest()

    return {
        "bfx-apikey": API_KEY,
        "bfx-nonce": nonce,
        "bfx-signature": signature
    }


API = "https://api.bitfinex.com/v2"
endpoint = "auth/r/wallets"
payload = {}
headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    **_build_authentication_headers(endpoint, payload)
}

response = requests.post(f"{API}/{endpoint}", json=payload, headers=headers)

print("wallet info")
# print(response.text)
# print()
# [
#     ["exchange","TRX",0.000005,0,0.000005,null,null],
#     ["exchange","ADA",9014.17733964,0,9014.17733964,null,null],
#     ["funding","USD",58612.51360097,0,535.91699104,null,null],
#     ["exchange","UST",1.27421408,0,1.27421408,"Affiliate Rebate",null],
#     ["exchange","USD",0,0,0,null,null]
# ]

data_arr = json.loads(response.text)
# print(type(data_arr))
for data in data_arr:
    print(data)
