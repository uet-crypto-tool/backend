from typing import Tuple


def egcd(a, b) -> Tuple[int, int, int]:
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def inverse_mod(a: int, p: int) -> int:
    if a < 0:
        return p - inverse_mod(-a, p)
    g, x, y = egcd(a, p)
    if g != 1:
        raise ArithmeticError("Modular inverse does not exist")
    else:
        return x % p


def powermod(a: int, b: int, p: int) -> int:
    return pow(a, b, p)


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def xgcd(a: int, b: int) -> Tuple[int, int, int]:
    prevx, x = 1, 0
    prevy, y = 0, 1
    while b:
        q = int(a / b)
        x, prevx = prevx - q*x, x
        y, prevy = prevy - q*y, y
        a, b = b, a % b
    return a, prevx, prevy


def charToIndex(c: str) -> int:
    return ord(c.lower()) - ord('a') + 1


def indexToChar(i: int) -> str:
    return chr(ord('a') + i - 1)


def encodeString(m: str) -> int:
    return sum(
        [charToIndex(c) * 26 ** (len(m) - i - 1)
         for i, c in enumerate(m.lower())]
    )


def decodeString(n: int) -> str:
    res = ""
    while n > 0:
        n, i = divmod(n, 26)
        res = indexToChar(i) + res
    return res
