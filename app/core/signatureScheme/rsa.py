import secrets
from app.core.utils import inverse_mod, gcd, powermod
from app.core.generators import randomIntInRange
from pydantic import BaseModel
from typing import Tuple


class Seed(BaseModel):
    p: int
    q: int


class PrivateKey(BaseModel):
    n: int
    e: int


class PublicKey(BaseModel):
    n: int
    d: int


def generateKey(seed: Seed) -> Tuple[PrivateKey, PublicKey]:
    p = seed.p
    q = seed.q
    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = generatePrivateKey(phi_n)
    d = inverse_mod(e, phi_n)

    return (PrivateKey(n=n, e=e), PublicKey(n=n, d=d))


def generatePrivateKey(phi_n) -> int:
    k = randomIntInRange(2, phi_n - 1)
    while gcd(k, phi_n) != 1:
        k = randomIntInRange(2, phi_n - 1)
    return k


def H(m: int) -> int:
    return m


def sign(privateKey: PrivateKey, message: int) -> int:
    return powermod(H(message), privateKey.e, privateKey.n)


def verify(publicKey: PublicKey, message: int, signature: int) -> bool:
    return H(message) == powermod(signature, publicKey.d, publicKey.n)
