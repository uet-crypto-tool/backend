import secrets
from app.core.utils import powermod, gcd, mul_mod, randomRelativePrime
from app.core.generators import randomIntInRange
from typing import Tuple
from pydantic import BaseModel


class Seed(BaseModel):
    p: int
    a: int


class PrivateKey(BaseModel):
    p: int
    a: int


class PublicKey(BaseModel):
    p: int
    alpha: int
    beta: int


def generateKey(seed: Seed) -> Tuple[PrivateKey, PublicKey]:
    alpha = randomRelativePrime(seed.p)
    beta = powermod(alpha, seed.a, seed.p)
    return (PrivateKey(p=seed.p, a=seed.a), PublicKey(p=seed.p, alpha=alpha, beta=beta))


def encrypt(publicKey: PublicKey, message: int) -> Tuple[int, int]:
    k = randomIntInRange(1, publicKey.p - 1)
    y1 = powermod(publicKey.alpha, k, publicKey.p)
    y2 = mul_mod(message, powermod(publicKey.beta, k, publicKey.p), publicKey.p)
    return (y1, y2)


def decrypt(privateKey: PrivateKey, encrypted_message: Tuple[int, int]) -> int:
    y1, y2 = encrypted_message
    return mul_mod(y2, powermod(y1, -privateKey.a, privateKey.p), privateKey.p)
