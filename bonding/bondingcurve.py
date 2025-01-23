import math
from abc import ABC, abstractmethod


class BondingCurve(ABC):
    """
    Abstract base class for bonding curves.

    Each concrete bonding curve must define:
      - price(x): float
      - price_integral(x): float
        => integral of price(u) du from 0 to x
      - cost_to_move(x_start, x_end): float
        => can default to price_integral(x_end) - price_integral(x_start),
           or be overridden if desired.
    """

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
