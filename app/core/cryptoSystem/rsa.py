import secrets
from app.core.utils import inverse_mod, gcd, powermod, randomRelativePrime
from app.core.generators import randomIntInRange
from typing import Tuple
from pydantic import BaseModel


class Seed(BaseModel):
    p: int
    q: int


class PublicKey(BaseModel):
    n: int
    e: int


class PrivateKey(BaseModel):
    n: int
    d: int


def generateKey(seed: Seed) -> Tuple[PrivateKey, PublicKey]:
    p, q = seed.p, seed.q
    n = p * q
    phi_n = (p - 1) * (q - 1)
    d = randomRelativePrime(phi_n)
    e = inverse_mod(d, phi_n)
    return (PrivateKey(n=n, d=d), PublicKey(n=n, e=e))


def encrypt(publicKey: PublicKey, message: int) -> int:
    return powermod(message, publicKey.e, publicKey.n)


def decrypt(privateKey: PrivateKey, ecrypted_message: int) -> int:
    return powermod(ecrypted_message, privateKey.d, privateKey.n)
