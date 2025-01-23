from bonding.bondingcurve import BondingCurve
import math


class SqrtBondingCurve(BondingCurve):
    """
    Implements the sqrt(1 + (x / scale)^2) bonding curve logic.

    price(x) = sqrt(1 + (x/scale)^2)
    price_integral(x) = 0.5 * [ x * sqrt(1 + (x/scale)^2 ) + scale * asinh(x / scale) ]
    """

    def __init__(self, scale: float = 500_000.0):
        self.scale = float(scale)

    def price(self, x: float) -> float:
        return math.sqrt(1.0 + (x / self.scale) ** 2)

    def price_integral(self, x: float) -> float:
        x_prime = x / self.scale
        return 0.5 * (
                x * math.sqrt(1.0 + x_prime ** 2)
                + self.scale * math.asinh(x_prime)
        )
