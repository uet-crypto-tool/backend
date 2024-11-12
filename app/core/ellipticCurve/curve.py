from __future__ import annotations
from typing import Tuple, Dict, Union
import app.core.ellipticCurve.point as point


class Curve:
    """
    Represents an elliptic curve defined by the equation:
        y^2 ≡ x^3 + ax + b (mod p)

    Attributes:
        name (str): Name of the curve.
        p (int): The prime modulus of the field.
        a (int): The coefficient for the x term in the curve equation.
        b (int): The constant term in the curve equation.
        g (point.Point): The base point (generator) of the curve.
        n (int): The order of the base point.
        h (int): The cofactor of the curve.
    """

    def __init__(
        self,
        p: int,
        a: int,
        b: int,
        g: Tuple[int, int],
        n: int,
        h: int,
        name: str = "undefined",
    ):
        """
        Initializes the elliptic curve.

        Args:
            p (int): The prime modulus.
            a (int): The coefficient for the x term.
            b (int): The constant term.
            g (Tuple[int, int]): The coordinates of the base point.
            n (int): The order of the base point.
            h (int): The cofactor.
            name (str): The name of the curve.
        """
        self.name = name
        self.p = p
        self.a = a
        self.b = b
        self.g = point.Point(self, g[0], g[1])  # Initialize base point
        self.n = n
        self.h = h

        if self.is_singular():
            raise ValueError("The curve is singular, invalid parameters.")

    def is_singular(self) -> bool:
        """
        Checks if the curve is singular.

        Returns:
            bool: True if the curve is singular, False otherwise.
        """
        return (4 * self.a**3 + 27 * self.b**2) % self.p == 0

    def on_curve(self, x: int, y: int) -> bool:
        """
        Checks if a point (x, y) lies on the curve.

        Args:
            x (int): The x-coordinate of the point.
            y (int): The y-coordinate of the point.

        Returns:
            bool: True if the point lies on the curve, False otherwise.
        """
        return (y**2 - x**3 - self.a * x - self.b) % self.p == 0

    def __eq__(self, other: Union[Curve, object]) -> bool:
        """
        Compares two curves for equality.

        Args:
            other (Curve): Another curve to compare.

        Returns:
            bool: True if the curves are equal, False otherwise.
        """
        if not isinstance(other, Curve):
            return False
        return (
            self.p == other.p
            and self.a == other.a
            and self.b == other.b
            and self.n == other.n
            and self.h == other.h
        )

    def __ne__(self, other: Union[Curve, object]) -> bool:
        """
        Compares two curves for inequality.

        Args:
            other (Curve): Another curve to compare.

        Returns:
            bool: True if the curves are not equal, False otherwise.
        """
        return not self.__eq__(other)

    def __str__(self) -> str:
        """
        Returns a string representation of the curve.

        Returns:
            str: String representation of the curve equation.
        """
        return f'"{self.name}" => y^2 ≡ x^3 + {self.a}x + {self.b} (mod {self.p})'

    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the curve.

        Returns:
            str: Detailed string representation of the curve.
        """
        return self.__str__()

    def to_json(self) -> Dict[str, Union[str, bool, Dict[str, str]]]:
        """
        Serializes the curve into a JSON-compatible dictionary.

        Returns:
            Dict[str, Union[str, bool, Dict[str, str]]]: JSON-compatible representation of the curve.
        """
        return {
            "name": self.name,
            "p": str(self.p),
            "a": str(self.a),
            "b": str(self.b),
            "g": {"x": str(self.g.x), "y": str(self.g.y)},
            "n": str(self.n),
            "h": str(self.h),
            "is_singular": self.is_singular(),
        }
