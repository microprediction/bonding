from bonding.curves.bondingcurve import BondingCurve
import math
import logging


class GrowthBondingCurve(BondingCurve):
    """
    A factor-based bonding curve that ensures:
      - f(0) = 1,
      - f(scale) = 2,
      - price grows by fraction 'a' each time x is multiplied by c.

    Mathematically:
        p = ln(1 + a) / ln(c),  (requires a > -1, c > 1)
        f(x) = 1 + (x^p / scale^p).

    So:
      1) f(0)   = 1
      2) f(scale)= 1 + 1 = 2
      3) strictly increasing for x>0 if p>0
      4) simple closed-form integral


    Motivated by a suggestion of Wilson Lau
    See https://medium.com/thoughtchains/on-single-bonding-curves-for-continuous-token-models-a167f5ffef89

    """

    def __init__(self,  scale=100.0, a=0.25, c=2.0):
        """
        Parameters
        ----------
        a : float
            Fractional growth per factor c. e.g. a=0.25 => +25% price each time x is multiplied by c.
            Must satisfy (1+a)>0.
        c : float
            The factor base. c>1 means 'per doubling/tripling/etc' of x.
        scale : float
            The x-value at which price is guaranteed to be 2. Must be > 0.
        """
        if (1 + a) <= 0:
            raise ValueError("Parameter 'a' must be > -1 so (1+a) is positive.")
        if c <= 1:
            raise ValueError("Parameter 'c' must be > 1 for log_c(x) style growth.")
        if scale <= 0:
            raise ValueError("Parameter 'scale' must be positive.")

        self.a = float(a)
        self.c = float(c)
        self.scale = float(scale)

        self.logger = logging.getLogger(self.__class__.__name__)

        # exponent p = ln(1+a)/ln(c). Must be > 0 if a>0 and c>1.
        self.p = math.log(1.0 + self.a) / math.log(self.c)
        if self.p <= 0:
            self.logger.warning("Resulting exponent p = %.4f is non-positive; curve may not be strictly increasing.",
                                self.p)

    def price(self, x: float) -> float:
        """
        price(x) = 1 + (x^p / scale^p),  for x >= 0
        with p = ln(1+a)/ln(c).

        => f(0)=1, f(scale)=2.
        """
        if x < 0:
            raise ValueError("Supply x cannot be negative.")

        return 1.0 + (x ** self.p) / (self.scale ** self.p)

    def price_integral(self, x: float) -> float:
        """
        ∫[0..x] price(u) du
         = ∫[0..x] [1 + (u^p / scale^p)] du
         = ∫[0..x] 1 du + ∫[0..x] [u^p / scale^p] du
         = x + (1 / scale^p) * [u^(p+1)/(p+1)] from 0..x
         = x + (x^(p+1) / [scale^p * (p+1)]),   if p != -1.
        """
        if x < 0:
            raise ValueError("Supply x cannot be negative.")
        if x == 0:
            return 0.0

        # If p == -1, the integral of u^-1 is ln(u). We'll assume a>0 => p>0 => no special case needed.
        return x + (x ** (self.p + 1)) / (self.scale ** self.p * (self.p + 1))

    def __repr__(self):
        return (f"<GrowthBondingCurve(a={self.a}, c={self.c}, scale={self.scale}, "
                f"p={self.p:.4f})>")


if __name__=='__main__':
    curve = GrowthBondingCurve(scale=10)
    curve.plot(x_max=10)