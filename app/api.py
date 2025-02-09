from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.services import create_order
from app.types import Order, CreateOrderResponseModel, CreateOrderModel
from app.models import OrderDB
from typing import List

app = FastAPI()

# Initialize database
init_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/orders",status_code=201,response_model=CreateOrderResponseModel,response_model_by_alias=True,)
async def create_order_endpoint(model: CreateOrderModel, db: Session = Depends(get_db)):
    try:
        order = create_order(db, model)
        return Order.from_orm(order)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error while placing the order")
    

@app.get("/orders/{order_id}", response_model=CreateOrderResponseModel)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/orders", response_model=List[CreateOrderResponseModel])
def get_orders(db: Session = Depends(get_db)):
    return db.query(OrderDB).all()