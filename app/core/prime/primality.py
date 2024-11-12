from __future__ import annotations
from math import log10
from app.core.prime.smallPrimes import smallPrimes
from app.core.prime import millerRabin


def isPrime(n: int) -> bool:
    """
    Determines probabalistically if a number is prime\n
    Input:
      integer n
    Outputs:
      boolean p (false if composite, true if "probably prime")
    """
    if n % 2 == 0 and n != 2:
        return False

    length = log10(n)

    if length < 4:
        # Use lookup table
        if n in smallPrimes:
            return True
        else:
            return False
    else:
        return millerRabin.isPrime(n)
