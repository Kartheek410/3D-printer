import os
import requests
import json
import time


def request(url, method, params={}, timeout=3):
    headers = {'content-type': 'application/json'}
    jsonid = 1

    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": jsonid
    }

    payload = json.dumps(payload).encode()

    try:
        r = requests.post(url,
                          data=payload,
                          headers=headers,
                          timeout=timeout)
    except Exception as e:
        print('error in json rpc request', e)
        return False

    return r.json()


if __name__ == '__main__':
    moto_url = 'http://192.168.40.120:2001'

    # enable motor
    ret = request(moto_url, 'motor_enable')
    print(ret)

    # start homing
    ret = request(moto_url, 'home')
    print(ret)

    # wait until homing done
    while True:
        ret = request(moto_url, 'home_status')
        if ret['result'] == 1:
            break
        time.sleep(0.5)

    # absolute movement to position 10000
    ret = request(moto_url, 'position_set', {'position': 10000})

    # wait until absolute movement done
    while True:
        ret = request(moto_url, 'motor_state')
        if ret['result'] == "ready":
            break
        time.sleep(0.5)

    ret = request(moto_url, 'position_get')
    print(ret)

    # relative movement of -5000 steps
    ret = request(moto_url, 'position_move', {'steps': -5000})

    # wait until relative movement done
    while True:
        ret = request(moto_url, 'motor_state')
        if ret['result'] == 'ready':
            break
        time.sleep(0.5)

    ret = request(moto_url, 'position_get')
    print(ret)
