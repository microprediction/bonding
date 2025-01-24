from bonding.curves.growthbondingcurve import GrowthBondingCurve
from bonding.amms.bondingcurveamm import BondingCurveAMM


class GrowthBondingCurveAMM(BondingCurveAMM):
    def __init__(self, scale=500_000, fee_rate: float = 0.0):
        super().__init__(curve=GrowthBondingCurve(scale=scale), fee_rate=fee_rate)




if __name__=='__main__':
    initial_investment_value = 1000.0  # Total currency to invest
    amm = GrowthBondingCurveAMM(scale=1000.0, fee_rate=0.001)
    shares = amm.buy_value(initial_investment_value)
    sale_proceeds_value = amm.sell_shares(shares)
    print(f"Proceeds from buying and selling all shares: {sale_proceeds_value}")
