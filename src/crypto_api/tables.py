import sqlalchemy as sa

from src.crypto_api.db import Base


class Currency(Base):
    __tablename__ = 'currency'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, unique=False)
    price = sa.Column(sa.FLOAT)
    time = sa.Column(sa.TIME)
