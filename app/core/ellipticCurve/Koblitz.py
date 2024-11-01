import multiprocessing
from typing import Union, Tuple
from app.core.ellipticCurve.point import Point
from app.core.ellipticCurve.domain import CurveDomainParamter
from functools import lru_cache, partial


def encode(
        message: str, curve_name: str = "secp521r1", d: int = 100, chunk_size: int = 10,  alphabet_size: int = 2**8, lengthy=True
) -> Union[Tuple[Tuple[Point, int]], Tuple[Point, int]]:
    """Encodes a textual message to a point on the elliptic curve using the Koblitz method.

    This method efficiently converts a textual message (represented as a string) into a point
    on the elliptic curve associated with this `Koblitz` instance. The Koblitz method leverages
    the specified `alphabet_size` to map characters in the message to integers within a valid
    range.

    Args:
        message (str): The textual message to be encoded. Each character in the message should
            be representable within the provided `alphabet_size`. Common choices for `alphabet_size`
            include 2**8 for ASCII encoding and 2**16 for Unicode encoding, depending on the character
            set used in the message.
        alphabet_size (int, optional): The size of the alphabet/character set used in the message.
                Defaults to 2**8 (256) for ASCII encoding. Higher values accommodate larger character sets.
        lengthy (bool, optional): A flag indicating whether the message is lengthy or not. If True, the method
            treats the `message` argument as a large message to be encoded in chunks. Defaults to False.

    Returns:
        Union[Tuple[Point, int], Tuple[Tuple[Point, int]]]:
            - If `lengthy` is False, a single tuple containing two elements is returned:
                - The first element is a `Point` object representing the encoded point on the elliptic curve.
                - The second element is an integer `j` that serves as an auxiliary value used during the
                encoding process.
            - If `lengthy` is True, a tuple of tuples is returned. Each inner tuple follows the same format
            as the single tuple described above.
    """

    # Encode a single message
    if not lengthy:
        curve = CurveDomainParamter.get(curve_name=curve_name)
        # Convert the string message to a single large integer
        message_decimal = sum(
            ord(char) * (alphabet_size**i) for i, char in enumerate(message[:chunk_size])
        )

        # Search for a valid curve point using the Koblitz method
        # d = 100  # Scaling factor
        for j in range(1, d - 1):
            x = (d * message_decimal + j) % curve.p
            s = (x**3 + curve.a * x + curve.b) % curve.p

            # Check if 's' is a quadratic residue modulo 'p', meaning 'y' can be computed
            if s == pow(s, (curve.p + 1) // 2, curve.p):
                y = pow(s, (curve.p + 1) // 4, curve.p)

                # Verify that the computed point is on the curve
                if curve.on_curve(x, y):
                    break

        return Point(curve, x, y), d

    # Initialize a multiprocessing pool
    pool = multiprocessing.Pool()

    # Execute the encode function in parallel using the pool
    encoded_messages = pool.map(
        partial(encode, curve_name=curve_name, d=d,
                alphabet_size=alphabet_size, lengthy=False),
        [message[i: i + chunk_size]
            for i in range(0, len(message), chunk_size)],
    )

    # Close the pool
    pool.close()
    pool.join()

    return tuple(encoded_messages)


def decode(
    encoded: Union[Point, tuple[Tuple[Point, int]]],
    d: int = 100,
    alphabet_size: int = 2**8,
    lengthy=True,
) -> str:
    """Decodes a point on an elliptic curve to a textual message using the Koblitz method.

    This method recovers the original textual message from a point on the elliptic curve
    associated with this `Koblitz` class. The `decode` method leverages the Koblitz method and
    the provided `j` value, which was obtained during the encoding process, to recover the message.
    The specified `alphabet_size` is crucial for interpreting the integer values derived from the
    curve point and mapping them back to characters in the message.

    Args:
        encoded (Point): The encoded point on the elliptic curve to be decoded, or a tuple of tuples
            representing multiple encoded points if `lengthy` was True during encoding.
        j (int): The auxiliary value 'j' that was generated during the encoding process and is
            used to assist in the decoding process. Defaults to 0.
        alphabet_size (int, optional): The size of the alphabet/character set used in the message.
                Defaults to 2**8 (256) for ASCII encoding. Higher values accommodate larger character sets.
        lengthy (bool, optional): A flag indicating whether the message was encoded in chunks. If True, the method
            treats the `encoded` argument as a collection of encoded messages to be decoded individually.
            Defaults to False.

    Returns:
        str: The decoded textual message that was originally encoded using the Koblitz method.

    Raises:
        ValueError: If the provided point is not on the elliptic curve associated with this `Koblitz` instance.
    """

    # Decode single point
    if not lengthy and isinstance(encoded, Point):
        # Calculate the original large integer from the point and 'j'
        message_decimal = encoded.x // d

        # Decompose the large integer into individual characters based on `alphabet_size`
        characters = []
        while message_decimal != 0:
            characters.append(chr(message_decimal % alphabet_size))
            message_decimal //= alphabet_size

        # Convert the list of characters into a string and return it
        return "".join(characters)

    # Decode tuple of (Point, int) pairs
    def is_tuple_of_point_int(instance): return isinstance(instance, tuple) and all(
        isinstance(elem, tuple)
        and len(elem) == 2
        and isinstance(elem[0], Point)
        and isinstance(elem[1], int)
        for elem in instance
    )

    characters = []
    if is_tuple_of_point_int(encoded):

        # Initialize a multiprocessing pool
        pool = multiprocessing.Pool()

        # Execute the decode function in parallel using the pool
        characters = pool.starmap(
            partial(decode, alphabet_size=alphabet_size, lengthy=False),
            [(i[0], i[1]) for i in encoded],
        )

        # Close the pool
        pool.close()
        pool.join()

    return "".join(characters)
