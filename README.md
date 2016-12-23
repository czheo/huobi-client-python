# huobi-client-python
## Installation
```
pip install huobi_client
```

## Put access key and secret key in `~/.huobi.keys`
```
xxxxxxxx-xxxxxxxx-xxxxxxxx-xxxxx
yyyyyyyy-yyyyyyyy-yyyyyyyy-yyyyy
```

## Usage

### Rest API
``` python
from huobi_client import Client
client = Client()
client.get_account_info() # get account info
client.get_orders() # get orders
client.get_order_info(id) # get order info by order id
client.buy(price, amount) # buy
client.sell(price, amount) # sell
client.buy_market(amount) # buy at market price
client.sell_market(amount) # sell at market price
client.cancel_order(id) # cancel order
client.get_new_deal_orders() # get new deal orders
client.withdraw_coin(address, amount)
client.cancel_withdraw_coin(withdraw_coin_id)
client.transfer(account_from, account_to, amount)
client.loan(amount, loan_type) # loan_type = {cny, btc, ltc, usd}
client.repay(loan_id, amount)
client.get_loan_available()
client.get_loans()
```

### SocketIO API
subscribe all messages
``` python
from huobi_client import StreamingClient
def on_message(data):
    print(data)
 
sclient = StreamingClient()
sclient.subscribe_all()
sclient.connect(on_message)
```
subscribe specific messages
``` python
from huobi_client import StreamingClient
def on_message(data):
    print(data)
 
sclient = StreamingClient()
sclient.subscribe('tradeDetail')
sclient.connect(on_message)
```

### Command Line Tool
```
$ huobi
usage: huobi [-h]
             {info,orders,oinfo,buy,sell,buym,sellm,cancel,norders,tid2oid,avail_loans,loans,stream}
             ...

huobi command line tool

positional arguments:
  {info,orders,oinfo,buy,sell,buym,sellm,cancel,norders,tid2oid,avail_loans,loans,stream}
    info                account info
    orders              orders
    oinfo               order info
    buy                 buy
    sell                sell
    buym                buy market
    sellm               sell market
    cancel              cancel order
    norders             get new deal order
    tid2oid             get order id by trade id
    avail_loans         get available loans
    loans               get loans
    stream              dump socketio data

optional arguments:
  -h, --help            show this help message and exit
```
