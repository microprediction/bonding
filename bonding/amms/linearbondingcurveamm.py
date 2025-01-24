from bonding.curves.linearbondingcurve import LinearBondingCurve
from bonding.amms.bondingcurveamm import BondingCurveAMM


class LinearBondingCurveAMM(BondingCurveAMM):
    def __init__(self, scale=500_000, fee_rate: float = 0.0):
        super().__init__(curve=LinearBondingCurve(scale=scale), fee_rate=fee_rate)



