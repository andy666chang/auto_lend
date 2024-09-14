
from datetime import datetime
import os, json, hmac, hashlib
import requests


def _build_authentication_headers(key, secret, endpoint, payload = None):
    nonce = str(round(datetime.now().timestamp() * 1_000))

    message = f"/api/v2/{endpoint}{nonce}"

    if payload != None:
        message += json.dumps(payload)

    signature = hmac.new(
        key=secret.encode("utf8"),
        msg=message.encode("utf8"),
        digestmod=hashlib.sha384
    ).hexdigest()

    return {
        "bfx-apikey": key,
        "bfx-nonce": nonce,
        "bfx-signature": signature
    }


if __name__ == '__main__':

    key, secret = (
        # os.getenv("BFX_API_KEY"),
        # os.getenv("BFX_API_SECRET")
        "YOUR_BFX_API_KEY",
        "YOUR_BFX_API_SECRET"
    )

    API = "https://api.bitfinex.com/v2"
    endpoint = "auth/w/order/submit"
    payload = {
        "type": "EXCHANGE LIMIT",
        "symbol": "tBTCUSD",
        "amount": "0.165212",
        "price": "30264.0"
    }
    headers = {
        "Content-Type": "application/json",
        **_build_authentication_headers(key, secret, endpoint, payload)
    }
    
    print("order submit")
    response = requests.post(f"{API}/{endpoint}", json=payload, headers=headers)
    print(response.text)
    print()
    
    #########################
    
    API = "https://api.bitfinex.com/v2"
    endpoint = "auth/r/wallets"
    payload = {}
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        **_build_authentication_headers(key, secret, endpoint, payload)
    }
    
    response = requests.post(f"{API}/{endpoint}", json=payload, headers=headers)
    
    print("wallet info")
    print(response.text)
    print()
    # [
    #     ["exchange","TRX",0.000005,0,0.000005,null,null],
    #     ["exchange","ADA",9014.17733964,0,9014.17733964,null,null],
    #     ["funding","USD",58612.51360097,0,535.91699104,null,null],
    #     ["exchange","UST",1.27421408,0,1.27421408,"Affiliate Rebate",null],
    #     ["exchange","USD",0,0,0,null,null]
    # ]
    
    #########################
    
    API = "https://api.bitfinex.com/v2"
    endpoint = "auth/r/funding/offers/fUSD"
    payload = {}
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        **_build_authentication_headers(key, secret, endpoint, payload)
    }
    
    response = requests.post(f"{API}/{endpoint}", json=payload, headers=headers)
    
    print("funding info")
    print(response.text)
    print()
    # [
    #     [3372550597,"fUSD",1724532988000,1724532988000,4102.04114086,4102.04114086,"LIMIT",null,null,0,"ACTIVE",null,null,null,0.00036,120,0,0,null,0,null]
    # ]
    
    #########################
    
    API = "https://api.bitfinex.com/v2"
    endpoint = "auth/w/funding/offer/submit"
    payload = {
        "type": "LIMIT",
        "symbol": "fUSD",
        "amount": "535",
        "rate": "0.0004",
        "period": 120,
        "flags": 0
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        **_build_authentication_headers(key, secret, endpoint, payload)
    }
    
    response = requests.post(f"{API}/{endpoint}", json=payload, headers=headers)
    
    print("funding offer submit")
    print(response.text)
    print()
    # [
    #     1724567357365,"fon-req",null,null,
    #     [3373562054,"fUSD",1724567357357,1724567357357,535,535,"LIMIT",null,null,0,"ACTIVE",null,null,null,0.0004,120,false,0,null,false,null],
    #     null,"SUCCESS","Submitting funding offer of 535.0 USD at 0.04000 for 120 days."
    # ]
    
    