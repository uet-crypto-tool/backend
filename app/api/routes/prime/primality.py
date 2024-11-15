from fastapi import APIRouter
from app.core.prime import aks, millerRabin, primality
from pydantic import BaseModel

router = APIRouter()


class PrimeCheckRequest(BaseModel):
    number: int


class Result(BaseModel):
    isPrime: bool


@router.post(
    "/aks/check",
    response_model=Result,
    summary="Check if a number is prime using the AKS primality test",
)
async def aks_check(req: PrimeCheckRequest):
    return Result(isPrime=aks.isPrime(req.number))


@router.post(
    "/miller_rabbin/check",
    response_model=Result,
    summary="Check if a number is prime using the Miller-Rabin primality test",
)
async def miller_rabbin_check(req: PrimeCheckRequest):
    return Result(isPrime=millerRabin.isPrime(req.number))


@router.post(
    "/check",
    response_model=Result,
    summary="Check if a number is prime using a default primality test",
)
async def default_check(req: PrimeCheckRequest):
    return Result(isPrime=primality.isPrime(req.number))
