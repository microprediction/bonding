from bonding.curves.bondingcurve import BondingCurve


class LinearBondingCurve(BondingCurve):
    """
    price(x) = m*x + b
    price_integral(x) = ∫(m*u + b) du = m/2 * x^2 + b*x
    """

    def __init__(self, scale: float=500_000):
        self.m = 1/scale
        self.b = 1

    def get_scale(self) -> float:
        return 1 / self.m

    def price(self, x: float) -> float:
        return self.m * x + self.b

    def price_integral(self, x: float) -> float:
        return (self.m / 2.0) * (x ** 2) + self.b * x


if __name__=='__main__':
    LinearBondingCurve(scale=10).plot()