from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
metadata = MetaData()

data_table = Table(
    'data', metadata,
    Column('id', Integer, primary_key=True),
    Column('intensity', Integer),
    Column('likelihood', Integer),
    Column('relevance', Integer),
    Column('year', Integer),
    Column('country', Text),
    Column('topics', Text),
    Column('region', Text),
    Column('city', Text),
)

if __name__ == "__main__":
    metadata.create_all(engine)
    print("✅ Table 'data' created successfully.")
