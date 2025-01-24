# bonding   ![tests_312](https://github.com/microprediction/bonding/workflows/tests_312/badge.svg) ![tests_312_scipy_matplotlib](https://github.com/microprediction/bonding/workflows/tests_312_scipy_matplotlib/badge.svg)
Bonding curves and automated market makers that use them. 

### Conceptual:
The market maker charges a deterministic incremental price that is a function of the number of outstanding shares x. To compute hypothetical trades (size dependence bids or offers) or actual trades it performs an integration of the price curve, also accounting for breakage when shares are rounded by a small QUANTA and optionally collecting a proportional fee. Simple intro [here](https://www.linkedin.com/pulse/bonding-curves-new-frontier-decentralized-finance-andrea-dal-mas-4zq3f/). 

### Usage:

Create a market maker:

    from bonding.amms.sqrtbondingcurveamm import SqrtBondingCurveAMM
    amm = SqrtBondingCurveAMM(scale=1000.0, fee_rate=0.001)

Invest $1000:

    shares = amm.buy_value(1000.0)

Then sell out:
    
    sale_proceeds_value = amm.sell_shares(shares)
    print(f"Proceeds from buying and selling all shares: {sale_proceeds_value}")
    print(f"Net cost of buying and selling all shares: {initial_investment_value - sale_proceeds_value}")


### Install

     pip install bonding
     pip install matplotlib
     pip install scipy 

Latter two are optional. Scipy is only used for numerical verification at present. 


### Curve properties
The bonding curves all satisfy the following conditions:

     price(0)=1
     prince(self.get_scale())=2 

See the [bondingcurve.py](https://github.com/microprediction/bonding/blob/main/bonding/curves/bondingcurve.py) for verification methods. 

They are also monotonic, as you can verify. For example:

     from bonding.amms.sqrtbondingcurve import SqrtBondingCurve
     SqrtBondingCurve(scale=10).plot()

### Automated market maker properties
Round trip buying and selling, in either direction, cannot yield an arbitrage whether we specify quantity or cost. See [bondingcurveamm,py](https://github.com/microprediction/bonding/blob/main/bonding/amms/bondingcurveamm.py) for verification methods. 
