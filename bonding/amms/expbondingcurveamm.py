

# bonding/amms/exponentialbondingcurveamm.py

from bonding.curves.expbondingcurve import ExpBondingCurve
from bonding.amms.bondingcurveamm import BondingCurveAMM


class ExpBondingCurveAMM(BondingCurveAMM):

    def __init__(self, scale: float = 500_000.0, fee_rate: float = 0.0):
        """

        scale : float, optional
            Scaling parameter for the exponential bonding curve.
            Determines roughly the x where the price doubles. Must be positive.
            Default: 500,000.0
        fee_rate : float, optional
            Fraction of each transaction (buy or sell) collected as fees.
            0.001 => 0.1%.
            Default: 0.0
        """
        super().__init__(curve=ExpBondingCurve(scale=scale), fee_rate=fee_rate)
