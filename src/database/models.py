from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from src.data.config import database_url
import pandas as pd
import csv


engine = create_async_engine(url=database_url, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(50), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)


class Catalog(Base):
    __tablename__ = 'catalog'

    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(100), nullable=True)
    puffs: Mapped[str] = mapped_column(String(100), nullable=True)
    flavor: Mapped[str] = mapped_column(String(100), nullable=True)
    image: Mapped[str] = mapped_column(String(200), nullable=True)
    volume: Mapped[str] = mapped_column(String(200), nullable=True)
    nicotine: Mapped[str] = mapped_column(String(200), nullable=True)
    heat_element: Mapped[str] = mapped_column(String(200), nullable=True)
    battery: Mapped[str] = mapped_column(String(200), nullable=True)
    connector: Mapped[str] = mapped_column(String(200), nullable=True)
    compound: Mapped[str] = mapped_column(String(300), nullable=True)

class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    prod_id: Mapped[int] = mapped_column(nullable=True)
    amount: Mapped[int] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=True)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open(r'src/database/DB_ver06.csv', encoding='cp1251') as file:
        reader = csv.reader(file, delimiter=';')
        header = list(next(reader))
        all_products = []
        for row in reader:
            new_line = {k: v for k, v in zip(header, row)}
            all_products.append(new_line)
        df = pd.DataFrame(all_products)
        async with async_session() as session:
            for index, row in df.iterrows():
                record = Catalog(**{
                    'id': int(row[0]),
                    'brand': row[1],
                    'puffs': row[2],
                    'flavor': row[3],
                    'image': row[4],
                    'volume': row[5],
                    'nicotine': row[6],
                    'heat_element': row[7],
                    'battery': row[8],
                    'connector': row[9],
                    'compound': row[10]
                })
                session.add(record)

            await session.commit()

