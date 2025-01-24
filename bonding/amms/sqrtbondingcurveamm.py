from bonding.curves.sqrtbondingcurve import SqrtBondingCurve
from bonding.amms.bondingcurveamm import BondingCurveAMM


class SqrtBondingCurveAMM(BondingCurveAMM):
    def __init__(self, scale: float = 500_000.0, fee_rate: float = 0.0):
        super().__init__(curve=SqrtBondingCurve(scale=scale), fee_rate=fee_rate)
