from pydantic import BaseModel


class updateOrderStateIn(BaseModel):
    status: str


class updateOrderStateOut(BaseModel):
    status: str

    class Config:
        orm_mode = True
