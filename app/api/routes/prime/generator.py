from fastapi import APIRouter
from app.core.prime.generator import generateProbablePrime, randomRelativePrime
from pydantic import BaseModel

router = APIRouter()


class GeneratePrimeRequest(BaseModel):
    bit_length: int


@router.post("/generate")
async def generate_prime_has_bit_length(req: GeneratePrimeRequest) -> int:
    return generateProbablePrime(req.bit_length)


@router.post("/generate_relative_prime")
async def generate_relative_prime(p: int) -> int:
    return randomRelativePrime(p)
