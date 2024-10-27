from fastapi import APIRouter
from app.core import primality
from app.core import generators
from pydantic import BaseModel

router = APIRouter()


class checkPrimeRequest(BaseModel):
    number: int


@router.post("/check")
async def isPrime(req: checkPrimeRequest):
    return {"isPrime": primality.isPrime(req.number)}


class generatePrimeRequest(BaseModel):
    bitLength: int


@router.post("/generate")
async def generatePrime(req: generatePrimeRequest):
    return generators.generateProbablePrime(req.bitLength)
