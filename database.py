# database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
engine = create_engine('sqlite:///./data/database.db', echo=True)
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    name = Column(String)
    phone = Column(String)
    address = Column(String)
    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id'))
    flower = Column(String)
    quantity = Column(Integer)
    wrapping = Column(String)
    total_price = Column(Float)
    status = Column(String, default="В обработке")
    user = relationship("User", back_populates="orders")

def init_db():
    Base.metadata.create_all(bind=engine)