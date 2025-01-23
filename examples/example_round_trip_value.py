
from bonding.sqrtbondingcurveamm import SqrtBondingCurveAMM


# Compare incremental buying

if __name__=='__main__':
    initial_investment_value = 1000.0  # Total currency to invest
    N = 10  # Number of splits
    fee_rate = 0.001
    amm = SqrtBondingCurveAMM(scale=1000.0, fee_rate=0.001)
    shares_bought = amm.buy_value(initial_investment_value)

    value_to_sell = amm.get_maximum_sell_value()
    shares_sold = amm.sell_value(value=value_to_sell)

    print(f"Original shares_bought={shares_bought} versus shares_sold={shares_sold}")
    print(f"Shares forfeited = {shares_bought-shares_sold}")

