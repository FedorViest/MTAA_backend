from pydantic import BaseModel


class updateOrderStateIn(BaseModel):
    status: str


class updateOrderStateOut(BaseModel):
    status: str

    class Config:
        orm_mode = True


class getRepairsOut(BaseModel):
    id: str
    customer_id: str
    pc_id: str
    status: str
    issue: str

    class Config:
        orm_mode = True
