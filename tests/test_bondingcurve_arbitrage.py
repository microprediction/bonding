# tests/test_bonding_curve_amm.py
import pytest
import math

from bonding.sqrtbondingcurveamm import SqrtBondingCurveAMM  # Adjust the import path as necessary


@pytest.fixture
def amm_with_fees():
    """Fixture for AMM instance with fees."""
    return SqrtBondingCurveAMM(scale=100.0, fee_rate=0.001)  # 0.1% fee


@pytest.fixture
def amm_no_fees():
    """Fixture for AMM instance without fees."""
    return SqrtBondingCurveAMM(scale=100.0, fee_rate=0.0)  # No fees


def test_no_arbitrage_immediate_round_trip_with_fees(amm_with_fees):
    """
    Test that buying and immediately selling with fees results in a net loss.
    """
    initial_investment = 1000.0

    # Buy shares with a specific currency amount
    shares_bought = amm_with_fees.buy_value(initial_investment)

    # Immediately sell all those shares
    net_received = amm_with_fees.sell_shares(shares_bought)

    # Assert that the user receives less than they invested due to fees
    assert net_received < initial_investment, \
        "Immediate round-trip with fees should not yield a profit."


def test_no_arbitrage_immediate_round_trip_no_fees(amm_no_fees):
    """
    Test that buying and immediately selling without fees results in breaking even.
    """
    initial_investment = 1000.0

    # Buy shares with a specific currency amount (no fees)
    shares_bought = amm_no_fees.buy_value(initial_investment)

    # Immediately sell all those shares
    net_received = amm_no_fees.sell_shares(shares_bought)

    # With zero fees, the user should roughly break even (allow small floating error).
    assert math.isclose(net_received, initial_investment, rel_tol=1e-6), \
        "Immediate round-trip with zero fees should be break-even."


def test_split_vs_single_trade_no_free_arbitrage():
    """
    Ensure that splitting a large trade into multiple small trades does not yield extra profit.
    """
    X = 1000.0  # total currency to invest
    N = 10  # number of splits

    # Single trade approach
    amm_single = SqrtBondingCurveAMM(scale=1000.0, fee_rate=0.001)
    shares_single = amm_single.buy_value(X)
    net_single = amm_single.sell_shares(shares_single)

    # Split approach
    amm_split = SqrtBondingCurveAMM(scale=1000.0, fee_rate=0.001)
    shares_split = 0.0
    for _ in range(N):
        shares_split += amm_split.buy_value(X / N)
    net_split = amm_split.sell_shares(shares_split)

    # Because of the bonding curve's continuity and the proportional fee,
    # multiple smaller buys/sell should not yield strictly more net than a single big trade
    assert net_split <= net_single + 1e-6, \
        "Multiple small buys+sell shouldn't yield strictly more net than a single trade."


def test_zero_trade_no_change(amm_with_fees):
    """
    Test that performing a zero-value trade does not change the state.
    """
    amm = amm_with_fees

    # Initial state
    initial_x = amm.x
    initial_cash = amm.total_cash_collected
    initial_fees = amm.total_fees_collected

    # Perform zero buy
    shares_bought = amm.buy_value(0.0)
    assert shares_bought == 0.0, "Buying with zero value should return zero shares."
    assert amm.x == initial_x, "Supply should remain unchanged after zero buy."
    assert amm.total_cash_collected == initial_cash, \
        "Cash collected should remain unchanged after zero buy."
    assert amm.total_fees_collected == initial_fees, \
        "Fees collected should remain unchanged after zero buy."

    # Perform zero sell
    net_received = amm.sell_shares(0.0)
    assert net_received == 0.0, "Selling zero shares should return zero currency."
    assert amm.x == initial_x, "Supply should remain unchanged after zero sell."
    assert amm.total_cash_collected == initial_cash, \
        "Cash collected should remain unchanged after zero sell."
    assert amm.total_fees_collected == initial_fees, \
        "Fees collected should remain unchanged after zero sell."


###############################################################################
# Additional Tests for the New "buy_shares" and "sell_value" Methods
###############################################################################

def test_buy_shares_no_fees(amm_no_fees):
    """
    Test buying an exact number of shares when there are no fees.
    - The user calls `buy_shares(num_shares)` and pays a certain total.
    - Then the user sells those shares.
    They should roughly break even, ignoring tiny rounding differences.
    """
    amm = amm_no_fees

    # Suppose we want exactly 10 shares
    shares_target = 10.0
    total_paid = amm.buy_shares(shares_target)
    assert total_paid > 0.0, "Buying shares should cost some positive amount of currency."
    # The supply should have increased exactly by 10
    assert math.isclose(amm.x, shares_target, rel_tol=1e-9), "Supply should increase by exactly 10."

    net_received = amm.sell_shares(shares_target)
    # No fees, so we expect net_received ~ total_paid
    assert math.isclose(net_received, total_paid, rel_tol=1e-6), \
        "Without fees, buying then selling the same shares should be near break-even."
    # Supply back to zero
    assert math.isclose(amm.x, 0.0, abs_tol=1e-9), \
        "Supply should be back to zero after selling all shares."


def test_buy_shares_with_fees(amm_with_fees):
    """
    Test buying an exact number of shares when there is a fee.
    - The user calls `buy_shares(num_shares)` and pays total_paid.
    - Then sells the same number of shares.
    The net_received from selling should be less than total_paid due to fees.
    """
    amm = amm_with_fees

    shares_target = 5.0
    total_paid = amm.buy_shares(shares_target)
    assert total_paid > 0.0, "Should pay positive currency for 5 shares."

    net_received = amm.sell_shares(shares_target)
    assert net_received < total_paid, \
        "With fees, user should not break even on immediate buy->sell round trip."
    assert math.isclose(amm.x, 0.0, abs_tol=1e-9), \
        "All shares sold, supply should return to 0."


def test_sell_value_no_fees(amm_no_fees):
    """
    Test selling enough shares to receive a specific amount of currency with no fees.
    - The user first buys some shares (buy_value).
    - Then the user calls `sell_value(...)` to get exactly some currency.
    Check that the shares sold is consistent and the user breaks even if they buy and sell instantly.
    """
    amm = amm_no_fees

    # Buy some shares with 500 currency
    shares_bought = amm.buy_value(500.0)
    # Now we want to get exactly 200
