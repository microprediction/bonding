from bonding.sqrtbondingcurveamm import SqrtBondingCurveAMM


# Compare incremental buying to single larger trade

def test_examples():
    total_investment_value = 1000.0  # Total currency to invest
    n_trading_opportunities = 10  # Number of splits

    # Single trade approach
    amm_single = SqrtBondingCurveAMM(scale=1000.0, fee_rate=0.001)
    shares_single = amm_single.buy_value(total_investment_value)
    net_single = amm_single.sell_shares(shares_single)

    # Split approach
    amm_split = SqrtBondingCurveAMM(scale=1000.0, fee_rate=0.001)
    shares_split = 0.0
    for _ in range(n_trading_opportunities):
        shares_split += amm_split.buy_value(total_investment_value / n_trading_opportunities)
    net_split = amm_split.sell_shares(shares_split)

    print(f"net_split={net_split}, net_single={net_single}")

    assert True