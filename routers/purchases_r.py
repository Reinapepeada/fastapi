from fastapi import APIRouter, Header


router = APIRouter()


@router.get("/")
def main_purchase():
    return {"msg": "welcome to purchases"}

