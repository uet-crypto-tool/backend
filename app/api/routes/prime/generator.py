from fastapi import APIRouter
from app.core.prime.generator import generateProbablePrime, randomRelativePrime
from pydantic import BaseModel

router = APIRouter()


class GeneratePrimeRequest(BaseModel):
    bit_length: int


@router.post(
    "/generate", summary="Generate a probable prime number with specified bit length"
)
async def generate_prime_has_bit_length(req: GeneratePrimeRequest):
    return {"prime": str(generateProbablePrime(req.bit_length))}


@router.post(
    "/generate_relative_prime",
    summary="Generate a random number that is relatively prime to the specified integer",
)
async def generate_relative_prime(p: int):
    return {"relative_prime": str(randomRelativePrime(p))}
