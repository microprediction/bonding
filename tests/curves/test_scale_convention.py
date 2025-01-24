from bonding.curves.allcurves import all_curves_cls


def test_scale_conventions():
    # Test the integral supplied by the curve against numerical integration
    # for all curves.
    for curve_cls in all_curves_cls():
        curve = curve_cls()
        curve.verify_scale_convention()


def test_initial_price():
    # Test the integral supplied by the curve against numerical integration
    # for all curves.
    for curve_cls in all_curves_cls():
        curve = curve_cls()
        curve.verify_initial_unit_price()
