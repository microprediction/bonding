
from bonding.amms.sqrtbondingcurveamm import SqrtBondingCurveAMM


# Compare incremental buying

if __name__=='__main__':
    initial_investment_value = 1000.0  # Total currency to invest
    N = 10  # Number of splits

    amm = SqrtBondingCurveAMM(scale=1000.0, fee_rate=0.001)
    shares = amm.buy_value(initial_investment_value)
    sale_proceeds_value = amm.sell_shares(shares)
    print(f"Proceeds from buying and selling all shares: {sale_proceeds_value}")
    print(f"Net cost of buying and selling all shares: {initial_investment_value - sale_proceeds_value}")


