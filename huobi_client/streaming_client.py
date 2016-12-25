from .socketIO_client import SocketIO
import logging

VALID_PERIOD = {
    "1min", "5min", "15min", "30min", "60min",
    "1day", "1week", "1mon", "1year",
}
VALID_PERCENT = {10, 20, 50, 80, 100}
VALID_SYMBOL = {
    'lastTimeLine',
    'lastKLine',
    'marketDepthDiff',
    'marketDepthTopDiff',
    'marketDetail',
    'tradeDetail',
    'marketOverview',
}
logger = logging.getLogger(__name__)


class StreamingClient:
    '''
    sc = StreamingClient()
    sc.subscribe('lastTimeLine')
    sc.run(on_msg)
    '''
    def __init__(self):
        self._io = SocketIO('hq.huobi.com', 80)
        self.req_data = {
            'version': 1,
            'msgType': 'reqMsgSubscribe',
            'symbolList': {}
        }

    def subscribe(self, sym, period='1min', percent=10, currency='btccny'):
        symbol_list = self.req_data['symbolList']
        if sym in VALID_SYMBOL:
            d = {
                'symbolId': currency,
                'pushType': 'pushLong',
            }
            if sym == 'lastKLine':
                if period in VALID_PERIOD:
                    d['period'] = period
                else:
                    raise Exception('period must be in %s'
                                    % VALID_PERIOD)
            elif sym == 'marketDepthDiff':
                if percent in VALID_PERCENT:
                    d['percent'] = '%d' % percent
                else:
                    raise Exception('percent must be in %s'
                                    % VALID_PERCENT)
            # init symbol_list[sym]
            if sym not in symbol_list:
                symbol_list[sym] = []
            # append record
            if d not in symbol_list[sym]:
                symbol_list[sym].append(d)
        else:
            raise Exception('"%s" is not a valid symbol.'
                            'symbol must be in %s'
                            % (sym, set(symbol_list.keys())))

    def subscribe_all(self, currency='btccny'):
        for sym in VALID_SYMBOL:
            if sym == 'lastKLine':
                for period in VALID_PERIOD:
                    self.subscribe(sym, period=period,
                                   currency=currency)
            elif sym == 'marketDepthTopDiff':
                for percent in VALID_PERCENT:
                    self.subscribe(sym, percent=percent,
                                   currency=currency)
            else:
                self.subscribe(sym, currency=currency)

    def unsubscribe(self, sym, period='1min',
                    percent=10, currency='btccny'):
        raise NotImplementedError

    def _on_connect(self):
        logger.info('connect')
        self._io.emit('request', self.req_data)

    def _on_reconnect(self):
        logger.info('reconnected')

    def _on_disconnect(self):
        logger.info('disconnected')

    def _on_request(self, data):
        logger.info('request: %s' % data)

    def connect(self, on_msg):
        self._io.on('connect', self._on_connect)
        self._io.on('reconnect', self._on_reconnect)
        self._io.on('disconnect', self._on_disconnect)
        self._io.on('request', self._on_request)
        self._io.on('message', on_msg)
        self._io.wait()

# unused
# def timeline(on_msg, currency='btccny'):
#     data = {
#         'msgType': 'reqTimeLine',
#     }
#     _run_client(on_msg, data, currency)
#
#
# def kline(on_msg, period='1min', currency='btccny'):
#     data = {
#         'msgType': 'reqKLine',
#         'period': period,
#     }
#     _run_client(on_msg, data, currency)
#
#
# def market_depth_top(on_msg, currency='btccny'):
#     data = {
#         'msgType': 'reqMarketDepthTop',
#     }
#     _run_client(on_msg, data, currency)
#
#
# def market_depth(on_msg, percent=10, currency='btccny'):
#     data = {
#         'msgType': 'reqMarketDepth',
#         'percent': percent,
#     }
#     _run_client(on_msg, data, currency)
#
#
# def trade_detail_top(on_msg, count=None, currency='btccny'):
#     data = {
#         'msgType': 'reqTradeDetailTop',
#     }
#     if count:
#         data['count'] = count
#     _run_client(on_msg, data, currency)
#
#
# def market_detail(on_msg, currency='btccny'):
#     data = {
#         'msgType': 'reqMarketDetail',
#     }
#     _run_client(on_msg, data, currency)
#
#
# def _run_client(on_msg, data, currency):
#     sc = StreamingClient()
#     data['symbolId'] = currency
#     sc.req_data.update(data)
#     del sc.req_data['symbolList']
#     print(sc.req_data)
#     sc.run(on_msg)
