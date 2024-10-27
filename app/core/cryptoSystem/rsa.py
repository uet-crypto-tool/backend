import secrets
from app.core.utils import inverse_mod, gcd, powermod
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
    p = seed.p
    q = seed.q
    n = p * q
    phi_n = (p - 1) * (q - 1)

    d = generatePrivateKey(phi_n)
    e = inverse_mod(d, phi_n)

    return (PrivateKey(n=n, d=d), PublicKey(n=n, e=e))


def generatePrivateKey(phi_n) -> int:
    k = 2 + secrets.randbelow(phi_n - 1)
    while gcd(k, phi_n) != 1:
        k = 2 + secrets.randbelow(phi_n - 1)
    return k


def encrypt(publicKey: PublicKey, message: int) -> int:
    return powermod(message, publicKey.e, publicKey.n)


def decrypt(privateKey: PrivateKey, ecrypted_message: int) -> int:
    return powermod(ecrypted_message, privateKey.d, privateKey.n)
