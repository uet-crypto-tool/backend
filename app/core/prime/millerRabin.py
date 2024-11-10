from __future__ import annotations
from math import log10, log, floor
from app.core.utils import fastPower
from app.core.prime.smallPrimes import smallPrimes


def isPrime(n: int, warnings: bool = False) -> bool:
    """
    Performs the Miller-Rabin Test on possible prime n\n
    Input:
      integers n
      boolean warnings (optional, show warnings)
    Outputs:
      boolean m (false if composite, true if "probably prime")
    """
    # https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test#Accuracy

    # If the generalized Riemann hypothesis is true, Miller-Rabin can be made deterministic
    if not n > 1:
        raise Exception("MillerRabin(): n must be strictly greater than 1")
    # Express as n = 2^r*d + 1
    d = n - 1
    r = 0
    while d % 2 == 0:
        r += 1
        d = d // 2

    witnessRange = min([n - 2, floor(2 * (log(n) ** 2))])
    aIndex = 0
    while smallPrimes[aIndex] < witnessRange:
        x = fastPower(smallPrimes[aIndex], d, n)
        if x == 1 or x == n - 1:
            # Failure to find a witness
            aIndex += 1
            if aIndex == len(smallPrimes):
                if warnings:
                    print(
                        "List of small primes for Miller-Rabin bases has been exhausted for n="
                        + str(n)
                    )
                    print("The result is probabalistically determined to be prime.")
                return True
            continue
        failure = False
        for i in range(r - 1):
            x = fastPower(x, 2, n)
            if x == n - 1:
                # Failure to find a witness
                aIndex += 1
                if aIndex == len(smallPrimes):
                    if warnings:
                        print(
                            "List of small primes for Miller-Rabin bases has been exhausted for n="
                            + str(n)
                        )
                        print("The result is probabalistically determined to be prime.")
                    return True
                failure = True
        if not failure:
            return False
    return True
