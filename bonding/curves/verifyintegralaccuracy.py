from bonding.using.usingscipy import using_scipy
from typing import List
import logging

if not using_scipy:
    def verify_integral_accuracy(curve, x_values: List[float], tolerance: float = 1e-6) -> bool:
        logger = logging.getLogger(curve.__class__.__name__)
        logger.info("Scipy not available, skipping numerical integration verification.")
        return True


if using_scipy:
    import scipy
    from typing import List

    def verify_integral_accuracy(curve, x_values: List[float], tolerance: float = 1e-6) -> bool:
        """
        Verify that the analytical price_integral matches the numerical integration
        of the price function for a list of x_values.

        Parameters
        ----------
        curve:  BondingCurve
            The bonding curve to verify.
        x_values : List[float]
            A list of x values at which to perform the verification.
        tolerance : float, optional
            The maximum allowed difference between analytical and numerical integrals.

        Returns
        -------
        bool
            True if all verifications pass within the tolerance, False otherwise.

        Raises
        ------
        AssertionError
            If any verification fails.

        """
        discrepancies = []
        for x in x_values:
            numerical_integral, _ = scipy.integrate.quad(curve.price, 0, x)
            analytical_integral = curve.price_integral(x)
            difference = abs(numerical_integral - analytical_integral)
            if difference > tolerance:
                discrepancies.append((x, numerical_integral, analytical_integral, difference))

        if discrepancies:
            logger = logging.getLogger(curve.__class__.__name__)
            logger.error(f"Integral verification failed for {len(discrepancies)} out of {len(x_values)} points.")
            for x, num, ana, diff in discrepancies:
                print(f"Discrepancy at x={x}: Numerical={num}, Analytical={ana}, Difference={diff}")
            raise AssertionError(f"Integral verification failed for {len(discrepancies)} out of {len(x_values)} points.")
        else:
            return True


