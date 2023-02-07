import asyncio
import os

from fastapi import FastAPI, Depends
from fastapi_utils.tasks import repeat_every

from src.crypto_api import tables
from src.crypto_api.API_Binance import router as BinanceRouter
from src.crypto_api.db import Base, engine, get_session, Session
import httpx as httpx

url_update = os.getenv('URL_UPDATE')
url_check = os.getenv('URL_CHECK')

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Crypto prices',
    description='Курс криптовалют',
    version='1.0.0',
)

app.include_router(BinanceRouter)


@app.get("/")
async def root():
    return {"message": "Hello World"}


async def request_update_price(client):
    response = await client.post(url_update)
    return response.text


async def request_check_price(client):
    response = await client.get(url_check)
    return response.text


@app.on_event("startup")
@repeat_every(seconds=1)
async def task():
    async with httpx.AsyncClient() as client:
        tasks = [request_update_price(client) for i in range(1)]
        result = await asyncio.gather(*tasks)


@app.on_event("startup")
@repeat_every(seconds=2)
async def task():
    async with httpx.AsyncClient() as client:
        tasks = [request_check_price(client) for i in range(1)]
        result = await asyncio.gather(*tasks)
        print(result)
