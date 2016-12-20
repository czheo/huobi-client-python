from socketIO_client import SocketIO
import logging

VALID_PERIOD = {
    "1min", "5min", "15min", "30min", "60min",
    "1day", "1week", "1mon", "1year",
}
VALID_PERCENT = {10, 20, 50, 80, 100}
VALID_CURRENCY = {'btc', 'ltc'}
logger = logging.getLogger(__name__)


class StreamingClient:
    def __init__(self, currency='btc'):
        if currency in VALID_CURRENCY:
            self._currency = currency
        else:
            raise Exception('"%s" is no a valid currency.'
                            'currency must be in %s'
                            % (currency, VALID_CURRENCY))
        self._io = SocketIO('hq.huobi.com', 80)
        self._req_data = {
            'version': 1,
            'msgType': 'reqMsgSubscribe',
            'symbolList': {
                'lastTimeLine': [],
                'lastKLine': [],
                'marketDepthDiff': [],
                'marketDepthTopDiff': [],
                'marketDetail': [],
                'tradeDetail': [],
                'marketOverview': [],
            }
        }

    def disconnect(self):
        self._io.disconnect()

    def _on_connect(self):
        logger.info('connected')
        self._io.emit('request', self._req_data)

    def _on_reconnect(self):
        logger.info('reconnected')
        self._io.emit('request', self._req_data)

    def _on_disconnect(self):
        logger.info('disconnected')

    def _on_request(self, data):
        logger.info('request: %s' % data)

    def run(self, on_msg):
        self._io.on('connect', self._on_connect)
        self._io.on('request', self._on_request)
        self._io.on('message', on_msg)
        self._io.on('reconnect', self._on_reconnect)
        self._io.on('disconnect', self._on_disconnect)
        self._io.wait()

    def register_symbol(self, sym, period='1min', percent=10):
        symbol_list = self._req_data['symbolList']
        if sym in symbol_list:
            d = {
                'symbolId': '%scny' % self._currency,
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
            symbol_list[sym].append(d)
        else:
            raise Exception('"%s" is not a valid symbol.'
                            'symbol must be in %s'
                            % (sym, set(symbol_list.keys())))

    def register_all_symbols(self):
        symbol_list = self._req_data['symbolList']
        for sym in symbol_list:
            if sym == 'lastKLine':
                for period in VALID_PERIOD:
                    self.register_symbol(sym, period=period)
            elif sym == 'marketDepthTopDiff':
                for percent in VALID_PERCENT:
                    self.register_symbol(sym, percent=percent)
            else:
                self.register_symbol(sym)
