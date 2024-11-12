from typing import Tuple
import secrets


def fastPower(b: int, e: int, m: int) -> int:
    """
    Efficiently computes (b^e) % m using binary exponentiation.

    Args:
        b (int): The base.
        e (int): The exponent.
        m (int): The modulus.

    Returns:
        int: The result of (b^e) % m.
    """
    b %= m
    e %= m

    r = 1
    if 1 & e:
        r = b
    while e:
        e >>= 1
        b = (b * b) % m
        if e & 1:
            r = (r * b) % m
    return r


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Extended Euclidean Algorithm to find the greatest common divisor (gcd)
    of two numbers a and b, along with coefficients for the linear combination.

    Args:
        a (int): First number.
        b (int): Second number.

    Returns:
        Tuple[int, int, int]: A tuple (gcd, x, y) such that a*x + b*y = gcd.
    """
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def inverse_mod(a: int, p: int) -> int:
    """
    Computes the modular inverse of a modulo p, if it exists.

    Args:
        a (int): The number to find the inverse of.
        p (int): The modulus.

    Returns:
        int: The modular inverse of a modulo p.

    Raises:
        ArithmeticError: If the modular inverse does not exist (i.e., gcd(a, p) != 1).
    """
    if a < 0:
        return p - inverse_mod(-a, p)
    g, x, y = egcd(a, p)
    if g != 1:
        raise ArithmeticError("Modular inverse does not exist")
    else:
        return x % p


def mul_mod(a: int, b: int, p: int) -> int:
    """
    Multiplies two numbers a and b modulo p.

    Args:
        a (int): First number.
        b (int): Second number.
        p (int): The modulus.

    Returns:
        int: The result of (a * b) % p.
    """
    return ((a % p) * (b % p)) % p


def powermod(a: int, b: int, p: int) -> int:
    """
    Computes (a^b) % p using the fastPower function.

    Args:
        a (int): The base.
        b (int): The exponent.
        p (int): The modulus.

    Returns:
        int: The result of (a^b) % p.
    """
    return fastPower(a, b, p)


def gcd(a: int, b: int) -> int:
    """
    Computes the greatest common divisor (gcd) of a and b.

    Args:
        a (int): First number.
        b (int): Second number.

    Returns:
        int: The gcd of a and b.
    """
    while b:
        a, b = b, a % b
    return a


def charToIndex(c: str) -> int:
    """
    Converts a character to an integer index, where 'a' is 1, 'b' is 2, etc.

    Args:
        c (str): The character to convert.

    Returns:
        int: The integer index of the character.
    """
    return ord(c.lower()) - ord("a") + 1


def indexToChar(i: int) -> str:
    """
    Converts an integer index to a character, where 1 maps to 'a', 2 to 'b', etc.

    Args:
        i (int): The integer index.

    Returns:
        str: The character corresponding to the index.
    """
    return chr(ord("a") + i - 1)


def encodeString(message: str, alphabet_size: int = 2**8) -> int:
    """
    Encodes a string into a large integer using a specified alphabet size.

    Args:
        message (str): The message to encode.
        alphabet_size (int): The size of the alphabet (default is 256 for ASCII).

    Returns:
        int: The encoded integer representation of the string.
    """
    return sum(ord(char) * (alphabet_size**i) for i, char in enumerate(message))


def decodeString(message_decimal: int, alphabet_size: int = 2**8) -> str:
    """
    Decodes an integer message into a string using a specified alphabet size.

    Args:
        message_decimal (int): The encoded integer message to decode.
        alphabet_size (int): The size of the alphabet (default is 256 for ASCII).

    Returns:
        str: The decoded string.
    """
    characters = []
    while message_decimal != 0:
        characters.append(chr(message_decimal % alphabet_size))
        message_decimal //= alphabet_size

    return "".join(characters)


def randomIntInRange(lower: int, upper: int) -> int:
    """
    Generates a random integer in the range [lower, upper].

    Args:
        lower (int): The lower bound (inclusive).
        upper (int): The upper bound (inclusive).

    Returns:
        int: A random integer in the specified range.
    """
    return lower + secrets.randbelow(upper - lower + 1)
