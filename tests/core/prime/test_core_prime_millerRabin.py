from app.core.prime.millerRabin import millerRabin
import random

def test_prime_numbers():
    """ Test that prime numbers are correctly identified. """
    primes = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71
    ]
    for prime in primes:
        assert millerRabin(prime) is True, f"{prime} should be prime"

def test_composite_numbers():
    """ Test that composite numbers are correctly identified. """
    composites = [
        4, 6, 8, 9, 10, 15, 16, 18, 20, 25,
        27, 28, 30, 35, 39, 40, 44, 45, 49, 50
    ]
    for composite in composites:
        assert millerRabin(composite) is False, f"{composite} should be composite"