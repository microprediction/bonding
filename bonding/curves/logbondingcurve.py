from bonding.curves.bondingcurve import BondingCurve
import math
import logging


class LogBondingCurve(BondingCurve):
    """
    Implements a logarithmic bonding curve defined by:
        f(x) = log(e + (e^2 - e) * (x / scale))

    Key properties:
    ---------------
    1) f(0) = log(e) = 1
       Starts at 1 when x=0.

    2) f(scale) = log(e + (e^2 - e) * (scale / scale)) = log(e + e^2 - e) = log(e^2) = 2
       Price doubles at x = scale.

    3) Strictly increasing for x >= 0 because derivative = (e^2 - e) / (e + (e^2 - e) * (x / scale)) > 0.

    4) Has an analytic integral:
         ∫ log(e + (e^2 - e) * (u / scale)) du
       which evaluates to:
         (e + (e^2 - e) * (x / scale)) * (log(e + (e^2 - e) * (x / scale)) - 1) / ((e^2 - e) / scale)
    """

    def __init__(self, scale: float = 500_000):
        """
        Initialize the LogBondingCurve.

        Parameters
        ----------
        scale : float, optional
            Scaling parameter for the curve. Must be positive.
            Determines the x at which the price doubles. Defaults to 500,000.
        """
        if scale <= 0:
            raise ValueError("Parameter 'scale' must be positive.")

        self.scale = float(scale)
        self.logger = logging.getLogger(self.__class__.__name__)

    def price(self, x: float) -> float:
        """
        price(x) = log(e + (e^2 - e) * (x / scale))

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
        return math.log(math.e + (math.e ** 2 - math.e) * (x / self.scale))

    def price_integral(self, x: float) -> float:
        """
        The definite integral of price(u) from 0 to x:

            ∫[0 to x] log(e + (e^2 - e) * (u / scale)) du
            = (e + (e^2 - e) * (x / scale)) * (log(e + (e^2 - e) * (x / scale)) - 1) / ((e^2 - e) / scale)

        Parameters
        ----------
        x : float
            The upper limit of integration (>= 0).

        Returns
        -------
        float
            ∫[0 to x] log(e + (e^2 - e) * (u / scale)) du
        """
        if x < 0:
            raise ValueError("Supply x cannot be negative.")
        if x == 0:
            return 0.0

        numerator = (math.e + (math.e ** 2 - math.e) * (x / self.scale)) * \
                    (math.log(math.e + (math.e ** 2 - math.e) * (x / self.scale)) - 1)
        denominator = (math.e ** 2 - math.e) / self.scale
        return numerator / denominator

    def __repr__(self) -> str:
        return (f"<LogBondingCurve(scale={self.scale}, "
                f"price(x)=log(e + (e^2 - e)*(x/scale)))>")


if __name__ == "__main__":
    curve = LogBondingCurve(scale=10)
    curve.plot(x_max=10)
    print(f"price(0)    = {curve.price(0):.4f}")
    print(f"price(10)   = {curve.price(10):.4f}")  # Should be 2.0
    print(f"price(50)   = {curve.price(50):.4f}")
    print(f"integral(0) = {curve.price_integral(0):.4f}")
    print(f"integral(10)= {curve.price_integral(10):.4f}")
    print(f"integral(50)= {curve.price_integral(50):.4f}")
