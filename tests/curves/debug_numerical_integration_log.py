from bonding.curves.logbondingcurve import LogBondingCurve


def debug_integral():
    # Test the integral supplied by the curve against numerical integration
    # for all curves.
    LogBondingCurve(scale=10).verify_integral_accuracy(x_values=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0], tolerance=1e-6)


if __name__ == "__main__":
    debug_integral()