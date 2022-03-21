from fastapi import APIRouter

router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)