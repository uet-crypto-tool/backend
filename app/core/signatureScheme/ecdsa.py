import secrets
from app.core.ellipticCurve.domain import CurveDomainParamter
from app.core.ellipticCurve.point import Point, PointType
from app.core.utils import inverse_mod
from typing import Tuple
from pydantic import BaseModel


class Seed(BaseModel):
    curve_domain_name: str


class PublicKey(BaseModel):
    curve_domain_name: str
    Q: PointType


class PrivateKey(BaseModel):
    curve_domain_name: str
    d: int


def generateKey(curve_domain_name: str):
    E = CurveDomainParamter.get(curve_domain_name)
    n = E.n
    G = E.g
    d = 1 + secrets.randbelow(n - 1)
    Q = G * d
    return (PrivateKey(curve_domain_name=curve_domain_name, d=d),
            PublicKey(curve_domain_name=curve_domain_name, Q=Q.type()))


def H(x: int) -> int:
    return x


def sign(privateKey: PrivateKey, message: int) -> Tuple[int, int]:
    E = CurveDomainParamter.get(privateKey.curve_domain_name)
    G = E.g

    n = E.n
    r = 0
    s = 0
    while s == 0:
        k = 1
        while r == 0:
            k = 1 + secrets.randbelow(n - 1)
            x = (G * k).x
            r = x % (n)

        h = H(message)
        dr_mod_n = (privateKey.d * r) % (n)
        h_plus_dr_mod_n = (h + dr_mod_n) % (n)
        k_inv = inverse_mod(k, n)
        s = (h_plus_dr_mod_n * k_inv) % (n)

    return (r, s)


def verify(publicKey: PublicKey, message: int, signature: Tuple[int, int]) -> bool:
    E = CurveDomainParamter.get(publicKey.curve_domain_name)
    G = E.g
    Q = Point(E, publicKey.Q.x, publicKey.Q.y)
    r, s = signature

    n = E.n
    w = inverse_mod(s, n)
    h = H(message)
    u1 = (h * w) % (n)
    u2 = (r * w) % (n)
    x = (G * u1 + Q * u2).x
    v = x % (n)

    return v == r
