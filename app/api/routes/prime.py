from fastapi import APIRouter
from app.core.prime.primality import isPrime
from app.core.prime.generator import generateProbablePrime
from pydantic import BaseModel

router = APIRouter()


class CheckPrimeRequest(BaseModel):
    number: int


class GeneratePrimeRequest(BaseModel):
    bitLength: int


@router.post("/check")
async def check_prime(req: CheckPrimeRequest):
    return {"isPrime": isPrime(req.number)}


@router.post("/generate")
async def generate_prime_has_bit_length(req: GeneratePrimeRequest) -> int:
    return generateProbablePrime(req.bitLength)
