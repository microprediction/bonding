# bonding   ![tests_312](https://github.com/microprediction/bonding/workflows/tests_312/badge.svg) ![tests_312_scipy_matplotlib](https://github.com/microprediction/bonding/workflows/tests_312_scipy_matplotlib/badge.svg)
Bonding curves and automated market makers that use them. 

### Introduction:
As a kid I liked to invent board games. One was like monopoly, except that you got to buy stocks. For each stock there was a pile of cards, each card representing a share. The first card indicated a price of 100. The second card indicated a price of 130, and so forth. 

Skipping forward to the reinvention of everything in web3, we have the modern equivalent with terminology `bonding curve`, for which there is a good simple intro [here](https://www.linkedin.com/pulse/bonding-curves-new-frontier-decentralized-finance-andrea-dal-mas-4zq3f/). A market maker charges a deterministic incremental price that is a monotonic (usually) function of the number of outstanding shares x. To compute hypothetical trades (e.g. size dependence bids or offers) or actual trades it performs an integration of the price curve. In this package we also account for and acrue breakage when shares are rounded by a small QUANTA, and the AMM can optionally collect a proportional fee. 

If you like control theory then this is a greenfield, I suspect. I'm collating [questions](https://github.com/microprediction/bonding/blob/main/QUESTIONS.md) and [literature](https://github.com/microprediction/bonding/blob/main/LITERATURE.md) sporadically. 


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


### Interpretation of `scale`
All curves satisfy:

     price(0)=1
     price(scale)=2 

See the [bondingcurve.py](https://github.com/microprediction/bonding/blob/main/bonding/curves/bondingcurve.py) for verification methods. 

They are also monotonic, as you can verify. For example:

     from bonding.amms.sqrtbondingcurve import SqrtBondingCurve
     SqrtBondingCurve(scale=10).plot()

### Automated market maker properties
Round trip buying and selling, in either direction, cannot yield an arbitrage whether we specify quantity or cost. See [bondingcurveamm,py](https://github.com/microprediction/bonding/blob/main/bonding/amms/bondingcurveamm.py) for verification methods. 
