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
    params = sorted(params.items())
    message = urlencode(params).encode('utf8')
    m = hashlib.md5()
    m.update(message)
    return m.hexdigest()


def _account_type_to_id(account_type):
    d = {
        'cny': 1,
        'usd': 2,
    }
    return d.get(account_type)


def _set_coin_type(params, coin_type):
    d = {
        'btc': 1,
        'ltc': 2,
    }
    params['coin_type'] = d.get(coin_type, 1)


def _loan_type_to_id(loan_type):
    d = {
        'cny': 1,
        'btc': 2,
        'ltc': 3,
        'usd': 4,
    }
    return d.get(loan_type)


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
            'repay_all': None,
        }
        for k, v in list(params.items()):
            if k in skip_params:
                skip_params[k] = v
                del params[k]

        params['access_key'] = self.access_key
        params['secret_key'] = self.secret_key
        params['created'] = int(time.time())
        params['sign'] = _signature(params)
        # NOTE: secret_key should not be in signature
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

    def get_new_deal_orders(self, coin_type='btc'):
        params = {
            'method': 'get_new_deal_orders'
        }
        _set_coin_type(params, coin_type)
        return self._request(params)

    def get_order_id_by_trade_id(self, trade_id, coin_type='btc'):
        params = {
            'method': 'get_new_deal_orders',
            'trade_id': trade_id,
        }
        _set_coin_type(params, coin_type)
        return self._request(params)

    def withdraw_coin(self, address, amount, trade_pwd=None, coin_type='btc'):
        params = {
            'method': 'withdraw_coin',
            'withdraw_address': address,
            'withdraw_amount': amount,
            'trade_password': trade_pwd,
            # withdraw_fee: useless
        }
        _set_coin_type(params, coin_type)
        return self._request(params)

    def cancel_withdraw_coin(self, withdraw_coin_id):
        params = {
            'method': 'cancel_withdraw_coin',
            'withdraw_coin_id': withdraw_coin_id,
        }
        return self._request(params)

    def get_withdraw_coin_result(self, withdraw_coin_id):
        params = {
            'method': 'get_withdraw_coin_result',
            'withdraw_coin_id': withdraw_coin_id,
        }
        return self._request(params)

    def transfer(self, account_from, account_to, amount):
        params = {
            'method': 'transfer',
            'account_from': _account_type_to_id(account_from),
            'account_to': _account_type_to_id(account_to),
            'amount': amount
        }
        return self._request(params)

    def loan(self, amount, loan_type):
        params = {
            'method': 'loan',
            'amount': amount,
            'loan_type': _loan_type_to_id(loan_type),
        }
        return self._request(params)

    def repay(self, loan_id, amount, repay_all=False):
        params = {
            'method': 'repayment',
            'loan_id': loan_id,
            'amount': amount,
            'repay_all': 1 if repay_all else 0,
        }
        return self._request(params)

    def get_loan_available(self):
        params = {
            'method': 'get_loan_available',
        }
        return self._request(params)

    def get_loans(self):
        params = {
            'method': 'get_loans',
        }
        return self._request(params)
