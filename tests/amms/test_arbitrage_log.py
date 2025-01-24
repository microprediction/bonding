from bonding.amms.logbondingcurveamm import LogBondingCurveAMM


def test_log_bonding_curve_amm():
    amm = LogBondingCurveAMM(scale=10)
    assert amm.assert_no_round_trip_arbitrage()
