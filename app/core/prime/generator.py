import secrets
import threading
import requests
from app.core.prime.primality import isPrime
from app.core.utils import gcd, randomIntInRange


def genNum(length, lock):
    """
    Attempts to generate a prime number of the specified bit length.

    This function runs in a loop until a prime number is found, at which point it updates
    the global `possibleNum` variable. It uses a lock to ensure thread safety during
    the update of `possibleNum`.

    Args:
        length (int): The bit length of the number to generate.
        lock (threading.Lock): A lock to prevent race conditions when updating `possibleNum`.
    """
    global possibleNum
    while not possibleNum:
        x = secrets.randbits(length)
        if isPrime(x):  # Check if the generated number is prime
            lock.acquire()
            try:
                possibleNum = x
            finally:
                lock.release()


def generateProbablePrimeThreaded(length: int) -> int:
    """
    Generates a random prime number of a specified binary length using multithreading.

    Args:
        length (int): The bit length of the prime number to generate.

    Returns:
        int: A probable prime number generated using multiple threads.
    """
    global possibleNum
    possibleNum = 0  # reset possibleNum
    lock = threading.Lock()  # Mutex lock to prevent race conditions
    threadNum = 2  # Number of threads to spawn for generating numbers

    # Create and start threads
    threads = [
        threading.Thread(daemon=True, target=genNum, args=(length, lock))
        for i in range(threadNum)
    ]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    return possibleNum


def generateProbablePrime(length: int) -> int:
    """
    Generates a random prime number of a specified binary length (single-threaded version).

    Args:
        length (int): The bit length of the prime number to generate.

    Returns:
        int: A random prime number generated using a brute-force method.
    
    The function uses the `secrets.randbits()` function to generate a random number of the 
    specified length, checks if it's prime, and if not, increments by 2 (to avoid even numbers).
    It continues this process until a prime number is found.
    """
    x = secrets.randbits(length)
    if x % 2 == 0:
        x += 1  # Ensure the number is odd
    while True:
        if isPrime(x):
            return x
        x += 2  # Increment by 2 to keep it odd


def generatePrimeUseAPI(length: int) -> int:
    """
    Generates a random prime number of a specified binary length by querying a third-party API.

    Args:
        length (int): The bit length of the prime number to generate. Supported values are 2048, 4096, and 8192.

    Returns:
        int: A prime number returned by the API in base 10.

    Raises:
        Exception: If the provided `length` is not one of the supported values (2048, 4096, 8192).
    """
    if length not in [2048, 4096, 8192]:
        raise Exception("generatePrimeUseAPI only supports lengths of 2048, 4096, or 8192")
    
    api_url = f"https://2ton.com.au/getprimes/random/{length}"
    response = requests.get(api_url)
    return int(response.json()["p"]["base10"])


def randomRelativePrime(p: int) -> int:
    """
    Generates a random integer that is relatively prime to a given number `p`.

    Args:
        p (int): The number to find a relatively prime integer with.

    Returns:
        int: A random integer `k` such that gcd(k, p) = 1, i.e., `k` is relatively prime to `p`.
    
    This function generates random integers between 2 and `p - 2` until it finds one that is
    relatively prime to `p`, i.e., the greatest common divisor (gcd) of `k` and `p` is 1.
    """
    k = randomIntInRange(2, p - 2)
    while gcd(k, p) != 1:
        k = randomIntInRange(2, p - 2)
    return k

