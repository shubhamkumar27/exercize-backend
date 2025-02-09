import uuid
from sqlalchemy.orm import Session
from app.models import OrderDB
from app.types import Order
from app.stock_exchange import place_order, OrderPlacementError
from celery import Celery
from app.database import SessionLocal

celery = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=['app.services'],
)

def create_order(db: Session, order_data) -> Order:
    order_id = str(uuid.uuid4())
    order_db = OrderDB(id=order_id, **order_data.dict(), status="pending")

    db.add(order_db)
    db.flush()
    db.commit()
    db.refresh(order_db)
    task = place_order_async.delay(order_db.id)
    return order_db

@celery.task(bind=True, max_retries=3)
def place_order_async(self, order_id: str):
    db = SessionLocal()
    try:
        order_db = db.query(OrderDB).filter(OrderDB.id == order_id).first()

        if not order_db:
            raise ValueError("Order not found %s", order_id)

        place_order(order_db)

        order_db.status = "placed"
        db.commit()
    except OrderPlacementError as e:
        print("failed to place order")
        self.retry(exc=e, countdown=5)
    finally:
        db.close()

