import asyncio
import json
import time

from binance import Client
from fastapi import Depends

from crypto_api import tables
from crypto_api.db import Session, get_session

api_key = '2BOFhBZGUHIrGxCuiISYNi9jBnbV9AKjcJEEO4JAWAk8dYsNRHQkojD1siLAZEXa'
api_secret = 'tfVLarrAI8nuJSS43Y2b9rPQN678m7MLYxQngycOZfo8wfczped44HFR5xhLUG50'


async def get_price(symbol: str):
    client = Client(api_key, api_secret)

    # fetch exchange info
    res = client.get_symbol_ticker(symbol=symbol)
    response = json.dumps(res, indent=2)
    data = json.loads(response)
    print(data['price'])

    client.close_connection()


# def check_change_ratio(session: Session = Depends(get_session)):
#     last_price = session.query(tables.Currency) \
#             .first()
#     print(last_price)

if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # for i in range(100):
    #     loop.run_until_complete(get_price('XRPUSDT'))
    # check_change_ratio()



    # print(time.time())
