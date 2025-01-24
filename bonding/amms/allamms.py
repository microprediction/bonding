

def all_amm_cls():
    from bonding.amms.linearbondingcurveamm import LinearBondingCurveAMM
    from bonding.amms.logbondingcurveamm import LogBondingCurveAMM
    from bonding.amms.sqrtbondingcurveamm import SqrtBondingCurveAMM
    from bonding.amms.expbondingcurveamm import ExpBondingCurveAMM
    from bonding.amms.growthbondingcurveamm import GrowthBondingCurveAMM
    return [
        LinearBondingCurveAMM,
        LogBondingCurveAMM,
        SqrtBondingCurveAMM,
        ExpBondingCurveAMM,
        GrowthBondingCurveAMM
    ]


if __name__ == '__main__':
    for amm in all_amm_cls():
        print(amm.__name__)