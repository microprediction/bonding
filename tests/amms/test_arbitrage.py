from bonding.amms.allamms import all_amm_cls


def test_buy_shares_then_sell_shares():
    """
    Test that all AMMs are importable and have the expected methods.
    """
    for amm in all_amm_cls():
        amm_instance = amm(scale=10)
        amm_instance.simulate_buy_shares_then_sell_shares(num_shares=1.0)


def test_all_amms_arbitrage():
    """
    Test that all AMMs are importable and have the expected methods.
    """
    for amm in all_amm_cls():
        assert hasattr(amm, 'buy_value'), f"{amm.__name__} should have a buy_value method."
        assert hasattr(amm, 'sell_shares'), f"{amm.__name__} should have a sell_shares method."
        assert hasattr(amm, 'buy_shares'), f"{amm.__name__} should have a buy_shares method."
        assert hasattr(amm, 'sell_value'), f"{amm.__name__} should have a sell_value method."

        amm_instance = amm(scale=10)
        assert amm_instance.assert_no_round_trip_arbitrage()
