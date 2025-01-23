from bonding.linearbondingcurve import LinearBondingCurve
from bonding.bondingcurveamm import BondingCurveAMM


class LinearBondingCurveAMM(BondingCurveAMM):
    def __init__(self, m: float, b: float, fee_rate: float = 0.0):
        super().__init__(curve=LinearBondingCurve(m=m,b=b), fee_rate=fee_rate)
