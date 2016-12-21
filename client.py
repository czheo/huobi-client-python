import os
import time
import hashlib
import requests
try:
    # py3
    from urllib.parse import urlencode
except:
    # py2
    from urllib import urlencode

HUOBI_API = "https://api.huobi.com/apiv3"


def _signature(params):
    params = sorted(params.items(), key=lambda d: d[0])
    message = urlencode(params).encode('utf8')
    m = hashlib.md5()
    m.update(message)
    m.digest()
    sig = m.hexdigest()
    return sig


def _set_coin_type(params, coin_type):
    d = {
        'btc': 1,
        'ltc': 2,
    }
    params['coin_type'] = d.get(coin_type, 1)


class Client:
    def __init__(self):
        key_path = os.path.join(os.path.expanduser('~'), '.huobi.keys')
        with open(key_path) as f:
            self.access_key, self.secret_key = f.read().splitlines()

    def _request(self, params):
        # delete and save params that not participate in signature
        skip_params = {
            'market': None,
            'trade_password': None,
            'trade_id': None,
        }
        for k, v in list(params.items()):
            if k in skip_params:
                skip_params[k] = v
                del params[k]

        params['access_key'] = self.access_key
        params['secret_key'] = self.secret_key
        params['created'] = int(time.time())
        params['sign'] = _signature(params)
        # NOTE: market should not be in signature
        del params['secret_key']

        # put skipped params back
        params.update(skip_params)
        # delete None params
        params = {k: v for k, v in params.items() if v is not None}
        return requests.get(HUOBI_API, params).json()

    def get_account_info(self):
        params = {
            'method': 'get_account_info',
        }
        return self._request(params)

    def get_orders(self, coin_type='btc'):
        params = {
            'method': 'get_orders',
        }
        _set_coin_type(params, coin_type)
        return self._request(params)

    def get_order_info(self, id, coin_type='btc'):
        params = {
            'method': 'order_info',
            'id': id
        }
        _set_coin_type(params, coin_type)
        return self._request(params)

    def buy(self, price, amount, trade_password=None,
            trade_id=None, coin_type='btc'):
        params = {
            'method': 'buy',
            'price': price,
            'amount': amount,
            'trade_password': trade_password,
            'trade_id': trade_id,
        }
        _set_coin_type(params, coin_type)
        return self._request(params)

    def sell(self, price, amount, trade_password=None,
             trade_id=None, coin_type='btc'):
        params = {
            'method': 'sell',
            'price': price,
            'amount': amount,
            'trade_password': trade_password,
            'trade_id': trade_id,
        }
        _set_coin_type(params, coin_type)
        return self._request(params)

    def buy_market(self, amount, trade_password=None,
                   trade_id=None, coin_type='btc'):
        '''
        amount: amount of cny
        '''
        params = {
            'method': 'buy_market',
            'amount': amount,
            'trade_password': trade_password,
            'trade_id': trade_id,
        }
        _set_coin_type(params, coin_type)
        return self._request(params)

    def sell_market(self, amount, trade_password=None,
                    trade_id=None, coin_type='btc'):
        '''
        amount: amount of btc
        '''
        params = {
            'method': 'sell_market',
            'amount': amount,
            'trade_password': trade_password,
            'trade_id': trade_id,
        }
        _set_coin_type(params, coin_type)
        return self._request(params)

    def cancel_order(self, id, coin_type='btc'):
        params = {
            'method': 'cancel_order',
            'id': id,
        }
        _set_coin_type(params, coin_type)
        return self._request(params)
