import secrets
from app.core.utils import inverse_mod, powermod, gcd
from app.core.primality import isPrime
from typing import Tuple
from pydantic import BaseModel, field_validator


class Seed(BaseModel):
    p: int
    a: int

    @field_validator('p')
    def check_prime(cls, value):
        if not isPrime(value):
            raise ValueError(f"{value} is not a prime number")
        return value


class PublicKey(BaseModel):
    p: int
    alpha: int
    beta: int

    @field_validator('p')
    def check_prime(cls, value):
        if not isPrime(value):
            raise ValueError(f"{value} is not a prime number")
        return value


class PrivateKey(BaseModel):
    p: int
    a: int
    alpha: int

    @field_validator('p')
    def check_prime(cls, value):
        if not isPrime(value):
            raise ValueError(f"{value} is not a prime number")
        return value


def generateKey(seed: Seed) -> Tuple[PrivateKey, PublicKey]:
    p = seed.p
    a = seed.a
    alpha = randomRelativePrime(p)
    beta = powermod(alpha, a, p)
    return (PrivateKey(p=p, a=a, alpha=alpha), PublicKey(p=p, alpha=alpha, beta=beta))


def randomRelativePrime(p) -> int:
    k = 2 + secrets.randbelow(p - 2)
    while gcd(k, p - 1) != 1:
        k = 2 + secrets.randbelow(p - 2)
    return k


def H(message: int) -> int:
    return message


def sign(privateKey: PrivateKey, message: int) -> Tuple[int, int]:
    k = randomRelativePrime(privateKey.p)
    y1 = powermod(privateKey.alpha, k, privateKey.p)

    ay1_mod = (privateKey.a * y1) % (privateKey.p - 1)
    h_minus_ay1_mod = (H(message) - ay1_mod) % (privateKey.p - 1)
    k_inv = inverse_mod(k, privateKey.p - 1)
    y2 = (h_minus_ay1_mod * k_inv) % (privateKey.p - 1)
    return (y1, y2)


def verify(publicKey: PublicKey, message: int, signature: Tuple[int, int]) -> bool:
    y1, y2 = signature
    v1 = (powermod(publicKey.beta, y1, publicKey.p) *
          powermod(y1, y2, publicKey.p)) % (publicKey.p)
    v2 = powermod(publicKey.alpha, H(message), publicKey.p)
    return v1 == v2
