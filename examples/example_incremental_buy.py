
from bonding.bondingcurveamm import BondingCurveAMM


# Compare incremental buying to single larger trade

if __name__=='__main__':
    total_investment_value = 1000.0  # Total currency to invest
    n_trading_opportunities = 10  # Number of splits

    # Single trade approach
    amm_single = BondingCurveAMM(scale=1000.0, fee_rate=0.001)
    shares_single = amm_single.buy_value(total_investment_value)
    net_single = amm_single.sell_shares(shares_single)

    # Split approach
    amm_split = BondingCurveAMM(scale=1000.0, fee_rate=0.001)
    shares_split = 0.0
    for _ in range(n_trading_opportunities):
        shares_split += amm_split.buy_value(total_investment_value / n_trading_opportunities)
    net_split = amm_split.sell_shares(shares_split)

    print(f"net_split={net_split}, net_single={net_single}")

    # Ensure that the split approach does not yield more net than the single trade
    assert net_split <= net_single + 1e-6, \
        "Multiple small buys+sell shouldn't yield strictly more net than a single trade."