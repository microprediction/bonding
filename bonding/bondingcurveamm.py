import logging
import math

# Define the smallest currency denomination
QUANTA = 1e-8


class BondingCurveAMM:
    """
    A simple Automated Market Maker (AMM) implementing a bonding curve:
        price(x) = sqrt(1 + (x / scale)^2)
    with integral:
        price_integral(x) = 0.5 * [ x * sqrt(1 + (x/scale)^2 )
                                    + scale * asinh(x / scale) ]

    Now supports a tiny proportional transaction fee rate, e.g. 0.001 for 0.1%.
    Also collects tiny breakage fees, which are fractions of the quanta
    Exposes hypothetical trade results (which can be used to display size-dependent bid-offers if needed)

    Attributes
    ----------
    scale : float
        Scaling parameter in the price function.
    fee_rate : float
        Fraction of each transaction (buy or sell) collected as fees. 0.001 => 0.1% fee.
    quanta : float
        Defines the smallest currency denomination (1e-8).
    x : float
        Current total minted/sold (the "supply" on the bonding curve).
    total_cash_collected : float
        Total amount of currency that the bonding curve has collected (this excludes fees).
    total_fees_collected : float
        Total amount of currency collected as fees.
    logger : logging.Logger
        Logger instance for logging events and errors.
    """

    def __init__(self, scale=500000.0, fee_rate=0.0, quanta=QUANTA):
        """
        Initialize the BondingCurveAMM.

        Parameters
        ----------
        scale : float, optional
            Scaling parameter in the bonding curve. Defaults to 500,000.
        fee_rate : float, optional
            Fraction of each transaction (buy or sell) to be taken as fees (0.001 => 0.1%).
        quanta : float, optional
            Defines the smallest currency denomination (1e-8). Defaults to QUANTA.
        """
        self.scale = float(scale)
        self.fee_rate = float(fee_rate)
        self.quanta = float(quanta)

        # Current supply of shares
        self.x = 0.0

        # AMM balances
        self.total_cash_collected = 0.0
        self.total_fees_collected = 0.0

        # Configure logger
        self.logger = logging.getLogger(self.__class__.__name__)

    ############################################################################
    # Price & Integral
    ############################################################################

    @staticmethod
    def _price(x: float, scale: float) -> float:
        """
        price(x) = sqrt(1 + (x / scale)^2).
        """
        return math.sqrt(1.0 + (x / scale) ** 2)

    @staticmethod
    def _price_integral(x: float, scale: float) -> float:
        """
        price_integral(x) = ∫ sqrt(1 + (u/scale)^2) du from 0 to x.

        = 0.5 * [ x * sqrt(1 + (x/scale)^2 ) + scale * asinh(x/scale) ]
        """
        x_prime = x / scale
        return 0.5 * (
                x * math.sqrt(1.0 + x_prime ** 2)
                + scale * math.asinh(x_prime)
        )

    def _cost_to_move(self, x_start: float, x_end: float) -> float:
        """
        Cost in currency to move from x_start to x_end.
        Positive if x_end > x_start (buying), negative if x_end < x_start (selling).
        """
        return self._price_integral(x_end, self.scale) - self._price_integral(x_start, self.scale)

    ############################################################################
    # Core "solver" method
    ############################################################################

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
            cost = self._cost_to_move(x_start, x_test)

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
            cost_mid = self._cost_to_move(x_start, x_mid)

            if abs(cost_mid - target_cost) < tolerance:
                return direction * mid_dx

            if (direction > 0 and cost_mid < target_cost) or \
                    (direction < 0 and cost_mid > target_cost):
                lower_dx = mid_dx
            else:
                upper_dx = mid_dx

        return direction * 0.5 * (lower_dx + upper_dx)

    ############################################################################
    # Simulation (Hypothetical) Methods
    #   - "buy_value"     => user spends a currency amount, mints shares
    #   - "buy_shares"    => user wants exactly n_trading_opportunities shares, figure out currency cost
    #   - "sell_value"    => user wants to get a currency amount, figure out shares
    #   - "sell_shares"   => user sells exactly n_trading_opportunities shares, figure out currency proceeds
    ############################################################################

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
        gross_cost = self._cost_to_move(self.x, self.x + num_shares)
        if gross_cost < 0:
            gross_cost = 0.0  # Edge case if num_shares=0 or x=0

        # If the user must ensure the curve receives exactly `gross_cost`,
        # then total_needed = gross_cost / (1 - fee_rate).
        # We'll round up to the nearest quanta so we definitely get that many shares.
        if self.fee_rate < 1.0:
            ideal_total = gross_cost / (1.0 - self.fee_rate)
        else:
            # If fee_rate=1, the user can't actually buy anything. We'll just handle zero-shares.
            ideal_total = float('inf') if gross_cost > 0 else 0.0

        quanta_used = int(math.ceil(ideal_total / self.quanta)) if ideal_total > 0 else 0
        total_paid = quanta_used * self.quanta
        breakage_fee = total_paid - ideal_total if total_paid > ideal_total else 0.0
        fee_amount = total_paid * self.fee_rate

        # The net that actually goes to the curve:
        # net = total_paid - fee_amount. That should be >= gross_cost, meaning user might slightly overpay.

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

        # 1) The "gross" currency (before fees/breakage) from x -> x - num_shares
        gross_currency = -self._cost_to_move(self.x, self.x - num_shares)
        if gross_currency < 0:
            gross_currency = 0.0  # Edge case, shouldn't happen if x>0 and num_shares>0

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

        gross_currency = quanta_used * self.quanta  # We want that from the curve
        fee_amount = gross_currency * self.fee_rate
        net_currency = gross_currency - fee_amount

        # 2) Solve for dx s.t. cost_to_move(x, x+dx) = -gross_currency
        # because the user is receiving `gross_currency` from the curve
        dx = self._solve_for_dx(self.x, -gross_currency)  # negative

        return {
            "quanta_used": quanta_used,
            "breakage_fee": breakage_fee,
            "fee_amount": fee_amount,
            "gross_currency": gross_currency,
            "net_currency": net_currency,
            "shares_sold": dx,
        }

    ############################################################################
    # Actual Action Methods
    ############################################################################

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

        # We'll assume we can indeed mint exactly num_shares:
        # The net cost is sim["gross_cost"], but the user pays sim["total_paid"] (including fees, breakage).
        # Increase supply by num_shares
        self.x += num_shares

        # The curve receives net = sim["total_paid"] - sim["fee_amount"]
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
        dx = sim["shares_sold"]  # negative

        # Check if this would exceed the current supply
        if self.x + dx < 0:
            raise ValueError("Not enough supply to sell the requested currency amount (would go negative).")

        # Finalize state
        self.x += dx
        self.total_fees_collected += sim["breakage_fee"] + sim["fee_amount"]
        self.total_cash_collected -= sim["net_currency"]

        return abs(dx)

    ############################################################################
    # Utility
    ############################################################################

    def get_maximum_sell_value(self) -> float:
        """
        Returns the maximum net currency value one can extract by selling all shares (self.x).
        """
        if self.x <= 0:
            return 0.0
        sim = self.simulate_sell_shares(num_shares=self.x)
        # We'll return net_currency truncated to quanta
        max_quanta = int(math.floor(sim["net_currency"] / self.quanta))
        return max_quanta * self.quanta

    def total_cost_at_supply(self, x_val: float = None) -> float:
        """
        Returns the integral of the price from 0 to x_val (or self.x).
        """
        if x_val is None:
            x_val = self.x
        return self._price_integral(x_val, self.scale)

    def current_price(self) -> float:
        """
        Returns the instantaneous price at supply self.x.
        """
        return self._price(self.x, self.scale)

    def __repr__(self) -> str:
        return (f"<BondingCurveAMM(scale={self.scale}, quanta={self.quanta}, fee_rate={self.fee_rate}, "
                f"supply={self.x:.6f}, "
                f"cash_collected={self.total_cash_collected:.6f}, "
                f"fees_collected={self.total_fees_collected:.6f})>")
