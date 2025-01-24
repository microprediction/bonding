

def all_amm_cls():
    from bonding.amms.linearbondingcurveamm import LinearBondingCurveAMM
    from bonding.amms.logbondingcurveamm import LogBondingCurveAMM
    from bonding.amms.sqrtbondingcurveamm import SqrtBondingCurveAMM
    return [
        LinearBondingCurveAMM,
        LogBondingCurveAMM,
        SqrtBondingCurveAMM,
    ]


if __name__ == '__main__':
    for amm in all_amm_cls():
        print(amm.__name__)