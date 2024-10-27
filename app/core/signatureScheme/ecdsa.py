import secrets
from app.core.ellipticCurve.ellipticCurve import Curve, Point
from app.core.utils import inverse_mod
from typing import Tuple


class Seed:
    E: Curve
    G: Point


class PublicKey:
    E: Curve
    G: Point
    Q: Point


class PrivateKey:
    E: Curve
    G: Point
    d: int


def generateKey(seed: Seed):
    E = seed.E
    n = E.field.n
    G = seed.G
    d = 1 + secrets.randbelow(n - 1)
    Q = G * d
    return (PrivateKey(E=E, G=G, d=d), PublicKey(E=E, G=G, Q=Q))


def H(self, x: int) -> int:
    return x


def sign(privateKey: PrivateKey, message: int) -> Tuple[int, int]:
    n = privateKey.E.field.n
    r = 0
    s = 0
    while s == 0:
        k = 1
        while r == 0:
            k = 1 + secrets.randbelow(n - 1)
            x = (privateKey.G * k).x
            r = x % (n)

        h = H(message)
        dr_mod_n = (privateKey.d * r) % (n)
        h_plus_dr_mod_n = (h + dr_mod_n) % (n)
        k_inv = inverse_mod(k, n)
        s = (h_plus_dr_mod_n * k_inv) % (n)

    return (r, s)


def verify(self, publicKey: PublicKey, message: int, r: int, s: int) -> bool:
    n = publicKey.E.field.n
    w = inverse_mod(s, n)
    h = H(message)
    u1 = (h * w) % (n)
    u2 = (r * w) % (n)
    x = (publicKey.G * u1 + publicKey.Q * u2).x
    v = x % (n)

    return v == r
