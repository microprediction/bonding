from bonding.amms.logbondingcurveamm import LogBondingCurveAMM


if __name__ == '__main__':
    amm = LogBondingCurveAMM(scale=10)
    assert amm.assert_no_round_trip_arbitrage()
