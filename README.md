# bonding   ![tests_312](https://github.com/microprediction/bonding/workflows/tests_312/badge.svg) ![tests_312_scipy_matplotlib](https://github.com/microprediction/bonding/workflows/tests_312_scipy_matplotlib/badge.svg)
Bonding curves and automated market makers that use them. 

### Conceptual:
The market maker charges a deterministic incremental price that is a function of the number of outstanding shares x. To compute hypothetical trades (size dependence bids or offers) or actual trades it performs an integration of the price curve, also accounting for breakage when shares are rounded by a small QUANTA and optionally collecting a proportional fee. 

### Usage:

Create a market maker:

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
