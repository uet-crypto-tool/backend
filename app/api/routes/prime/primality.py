from fastapi import APIRouter
from app.core.prime import aks, millerRabin, primality
from pydantic import BaseModel

router = APIRouter()


class PrimeCheckRequest(BaseModel):
    number: int


class Result(BaseModel):
    isPrime: bool


@router.post("/aks/check", response_model=Result)
async def aks_check(req: PrimeCheckRequest):
    return Result(isPrime=aks.isPrime(req.number))


@router.post("/miller_rabbin/check", response_model=Result)
async def miller_rabbin_check(req: PrimeCheckRequest):
    return Result(isPrime=millerRabin.isPrime(req.number))


@router.post("/check", response_model=Result)
async def default_check(req: PrimeCheckRequest):
    return Result(isPrime=primality.isPrime(req.number))
