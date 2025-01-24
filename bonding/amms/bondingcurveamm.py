import logging
import math
from bonding.amms.ammdefaultparams import QUANTA


class BondingCurveAMM:
    """
    A simple Automated Market Maker (AMM) that uses a given BondingCurve
    to determine pricing, while handling transaction fees, rounding, and state tracking.

    Attributes
    ----------
    curve : BondingCurve
        The amms curve instance that defines price and integral logic.
    fee_rate : float
        Fraction of each transaction (buy or sell) collected as fees. 0.001 => 0.1%.
    quanta : float
        Defines the smallest currency denomination (1e-8).
    x : float
        Current total minted/sold (the "supply" on the amms curve).
    total_cash_collected : float
        Total amount of currency that the amms curve has collected (this excludes fees).
    total_fees_collected : float
        Total amount of currency collected as fees.
    logger : logging.Logger
        Logger instance for logging events and errors.
    """

    def __init__(self, curve, fee_rate=0.0, quanta=QUANTA):
        """
        Initialize the BondingCurveAMM.

        Parameters
        ----------
        curve : BondingCurve
            A amms curve instance (e.g. SqrtBondingCurve).
        fee_rate : float, optional
            Fraction of each transaction (buy or sell) to be taken as fees (0.001 => 0.1%).
        quanta : float, optional
            Defines the smallest currency denomination (1e-8). Defaults to QUANTA.
        """
        self.curve = curve
        self.fee_rate = float(fee_rate)
        self.quanta = float(quanta)

        # Current supply of shares
        self.x = 0.0

        # AMM balances
        self.total_cash_collected = 0.0
        self.total_fees_collected = 0.0

        # Configure logger
        self.logger = logging.getLogger(self.__class__.__name__)

    ###########################################################################
    # Internal solver that uses the curve's cost_to_move
    ###########################################################################
    def _solve_for_dx(self, x_start: float, target_cost: float,
                      tolerance=1e-12, max_iter=200) -> float:
        """
        Solve for dx such that cost_to_move(x_start, x_start + dx) = target_cost
        using the bisection method.

        Returns
        -------
        float
            dx (positive if buying, negative if selling).
        """
        if abs(target_cost) < tolerance:
            return 0.0

        direction = 1.0 if target_cost > 0 else -1.0

        # Bisection bracketing
        lower_dx = 0.0
        upper_dx = 1e-12

        # Expand to bracket the solution
        while True:
            x_test = x_start + direction * upper_dx
            if x_test < 0:
                x_test = 0.0
            cost = self.curve.cost_to_move(x_start, x_test)  # Use the curve's logic

            # If we've bracketed the target
            if (direction > 0 and cost >= target_cost) or \
                    (direction < 0 and cost <= target_cost):
                break

            upper_dx *= 2.0
            if abs(upper_dx) > 1e20:
                raise RuntimeError("Failed to bracket the solution for dx (bisection).")

        # Bisection
        for _ in range(max_iter):
            mid_dx = 0.5 * (lower_dx + upper_dx)
            x_mid = x_start + direction * mid_dx
            if x_mid < 0:
                x_mid = 0.0
            cost_mid = self.curve.cost_to_move(x_start, x_mid)

            if abs(cost_mid - target_cost) < tolerance:
                return direction * mid_dx

            if (direction > 0 and cost_mid < target_cost) or \
                    (direction < 0 and cost_mid > target_cost):
                lower_dx = mid_dx
            else:
                upper_dx = mid_dx

        return direction * 0.5 * (lower_dx + upper_dx)

    ###########################################################################
    # Simulation (Hypothetical) Methods
    ###########################################################################
    def simulate_buy_value(self, total_value: float):
        """
        Simulate buying with `total_value` currency.

        Returns a dict with:
            {
                'quanta_used': int,
                'breakage_fee': float,
                'fee_amount': float,
                'net_currency': float,   # actual currency that goes into the curve
                'shares_received': float
            }
        """
        if total_value < 0:
            raise ValueError("Buy value must be non-negative.")

        # 1) Determine how many quanta we can use
        quanta_used = int(math.floor(total_value / self.quanta))
        breakage_fee = total_value - (quanta_used * self.quanta)

        gross_currency = quanta_used * self.quanta
        fee_amount = gross_currency * self.fee_rate
        net_currency = gross_currency - fee_amount

        # 2) Solve how many shares (dx) we can buy with net_currency
        shares_received = self._solve_for_dx(self.x, net_currency)

        return {
            "quanta_used": quanta_used,
            "breakage_fee": breakage_fee,
            "fee_amount": fee_amount,
            "net_currency": net_currency,
            "shares_received": shares_received,
        }

    def simulate_buy_shares(self, num_shares: float):
        """
        Simulate buying exactly `num_shares`, determining how much currency is required.

        Returns a dict with:
            {
                'gross_cost': float,     # The net cost (without fees) required by the curve
                'quanta_used': int,
                'breakage_fee': float,
                'fee_amount': float,
                'total_paid': float,     # The total currency user must pay
            }
        """
        if num_shares < 0:
            raise ValueError("Cannot buy a negative number of shares.")
        # The net cost to move supply from x to x + num_shares
        gross_cost = self.curve.cost_to_move(self.x, self.x + num_shares)
        if gross_cost < 0:
            gross_cost = 0.0  # Edge case if num_shares=0 or x=0

        # If the user must ensure the curve receives exactly `gross_cost`,
        # then total_needed = gross_cost / (1 - fee_rate).
        # We'll round up to the nearest quanta so we definitely get that many shares.
        if self.fee_rate < 1.0:
            ideal_total = gross_cost / (1.0 - self.fee_rate)
        else:
            # If fee_rate=1, the user can't actually buy anything.
            ideal_total = float('inf') if gross_cost > 0 else 0.0

        quanta_used = int(math.ceil(ideal_total / self.quanta)) if ideal_total > 0 else 0
        total_paid = quanta_used * self.quanta
        breakage_fee = total_paid - ideal_total if total_paid > ideal_total else 0.0
        fee_amount = total_paid * self.fee_rate

        return {
            "gross_cost": gross_cost,
            "quanta_used": quanta_used,
            "breakage_fee": breakage_fee,
            "fee_amount": fee_amount,
            "total_paid": total_paid,
        }

    def simulate_sell_shares(self, num_shares: float):
        """
        Simulate selling `num_shares` from the current supply.

        Returns a dict with:
            {
                'gross_currency': float,
                'quanta_used': int,
                'breakage_fee': float,
                'fee_amount': float,
                'net_currency': float,
            }
        """
        if num_shares < 0:
            raise ValueError("Cannot sell a negative number of shares.")
        if num_shares > self.x:
            raise ValueError("Cannot sell more shares than current supply.")

        # 1) The "gross" currency (before fees) from x -> x - num_shares
        gross_currency = -self.curve.cost_to_move(self.x, self.x - num_shares)
        if gross_currency < 0:
            gross_currency = 0.0  # Edge case

        # 2) Break into quanta
        quanta_used = int(math.floor(gross_currency / self.quanta))
        actual_gross = quanta_used * self.quanta
        breakage_fee = gross_currency - actual_gross

        fee_amount = actual_gross * self.fee_rate
        net_currency = actual_gross - fee_amount

        return {
            "gross_currency": gross_currency,
            "quanta_used": quanta_used,
            "breakage_fee": breakage_fee,
            "fee_amount": fee_amount,
            "net_currency": net_currency,
        }

    def simulate_sell_value(self, target_value: float):
        """
        Simulate selling enough shares to receive `target_value` total currency.

        Returns a dict with:
            {
                'quanta_used': int,
                'breakage_fee': float,
                'fee_amount': float,
                'gross_currency': float,
                'net_currency': float,
                'shares_sold': float
            }
        """
        if target_value < 0:
            raise ValueError("Target sell value must be non-negative.")

        # 1) break into quanta
        quanta_used = int(math.floor(target_value / self.quanta))
        breakage_fee = target_value - quanta_used * self.quanta

        gross_currency = quanta_used * self.quanta
        fee_amount = gross_currency * self.fee_rate
        net_currency = gross_currency - fee_amount

        # 2) Solve for dx s.t. cost_to_move(x, x+dx) = -gross_currency
        # (the user is receiving `gross_currency`)
        dx = self._solve_for_dx(self.x, -gross_currency)  # likely negative

        return {
            "quanta_used": quanta_used,
            "breakage_fee": breakage_fee,
            "fee_amount": fee_amount,
            "gross_currency": gross_currency,
            "net_currency": net_currency,
            "shares_sold": dx,
        }

    ###########################################################################
    # Actual Action Methods (State-Changing)
    ###########################################################################
    def buy_value(self, value: float) -> float:
        """
        The user spends `value` currency to buy shares.
        Returns the number of shares actually purchased.
        """
        sim = self.simulate_buy_value(value)

        # Update state from simulation
        self.total_fees_collected += sim["breakage_fee"] + sim["fee_amount"]
        self.total_cash_collected += sim["net_currency"]
        self.x += sim["shares_received"]

        return sim["shares_received"]

    def buy_shares(self, num_shares: float) -> float:
        """
        The user wants to buy exactly `num_shares`.
        Returns the total currency they actually paid.
        """
        sim = self.simulate_buy_shares(num_shares)

        # We assume we can indeed mint exactly num_shares
        self.x += num_shares

        # The curve receives net = (total_paid - fee_amount)
        net_currency = sim["total_paid"] - sim["fee_amount"]

        # Update AMM balances
        self.total_fees_collected += sim["breakage_fee"] + sim["fee_amount"]
        self.total_cash_collected += net_currency

        return sim["total_paid"]

    def sell_shares(self, num_shares: float) -> float:
        """
        Sell exactly `num_shares`, returning the net currency the user receives.
        """
        sim = self.simulate_sell_shares(num_shares)

        # Remove the shares from supply
        self.x -= num_shares

        # The user receives sim["net_currency"]
        self.total_cash_collected -= sim["net_currency"]
        self.total_fees_collected += sim["breakage_fee"] + sim["fee_amount"]

        return sim["net_currency"]

    def sell_value(self, value: float) -> float:
        """
        Sell enough shares to receive `value` currency (in total).
        Returns the number of shares sold (positive float).
        """
        sim = self.simulate_sell_value(value)
        dx = sim["shares_sold"]  # negative or possibly 0

        # Check if this would exceed the current supply
        if self.x + dx < 0:
            raise ValueError("Not enough supply to sell the requested currency amount (would go negative).")

        # Finalize state
        self.x += dx
        self.total_fees_collected += sim["breakage_fee"] + sim["fee_amount"]
        self.total_cash_collected -= sim["net_currency"]

        return abs(dx)

    ###########################################################################
    # Utility
    ###########################################################################
    def get_maximum_sell_value(self) -> float:
        """
        Returns the maximum net currency value one can extract by selling all shares (curve.x).
        """
        if self.x <= 0:
            return 0.0
        sim = self.simulate_sell_shares(num_shares=self.x)
        # We'll return net_currency truncated to quanta
        max_quanta = int(math.floor(sim["net_currency"] / self.quanta))
        return max_quanta * self.quanta

    def total_cost_at_supply(self, x_val: float = None) -> float:
        """
        Returns the integral of the price from 0 to x_val (or curve.x).
        """
        if x_val is None:
            x_val = self.x
        return self.curve.price_integral(x_val)

    def current_price(self) -> float:
        """
        Returns the instantaneous price at supply curve.x.
        """
        return self.curve.price(self.x)

    def __repr__(self) -> str:
        return (f"<BondingCurveAMM("
                f"curve={self.curve.__class__.__name__}, "
                f"fee_rate={self.fee_rate}, "
                f"quanta={self.quanta}, "
                f"supply={self.x:.6f}, "
                f"cash_collected={self.total_cash_collected:.6f}, "
                f"fees_collected={self.total_fees_collected:.6f})>")

    ###########################################################################
    # Arbitrage checks (Round Trip Simulations)
    ###########################################################################
    def simulate_buy_value_then_sell_shares(self, buy_value: float = 1.0):
        """
        Simulate spending `buy_value` currency to buy shares, and then
        immediately selling *all* those purchased shares.

        Returns
        -------
        dict
            {
                'initial_currency': float,
                'final_currency': float,
                'net_delta': float,
                'buy_sim': dict,      # output of simulate_buy_value(...)
                'sell_sim': dict,     # output of simulate_sell_shares(...)
                'arbitrage': bool,    # True if net_delta > 0
            }
        """
        # -- 1) Snapshot current AMM state --
        old_x = self.x
        old_cash = self.total_cash_collected
        old_fees = self.total_fees_collected

        try:
            # -- 2) Perform the actual buy and sell on the AMM --
            shares_received = self.buy_value(buy_value)  # real state change
            final_currency = self.sell_shares(shares_received)  # real state change

            # -- 3) Calculate the net delta --
            net_delta = final_currency - buy_value

            return {
                "initial_currency": buy_value,
                "final_currency": final_currency,
                "net_delta": net_delta,
                "buy_sim": {},  # Optionally, include simulation details if needed
                "sell_sim": {},
                "arbitrage": (net_delta > 0),
            }
        finally:
            # -- 4) Revert state to snapshot to avoid polluting further tests --
            self.x = old_x
            self.total_cash_collected = old_cash
            self.total_fees_collected = old_fees

    def simulate_buy_shares_then_sell_shares(self, num_shares: float = 1.0):
        """
        Simulate buying exactly `num_shares`, then immediately selling
        those same shares.

        Returns
        -------
        dict
            {
                'shares_bought': float,
                'currency_spent': float,    # total_paid from buy_shares
                'currency_received': float, # net_currency from sell_shares
                'net_delta': float,
                'arbitrage': bool
            }
        """
        # -- 1) Snapshot --
        old_x = self.x
        old_cash = self.total_cash_collected
        old_fees = self.total_fees_collected

        try:
            # -- 2) Actual operations --
            currency_spent = self.buy_shares(num_shares)  # returns total_paid
            currency_received = self.sell_shares(num_shares)

            # -- 3) Net delta in currency --
            net_delta = currency_received - currency_spent

            return {
                "shares_bought": num_shares,
                "currency_spent": currency_spent,
                "currency_received": currency_received,
                "net_delta": net_delta,
                "arbitrage": (net_delta > 0),
            }
        finally:
            # -- 4) Revert --
            self.x = old_x
            self.total_cash_collected = old_cash
            self.total_fees_collected = old_fees

    def simulate_sell_value_then_buy_shares(self, target_value: float = 1.0):
        """
        Simulate selling enough shares to receive exactly `target_value` currency,
        then use the *net* proceeds to buy shares again.

        Returns
        -------
        dict
            {
                'target_value': float,
                'shares_sold': float,          # positive
                'buy_shares_received': float,  # how many shares we get from the net currency
                'shares_delta': float,         # (buy_shares_received - shares_sold)
                'arbitrage': bool
            }
        """
        # -- 1) Snapshot --
        old_x = self.x
        old_cash = self.total_cash_collected
        old_fees = self.total_fees_collected

        try:
            # -- 2) Sell enough shares to get `target_value` currency (actual call) --
            shares_sold = self.sell_value(target_value)  # returns # shares sold
            # Now the user has `target_value` currency (conceptually)...

            # -- 3) Use that same currency to buy shares again (actual call) --
            #   We'll call buy_value(...) with exactly `target_value`
            shares_bought = self.buy_value(target_value)

            # -- 4) net shares difference --
            shares_delta = shares_bought - shares_sold

            return {
                "target_value": target_value,
                "shares_sold": shares_sold,
                "buy_shares_received": shares_bought,
                "shares_delta": shares_delta,
                "arbitrage": (shares_delta > 0),
            }
        finally:
            # -- 5) Revert --
            self.x = old_x
            self.total_cash_collected = old_cash
            self.total_fees_collected = old_fees

    def simulate_sell_shares_then_buy_value(self, shares_to_sell: float = 1.0):
        """
        Simulate selling exactly `shares_to_sell`, then use the net proceeds
        to buy as much as possible of the AMM (buy_value) with that currency.

        Returns
        -------
        dict
            {
                'shares_sold': float,
                'currency_received': float,
                'shares_bought': float,
                'shares_delta': float,
                'arbitrage': bool
            }
        """
        # -- 1) Snapshot --
        old_x = self.x
        old_cash = self.total_cash_collected
        old_fees = self.total_fees_collected

        try:
            # -- 2) Sell `shares_to_sell` (actual call) --
            currency_received = self.sell_shares(shares_to_sell)

            # -- 3) Use that entire currency to buy_value(...) again --
            shares_bought = self.buy_value(currency_received)

            # -- 4) Compare new shares vs. old
            shares_delta = shares_bought - shares_to_sell

            return {
                "shares_sold": shares_to_sell,
                "currency_received": currency_received,
                "shares_bought": shares_bought,
                "shares_delta": shares_delta,
                "arbitrage": (shares_delta > 0),
            }
        finally:
            # -- 5) Revert --
            self.x = old_x
            self.total_cash_collected = old_cash
            self.total_fees_collected = old_fees

    def assert_no_round_trip_arbitrage(self) -> bool:
        """
        Runs a few sample round-trip trades with *actual* state changes
        (then reverts after each test). If any scenario yields a net profit,
        raises RuntimeError.

        Returns
        -------
        bool
            True if no arbitrage found, else RuntimeError is raised.
        """
        # You can pick a small set of test values/shares
        test_values = [0.5, 1.0, 10.0]
        test_shares = [0.5, 1.0, 10.0]

        # (1) Buy-value->Sell-shares
        for val in test_values:
            result = self.simulate_buy_value_then_sell_shares(val)
            if result["arbitrage"]:
                raise RuntimeError(
                    f"Arbitrage detected in buy_value->sell_shares for value={val}: "
                    f"net_delta={result['net_delta']}"
                )

        # (2) Buy-shares->Sell-shares
        for s in test_shares:
            result = self.simulate_buy_shares_then_sell_shares(s)
            if result["arbitrage"]:
                raise RuntimeError(
                    f"Arbitrage detected in buy_shares->sell_shares for shares={s}: "
                    f"net_delta={result['net_delta']}"
                )

        # (3) Sell-value->Buy-shares
        for val in test_values:
            # Only attempt if the AMM has enough supply to realistically sell `val`.
            if self.get_maximum_sell_value() >= val:
                result = self.simulate_sell_value_then_buy_shares(val)
                if result["arbitrage"]:
                    raise RuntimeError(
                        f"Arbitrage detected in sell_value->buy_shares for value={val}: "
                        f"shares_delta={result['shares_delta']}"
                    )

        # (4) Sell-shares->Buy-value
        for s in test_shares:
            # Must have enough shares (s <= curve.x) to do the test
            if s <= self.x:
                result = self.simulate_sell_shares_then_buy_value(s)
                if result["arbitrage"]:
                    raise RuntimeError(
                        f"Arbitrage detected in sell_shares->buy_value for shares={s}: "
                        f"shares_delta={result['shares_delta']}"
                    )

        # If we made it here, no arbitrage in tested scenarios
        return True
