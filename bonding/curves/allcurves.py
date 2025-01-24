def all_curves_cls():
    from bonding.curves.linearbondingcurve import LinearBondingCurve
    from bonding.curves.logbondingcurve import LogBondingCurve
    from bonding.curves.sqrtbondingcurve import SqrtBondingCurve
    from bonding.curves.growthbondingcurve import GrowthBondingCurve
    from bonding.curves.expbondingcurve import ExpBondingCurve
    return [
        LinearBondingCurve,
        LogBondingCurve,
        SqrtBondingCurve,
        GrowthBondingCurve,
        ExpBondingCurve
    ]


if __name__ == '__main__':
    for amm in all_curves_cls():
        print(amm.__name__)