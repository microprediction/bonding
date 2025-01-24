from bonding.curves.bondingcurve import BondingCurve
import math
import logging


class LogBondingCurve(BondingCurve):
    """
    Implements scale logarithmic bonding curve defined by:
        f(x) = log(e + (x / scale))

    Key properties:
    ---------------
    1) f(0) = log(e) = 1
       Starts at 1 when x=0.

    2) Strictly increasing for x >= 0 because derivative = 1 / ( e + x/scale ) > 0.

    3) Has an analytic integral:
         ∫ log(e + (u / scale)) du
       which we implement as scale definite integral from 0 to x in price_integral(x).
    """

    def __init__(self, scale: float = 500_000):
        """
        Initialize the LogBondingCurve.

        Parameters
        ----------
        scale : float, optional
            Scaling parameter for the curve. Must be positive.
            Default: 500,000
        """
        if scale <= 0:
            raise ValueError("Parameter 'scale' must be positive.")

        self.scale = float(scale)
        self.logger = logging.getLogger(self.__class__.__name__)

    def price(self, x: float) -> float:
        """
        price(x) = log(e + x/scale)

        Parameters
        ----------
        x : float
            The current supply (>= 0).

        Returns
        -------
        float
            The instantaneous price at supply x.
        """
        if x < 0:
            raise ValueError("Supply x cannot be negative.")
        return math.log(math.e + x / self.scale)

    def price_integral(self, x: float) -> float:
        """
        The definite integral of price(u) from 0 to x:

            ∫[0 to x] log(e + (u / scale)) du

        By substitution and simplifying, this evaluates to:

            scale*e * ln(e + x/scale) + x * ln(e + x/scale) - x - scale*e

        Parameters
        ----------
        x : float
            The upper limit of integration (>= 0).

        Returns
        -------
        float
            ∫[0 to x] log(e + (u / scale)) du
        """
        if x < 0:
            raise ValueError("Supply x cannot be negative.")

        if x == 0:
            return 0.0

        # Derived expression for ∫ ln(e + (u / scale)) du from 0 to x
        a_e = self.scale * math.e
        return (a_e * math.log(math.e + x / self.scale)
                + x * math.log(math.e + x / self.scale)
                - x
                - a_e)


if __name__ == "__main__":
    curve = LogBondingCurve(scale=10)
    curve.plot(x_max=10)
    print(f"price(0)    = {curve.price(0):.4f}")
    print(f"price(50)   = {curve.price(50):.4f}")
    print(f"integral(50)= {curve.price_integral(50):.4f}")
