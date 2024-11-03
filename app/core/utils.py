from typing import Tuple
from app.core.generators import randomIntInRange


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


def mul_mod(a: int, b: int, p: int) -> int:
    return ((a % p) * (b % p)) % p


def powermod(a: int, b: int, p: int) -> int:
    return pow(a, b, p)


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def randomRelativePrime(p) -> int:
    k = randomIntInRange(2, p - 2)
    while gcd(k, p) != 1:
        k = randomIntInRange(2, p - 2)
    return k


def charToIndex(c: str) -> int:
    return ord(c.lower()) - ord("a") + 1


def indexToChar(i: int) -> str:
    return chr(ord("a") + i - 1)


def encodeString(message: str, alphabet_size: int = 2**8) -> int:
    return sum(ord(char) * (alphabet_size**i) for i, char in enumerate(message))


def decodeString(message_decimal: int, alphabet_size: int = 2**8) -> str:
    characters = []
    while message_decimal != 0:
        characters.append(chr(message_decimal % alphabet_size))
        message_decimal //= alphabet_size

    return "".join(characters)
