from abc import ABC, abstractmethod
from bonding.curveplots.matplotlibcurveplot import matplotlib_curve_plot
from bonding.curves.verifyintegralaccuracy import verify_integral_accuracy
from typing import List


class BondingCurve(ABC):
    """
    Abstract base class for amms curves.

    Each concrete amms curve must define:
      - price(x): float
      - price_integral(x): float
        => integral of price(u) du from 0 to x
      - cost_to_move(x_start, x_end): float
        => can default to price_integral(x_end) - price_integral(x_start),
           or be overridden if desired.
    """

    def get_scale(self) -> float:
        try:
            return self.__getattribute__("scale")
        except AttributeError:
            raise NotImplementedError("Concrete class must implement get_scale() method or have scale attribute.")

    @abstractmethod
    def price(self, x: float) -> float:
        """
        Return the instantaneous price at `x`.
        """
        pass

    @abstractmethod
    def price_integral(self, x: float) -> float:
        """
        Return the integral of the price function from 0 to x.
        """
        pass

    def cost_to_move(self, x_start: float, x_end: float) -> float:
        """
        Return the cost to move from x_start to x_end.
        Default implementation: difference in the integrals.
        """
        return self.price_integral(x_end) - self.price_integral(x_start)

    def plot(self, x_max: float = 10, num_points: int = 1000):
        return matplotlib_curve_plot(self, x_max=x_max, num_points=num_points)

    def verify_integral_accuracy(self, x_values: List[float], tolerance: float = 1e-6) -> bool:
        return verify_integral_accuracy(self, x_values=x_values, tolerance=tolerance)

    def verify_initial_unit_price(self):
        # Price should double by the time we issue scale shares
        return abs(self.price(0) - 1) < 1e-6

    def verify_scale_convention(self):
        # Price should double by the time we issue scale shares
        return abs(self.price(self.get_scale()) - 2) < 1e-6


