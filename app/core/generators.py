import requests
import threading
import secrets
from app.core.primality import millerRabin


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


def generateProbablePrimeThreaded(length: int) -> int:
    """
    Generates a random prime number of a specified binary length
    Input:
      integer length
    Output:
      integer p
    """
    global possibleNum
    # global count
    possibleNum = 0  # reset
    lock = threading.Lock()  # mutex lock to prevent race conditions
    threadNum = 2  # number of threads to spawn to generate number/primality pairs

    # Create list of threads
    threads = [
        threading.Thread(daemon=True, target=genNum, args=(length, lock))
        for i in range(threadNum)
    ]
    # Execute threads concurrently
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    # print('Count: ' + str(count))

    return possibleNum


def generateProbablePrime(length: int) -> int:
    """
    Generates a random prime number of a specified binary length, not multithreaded
    Input:
      integer length
    Output:
      integer p
    """
    x = secrets.randbits(length)
    if x % 2 == 0:
        x += 1
    while True:
        if millerRabin(x):
            return x
        x += 2


def generatePrimeUseAPI(length: int) -> int:
    if length not in [2048, 4096, 8192]:
        raise Exception("GenreatePrimeUseAPI only support length is 2048, 4096 or 8192")
    api_url = f"https://2ton.com.au/getprimes/random/{length}"
    response = requests.get(api_url)
    return int(response.json()["p"]["base10"])


def randomIntInRange(a: int, b: int) -> int:
    return a + secrets.randbelow(b)
