from bonding.curves.allcurves import all_curves_cls


def test_all_curves():
    # Test the integral supplied by the curve against numerical integration
    # for all curves.
    for curve_cls in all_curves_cls():
        curve = curve_cls()
        curve.verify_integral_accuracy(x_values=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0], tolerance=1e-6)
