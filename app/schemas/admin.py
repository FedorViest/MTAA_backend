from pydantic import BaseModel

class AllRatingsOut(BaseModel):
    id: int
    rating: float
    comment: str

    class Config:
        orm_mode = True