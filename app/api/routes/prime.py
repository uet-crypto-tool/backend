from fastapi import APIRouter
from app.core import primality
from app.core import generators
from pydantic import BaseModel

router = APIRouter()


class CheckPrimeRequest(BaseModel):
    number: int


class GeneratePrimeRequest(BaseModel):
    bitLength: int


@router.post("/check")
async def check_prime(req: CheckPrimeRequest):
    return {"isPrime": primality.isPrime(req.number)}


@router.post("/generate")
async def generate_prime_has_bit_length(req: GeneratePrimeRequest):
    return generators.generateProbablePrime(req.bitLength)
