from bonding.bondingcurve import BondingCurve


class LinearBondingCurve(BondingCurve):
    """
    price(x) = m*x + b
    price_integral(x) = ∫(m*u + b) du = m/2 * x^2 + b*x
    """

    def __init__(self, m: float, b: float):
        self.m = m
        self.b = b

    def price(self, x: float) -> float:
        return self.m * x + self.b

    def price_integral(self, x: float) -> float:
        return (self.m / 2.0) * (x ** 2) + self.b * x
