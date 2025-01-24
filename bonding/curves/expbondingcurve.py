from bonding.curves.bondingcurve import BondingCurve
import math
import logging


class ExpBondingCurve(BondingCurve):
    """
    Implements an exponential bonding curve defined by:
        f(x) = (1 / (e - 1)) * e^(x / scale) + (e - 2) / (e - 1)

    Key properties:
    ---------------
    1) f(0) = 1
       Starts at 1 when x=0.

    2) f(scale) = 2
       Price doubles at x = scale.

    3) Strictly increasing for x >= 0 because derivative = (1 / scale) * (1 / (e - 1)) * e^(x / scale) > 0.

    4) Has an analytic integral:
         ∫[0 to x] f(u) du = (scale / (e - 1)) * (e^(x / scale) - 1) + ((e - 2) / (e - 1)) * x
    """

    def __init__(self, scale: float = 500_000):
        """
        Initialize the ExpBondingCurve.

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

        # Precompute constants a and b for efficiency
        self.a = 1.0 / (math.e - 1)
        self.b = (math.e - 2) / (math.e - 1)

    def price(self, x: float) -> float:
        """
        price(x) = (1 / (e - 1)) * e^(x / scale) + (e - 2) / (e - 1)

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
        return self.a * math.exp(x / self.scale) + self.b

    def price_integral(self, x: float) -> float:
        """
        The definite integral of price(u) from 0 to x:

            ∫[0 to x] [(1 / (e - 1)) * e^(u / scale) + (e - 2) / (e - 1)] du

        Which evaluates to:

            (scale / (e - 1)) * (e^(x / scale) - 1) + ((e - 2) / (e - 1)) * x

        Parameters
        ----------
        x : float
            The upper limit of integration (>= 0).

        Returns
        -------
        float
            ∫[0 to x] price(u) du
        """
        if x < 0:
            raise ValueError("Supply x cannot be negative.")
        if x == 0:
            return 0.0

        integral = (self.scale / (math.e - 1)) * (math.exp(x / self.scale) - 1) + \
                   ((math.e - 2) / (math.e - 1)) * x
        return integral

    def __repr__(self) -> str:
        return (f"<ExpBondingCurve(scale={self.scale}, "
                f"a={self.a:.6f}, b={self.b:.6f})>")


if __name__ == "__main__":
    # Initialize the Exponential Bonding Curve with a scale of 10
    curve = ExpBondingCurve(scale=10)

    # Plot the price function and its analytical vs numerical integrals
    curve.plot(x_max=10, num_points=1000)

    # Verify the integral accuracy
    x_test_values = [0, 1, 5, 10, 20, 30, 40, 50]
    try:
        curve.verify_integral_accuracy(x_test_values, tolerance=1e-6)
        print("Exponential Bonding Curve: Integral verification passed.")
    except AssertionError as e:
        print(f"Exponential Bonding Curve: Integral verification failed.\n{e}")

    # Print some price and integral values
    test_xs = [0, 10, 20, 30, 40, 50]
    for x in test_xs:
        price = curve.price(x)
        integral = curve.price_integral(x)
        print(f"price({x})    = {price:.6f}")
        print(f"integral({x}) = {integral:.6f}")
