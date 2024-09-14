
from user import load_user
from authenticated import _build_authentication_headers
from wallet import get_wallet
import requests
import json

def bit_lend(user, symbol, amount, rate, period):
    key = user['key']
    secret = user['secret']

    API = "https://api.bitfinex.com/v2"
    endpoint = "auth/w/funding/offer/submit"
    payload = {
        "type": "LIMIT",
        "symbol": symbol,
        "amount": amount,
        "rate": rate,
        "period": period,
        "flags": 0
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        **_build_authentication_headers(key, secret, endpoint, payload)
    }

    return requests.post(f"{API}/{endpoint}", json=payload, headers=headers)



if __name__ == '__main__':
    users = load_user("database.json")

    for user in users:

        lends = user['lend']
        for lend in lends:
            print(lend)

        print()

        data = get_wallet(user)
        for i in data:
            if i[0] == 'funding':
                symbol = i[1]
                amount = i[4]
                print(symbol + ": " + str(amount))

                config = {}
                for lend in lends:
                    if lend['symbol'] == symbol :
                        config = lend
                        break;

                if config == {}:
                    continue;

                sub_amount = 0
                if amount > config['amount'] :
                    sub_amount = config['amount']
                elif amount > 200 :
                    sub_amount = amount
                else :
                    continue;


                symbol = 'f' + symbol
                ret = bit_lend(user, symbol, str(sub_amount), str(config['rate']), 120);
                print(ret)
                print(ret.text)



