import secrets
from app.core.utils import inverse_mod, powermod, gcd
from typing import Tuple
from pydantic import BaseModel, validator
from app.core.primality import isPrime


class Seed(BaseModel):
    p: int
    a: int

    @validator('p')
    def check_prime(cls, value):
        if not isPrime(value):
            raise ValueError(f"{value} is not a prime number")
        return value


class PrivateKey(BaseModel):
    p: int
    a: int

    @validator('p')
    def check_prime(cls, value):
        if not isPrime(value):
            raise ValueError(f"{value} is not a prime number")
        return value


class PublicKey(BaseModel):
    p: int
    alpha: int
    beta: int

    @validator('p')
    def check_prime(cls, value):
        if not isPrime(value):
            raise ValueError(f"{value} is not a prime number")
        return value


def generateKey(seed: Seed) -> Tuple[PrivateKey, PublicKey]:
    alpha = randomRelativePrime(seed.p)
    beta = powermod(alpha, seed.a, seed.p)
    return (PrivateKey(p=seed.p, a=seed.a), PublicKey(p=seed.p, alpha=alpha,
                                                      beta=beta))


def randomRelativePrime(p) -> int:
    k = 2 + secrets.randbelow(p - 2)
    while gcd(k, p - 1) != 1:
        k = 2 + secrets.randbelow(p - 2)
    return k


def encrypt(publicKey: PublicKey,  message: int) -> Tuple[int, int]:
    k = 1 + secrets.randbelow(publicKey.p - 1)
    y1 = powermod(publicKey.alpha, k, publicKey.p)
    y2 = (message * powermod(publicKey.beta, k, publicKey.p)) % (publicKey.p)
    return (y1, y2)


def decrypt(privateKey: PrivateKey, encrypted_message: Tuple[int, int]) -> int:
    y1, y2 = encrypted_message
    return (y2 * powermod(y1, -privateKey.a, privateKey.p)) % (privateKey.p)
