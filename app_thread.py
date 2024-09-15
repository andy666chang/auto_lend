
from user import load_user
from authenticated import _build_authentication_headers
from wallet import get_wallet
from lend import bit_lend
import requests
import json
import time
import os
import threading

THREAD_NUM = 5


def fund_wallet_get(user):
    wallet = []
    data = get_wallet(user)
    for i in data:
        if i[0] == 'funding':
            wallet.append(i)

    return wallet

def lend_job(user):
    print("user: " + user['name'])

    # Get user lend config
    lends = user['lend']

    # Get wallet info
    wallet = fund_wallet_get(user)
    # print(wallet)

    # Search all lend config
    for lend in lends:
        symbol = ''
        amount = 0
        
        # Search wallet
        for coin in wallet:
            if coin[1] == lend['symbol']:
                symbol = coin[1];
                amount = coin[4];
                break;
        
        if symbol == '':
            continue; # skip

        # seperate amount
        sub_amount = 0
        if amount > lend['amount'] :
            sub_amount = lend['amount']
        elif amount > 150 :
            sub_amount = amount
        else :
            continue;

        symbol = 'f' + symbol
        ret = bit_lend(user, symbol, str(sub_amount), str(lend['rate']), 120);
        # print(ret)
        print(ret.text)

    # print(user['name'] + " Finish")
    semaphore.release()
    return



if __name__ == '__main__':

    # Get path
    dire = os.path.dirname(os.path.abspath(__file__))
    # print("Current directory:", dire)
    # print("Load file:" + dire + os.sep + "database.json")

    # Load users
    users = load_user(dire + os.sep + "database.json")

    # 建立旗標
    semaphore = threading.Semaphore(THREAD_NUM)

    # Process all users
    for user in users:
        semaphore.acquire()
        t = threading.Thread(target = lend_job, args = (user,))
        t.daemon = True 
        t.start()

    # time.sleep(5)
    for x in range(THREAD_NUM):
        semaphore.acquire()

    for x in range(THREAD_NUM):
        semaphore.release()