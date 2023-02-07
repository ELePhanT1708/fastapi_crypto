from datetime import datetime

from pydantic import BaseModel


class BaseCurrency(BaseModel):
    name: int
    price: float
    timestamp: datetime
