import asyncio
from datetime import datetime
import os

from dotenv import load_dotenv
import json

from binance import AsyncClient, Client
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.crypto_api.db import get_session
from src.crypto_api import tables

load_dotenv()
key = os.getenv('BINANCE_KEY')
secret = os.getenv('BINANCE_SECRET')

router = APIRouter(
    prefix='/binance',
    tags=['Binance']
)


class BinanceService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def update_price(self,
                           symbol: str, ):
        client = AsyncClient(key, secret)

        # fetch exchange info
        res = await client.get_symbol_ticker(symbol=symbol)
        print(res)
        response = json.dumps(res, indent=2)
        data = json.loads(response)
        client.close_connection()
        print(data)
        result = {
            'name': f'{symbol}',
            'price': f"{data['price']}",
            'time': f'{datetime.utcnow()}'
        }
        currency_course = tables.Currency(**result)
        self.session.add(currency_course)
        self.session.commit()

        return data['price']

    def check_ratio_of_change(self):
        last_price = self.session.query(tables.Currency).order_by(-tables.Currency.id).first()
        curr_price = last_price.price
        curr_id = last_price.id
        rps = 1
        sec_in_hour = 60 * 60
        prev_id = curr_id - sec_in_hour * rps  # тут сделано аппроксимация расчёта времени, нет точного отсчета ,
                                                # но есть примерный час
        if prev_id < 0:
            prev_price = self.session.query(tables.Currency).first()
        else:
            prev_price = self.session.query(tables.Currency).get(prev_id)
        percent_of_change = (curr_price - prev_price.price)/prev_price.price * 100
        if percent_of_change >= 1 or \
            percent_of_change <= -1:
            return '!!!!!!!!!!!     Price was changed more than one percent' \
                   f'               Percent = {percent_of_change}'
        else:
            return '!!!!!!!!!!!!    Price within permitted borders' \
                   f'               Percent = {percent_of_change}'


@router.post('/update_price')
async def update_price(
        service: BinanceService = Depends()
):
    response = await service.update_price('XRPUSDT')
    return response


@router.get('/check')
async def update_price(
        service: BinanceService = Depends()
):
    return service.check_ratio_of_change()

