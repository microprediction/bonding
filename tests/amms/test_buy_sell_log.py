from bonding.amms.logbondingcurveamm import LogBondingCurveAMM


def test_buy_then_sell():
    amm = LogBondingCurveAMM(scale=10)
    amm.simulate_buy_shares_then_sell_shares(num_shares=1.0)
