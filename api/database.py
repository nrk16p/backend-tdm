from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,          # connections ที่เปิดค้างไว้
    max_overflow=20,       # connections พิเศษเมื่อ pool เต็ม
    pool_timeout=30,       # วินาทีที่รอก่อน raise error
    pool_recycle=1800,     # recycle connection ทุก 30 นาที (ป้องกัน stale)
    pool_pre_ping=True,    # ping ก่อนใช้งาน (ตรวจว่า connection ยังใช้ได้)
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
