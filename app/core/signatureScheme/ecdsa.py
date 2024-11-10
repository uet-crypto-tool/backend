from app.core.ellipticCurve.domain import CurveDomainParamter
from app.core.ellipticCurve.point import Point
from app.core.utils import inverse_mod, mul_mod, randomIntInRange
from typing import Tuple
import hashlib


def generateKey(curve_name: str) -> Tuple[str, int, Point]:
    curve = CurveDomainParamter.get(curve_name)
    d = randomIntInRange(1, curve.n - 1)
    Q = curve.g * d
    return curve_name, d, Q



def H(message: str, n: int) -> int:
    return int(hashlib.sha512(message.encode()).hexdigest(), 16) % n


def sign(curve_name: str, d: int, message: str) -> Tuple[int, int]:
    curve = CurveDomainParamter.get(curve_name)
    G = curve.g
    n = curve.n
    r = 0
    s = 0
    while s == 0:
        k = 1
        while r == 0:
            k = randomIntInRange(1, n - 1)
            x = (G * k).x
            r = x % n

        hashed_message = H(message, n)
        dr_mod_n = mul_mod(d, r, n)
        h_plus_dr_mod_n = (hashed_message  + dr_mod_n) % (n)
        k_inv = inverse_mod(k, n)
        s = mul_mod(h_plus_dr_mod_n, k_inv, n)

    return r, s


def verify(curve_name: str, Q: Point, message: str, signature: Tuple[int, int]) -> bool:
    curve = CurveDomainParamter.get(curve_name)
    G = curve.g
    r, s = signature

    n = curve.n
    w = inverse_mod(s, n)
    h = H(message, n)
    u1 = mul_mod(h, w, n)
    u2 = mul_mod(r, w, n)
    x = (G * u1 + Q * u2).x
    v = x % n

    return v == r
