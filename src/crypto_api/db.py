
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    'postgresql://fastapi:fastapi@localhost:5432/fastapi',
    # connect_args={'check_same_thread': False}  # For SQLite
)

Session = sessionmaker(
    engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


def get_session() -> Session:
    session = Session()
    try:
        yield session
    finally:
        session.close()
