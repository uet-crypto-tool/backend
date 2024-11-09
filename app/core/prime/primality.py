from __future__ import annotations
from math import log10
import secrets
from app.core.prime.smallPrimes import smallPrimes
from app.core.prime.millerRabin import millerRabin


def genNum(length, lock):
    global possibleNum
    # global count
    while not possibleNum:
        x = secrets.randbits(length)
        # lock.acquire()
        # try:
        #  count += 1
        # finally:
        #  lock.release()
        if millerRabin(x):
            lock.acquire()
            try:
                possibleNum = x
            finally:
                lock.release()
    # print(str(threading.get_ident()) + ' closing, count=' + str(count))


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
        return millerRabin(n)
