from client import Client
from pprint import pprint
import argparse


def main(args):
    c = Client()
    if args.command == 'info':
        pprint(c.get_account_info())
    elif args.command == 'orders':
        pprint(c.get_orders())
    elif args.command == 'oinfo':
        pprint(c.get_order_info(args.id))
    elif args.command == 'buy':
        pprint(c.buy(args.price, args.amount))
    elif args.command == 'sell':
        pprint(c.sell(args.price, args.amount))
    elif args.command == 'buym':
        pprint(c.buy_market(args.amount))
    elif args.command == 'sellm':
        pprint(c.sell_market(args.amount))
    elif args.command == 'cancel':
        pprint(c.cancel_order(args.id))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='huobi',
                                     description='huobi command line tool')
    subparsers = parser.add_subparsers(dest='command')
    # info
    parser_info = subparsers.add_parser('info', help='account info')
    # orders
    parser_orders = subparsers.add_parser('orders', help='orders')
    # oinfo
    parser_oinfo = subparsers.add_parser('oinfo', help='order info')
    parser_oinfo.add_argument('id')
    # buy
    parser_buy = subparsers.add_parser('buy', help='buy')
    parser_buy.add_argument('price', type=float)
    parser_buy.add_argument('amount', type=float)
    # sell
    parser_sell = subparsers.add_parser('sell', help='sell')
    parser_sell.add_argument('price', type=float)
    parser_sell.add_argument('amount', type=float)
    # buy_market
    parser_buym = subparsers.add_parser('buym', help='buy market')
    parser_buym.add_argument('amount', type=float)
    # sell_market
    parser_sellm = subparsers.add_parser('sellm', help='sell market')
    parser_sellm.add_argument('amount', type=float)
    # cancel order
    parser_cancel = subparsers.add_parser('cancel', help='cancel order')
    parser_cancel.add_argument('id')

    args = parser.parse_args()
    if args.command:
        main(args)
    else:
        parser.print_help()
