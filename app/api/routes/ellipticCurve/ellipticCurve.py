from fastapi import APIRouter
from app.ellipticCurve import ellipticCurve

router = APIRouter()


@router.get("/getPoints")
async def getPoints(msg: str):
    return ellipticCurve.getPoints()
