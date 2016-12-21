from streaming_client import StreamingClient
import logging
import json


def on_msg(data):
    print(data['msgType'])

logging.basicConfig(level=logging.INFO)
sc = StreamingClient()
sc.register_all_symbols()
sc.run(on_msg)
