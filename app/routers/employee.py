from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.schemas.employee import *
from app.database import connect_to_db
from sqlalchemy.orm import Session
from app.models import *
from app.schemas.employee import *

router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)


@router.put("/updateOrderState/{order_id}", response_model=updateOrderStateOut)
def update_order(order_info: updateOrderStateIn, order_id: int, db_conn: Session = Depends(connect_to_db)):
    query_result = db_conn.query(Orders).filter(Orders.id == order_id)

    if not query_result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Order not found")

    query_result.update(order_info.dict())
    db_conn.commit()

    return order_info.dict()
