from sqlalchemy import Column, String, Integer, DateTime, Numeric, Enum
from datetime import datetime
from app.database import Base
from app.types import OrderType, OrderSide

# SQLAlchemy model
class OrderDB(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    type_ = Column(Enum(OrderType), nullable=False)
    side = Column(Enum(OrderSide), nullable=False)
    instrument = Column(String(12), nullable=False)
    limit_price = Column(Numeric(10, 2), nullable=True)
    quantity = Column(Integer, nullable=False)
    status = Column(String, default="pending")
