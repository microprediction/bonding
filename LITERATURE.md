In no particular order. The scope is robust diversified portfolios and things that help, **but focused on bonding curves and related game-theoretic properties**. To add to this list or correct an entry, ideally:

1. Fork the repo (top right)  
2. Edit this file.  
3. Submit a pull request (also possible with a click or two).  

Or file an [issue](https://github.com/microprediction/bonding/issues).

## A Myersonian Framework for Optimal Liquidity Provision in Automated Market Makers [arxiv](https://arxiv.org/abs/2303.00208)
Jason Milionis, Ciamac C. Moallemi, Tim Roughgarden

In decentralized finance ("DeFi"), automated market makers (AMMs) enable traders to programmatically exchange one asset for another. Such trades are enabled by the assets deposited by liquidity providers (LPs). The goal of this paper is to characterize and interpret the optimal (i.e., profit-maximizing) strategy of a monopolist liquidity provider, as a function of that LP's beliefs about asset prices and trader behavior. We introduce a general framework for reasoning about AMMs based on a Bayesian-like belief inference framework, where LPs maintain an asset price estimate. In this model, the market maker (i.e., LP) chooses a demand curve that specifies the quantity of a risky asset to be held at each dollar price. Traders arrive sequentially and submit a price bid that can be interpreted as their estimate of the risky asset price; the AMM responds to this submitted bid with an allocation of the risky asset to the trader, a payment that the trader must pay, and a revised internal estimate for the true asset price. We define an incentive-compatible (IC) AMM as one in which a trader's optimal strategy is to submit its true estimate of the asset price, and characterize the IC AMMs as those with downward-sloping demand curves and payments defined by a formula familiar from Myerson's optimal auction theory. We generalize Myerson's virtual values, and characterize the profit-maximizing IC AMM. The optimal demand curve generally has a jump that can be interpreted as a "bid-ask spread," which we show is caused by a combination of adverse selection risk (dominant when the degree of information asymmetry is large) and monopoly pricing (dominant when asymmetry is small). This work opens up new research directions into the study of automated exchange mechanisms from the lens of optimal auction theory and iterative belief inference, using tools of theoretical computer science in a novel way.


## Equitable Continuous Organizations with Self-Assessed Valuations [arxiv](https://arxiv.org/pdf/2203.10644)
Howard Heaton Sam Green

Organizations are often unable to align the interests of all stakeholders with the financial success of the organization (e.g. due to regulation). However, continuous
organizations (COs) introduce a paradigm shift. COs offer immediate liquidity, are
permission-less and can align incentives. CO shares are issued continuously in the
form of tokens via a smart contract on a blockchain. Token prices are designed to
increase as more tokens are minted. When the share supply is low, near-zero prices
make it advantageous to buy and hold tokens until interest in the CO increases, enabling a profitable sale. This attribute of COs, known as investment efficiency, is
desirable. Yet, it can yield allocative inefficiency via the “holdout problem,” i.e. latecomers may find a CO more valuable than early tokenholders, but be unable to attain
the same token holdings due to inflated prices. With the aim of increasing overall equity, we introduce a voting mechanism into COs. We show this balances allocative
and investment efficiency, and may dissuade speculative trading behaviors, thereby
decreasing investment risk.


## Adaptive Curves for Optimally Efficient Market Making  [arxiv](https://arxiv.org/abs/2406.13794)
Viraj Nadkarni, Sanjeev Kulkarni, Pramod Viswanath

Automated Market Makers (AMMs) are essential in Decentralized Finance (DeFi) as they match liquidity supply with demand. They function through liquidity providers (LPs) who deposit assets into liquidity pools. However, the asset trading prices in these pools often trail behind those in more dynamic, centralized exchanges, leading to potential arbitrage losses for LPs. This issue is tackled by adapting market maker bonding curves to trader behavior, based on the classical market microstructure model of Glosten and Milgrom. Our approach ensures a zero-profit condition for the market maker's prices. We derive the differential equation that an optimal adaptive curve should follow to minimize arbitrage losses while remaining competitive. Solutions to this optimality equation are obtained for standard Gaussian and Lognormal price models using Kalman filtering. A key feature of our method is its ability to estimate the external market price without relying on price or loss oracles. We also provide an equivalent differential equation for the implied dynamics of canonical static bonding curves and establish conditions for their optimality. Our algorithms demonstrate robustness to changing market conditions and adversarial perturbations, and we offer an on-chain implementation using Uniswap v4 alongside off-chain AI co-processors.

## Static Replication of Impermanent Loss for Concentrated Liquidity Provision in Decentralised Markets
Jun Deng, Hua Zong, Yun Wang

This article analytically characterizes the impermanent loss of concentrated liquidity provision for automatic market makers in
decentralised markets such as Uniswap. We propose two static replication formulas for the impermanent loss by a combination of
European calls or puts with strike prices supported on the liquidity provision price interval. It facilitates liquidity providers to hedge
impermanent loss by trading crypto options in more liquid centralised exchanges such as Deribit. Numerical examples illustrate the
astonishing accuracy of the static replication

## Fragmentation and optimal liquidity supply on decentralized exchanges [pdf](https://arxiv.org/pdf/2307.13772)
Alfred Lehar, Christine A. Parlour, Marius Zoican

We investigate how liquidity providers (LPs) choose between high- and low-fee trading venues,
in the face of a fixed common gas cost. Analyzing Uniswap data, we find that high-fee pools
attract 58% of liquidity supply yet execute only 21% of volume. Large LPs dominate low-fee
pools, frequently adjusting out-of-range positions in response to informed order flow. In contrast,
small LPs converge to high-fee pools, accepting lower execution probabilities to mitigate adverse
selection and liquidity management costs. Fragmented liquidity dominates a single-fee market,
as it encourages more liquidity providers to enter the market, while fostering LP competition on
the low-fee pool



## Bonding Curves in Continuous Token Models [medium](https://medium.com/thoughtchains/on-single-bonding-curves-for-continuous-token-models-a167f5ffef89)

Bonding curves are a fundamental concept in the design of continuous token models. They provide a mathematical relationship between the supply of a token and its price, enabling the seamless issuance and redemption of tokens. By defining this relationship, bonding curves facilitate automated market making and ensure continuous liquidity without relying on traditional exchange order books.


Remark. This motivated [growth bonding curve](https://github.com/microprediction/bonding/blob/main/bonding/curves/growthbondingcurve.py)

## A non-custodial portfolio manager, liquidity provider, and price sensor. [pdf](https://wikibitimg.fx994.com/attach/2021/05/212595670202/WBE212595670202_14467.pdf)
Fernando Martinelli, Nikolai Mushegian

A Balancer Pool is an automated market maker with certain key properties that cause it to function as a selfbalancing weighted portfolio and price sensor.
Balancer turns the concept of an index fund on its head: instead of paying fees to portfolio managers to
rebalance your portfolio, you collect fees from traders, who rebalance your portfolio by following arbitrage
opportunities.
Balancer is based on a particular N-dimensional surface which denes a cost function for the exchange of
any pair of tokens held in a Balancer Pool. This approach was rst described by V. Buterin[0]
(https://www.reddit.com/r/ethereum/comments/55m04x/lets_run_onchain_decentralized_exchanges_the_way/),
generalized by Alan Lu[1] (https://blog.gnosis.pm/building-a-decentralized-exchange-in-ethereumeea4e7452d6e), and proven viable for market making by the popular Uniswap[2] (https://uniswap.io) dapp.
We independently arrived at the same surface denition by starting with the requirement that any trade
must maintain a constant proportion of value in each asset of the portfolio. We applied an invariant-based
modeling approach described by Zargham et al[3] (https://arxiv.org/pdf/1807.00955.pdf) to construct this
solution. We will prove that these constant-value market makers have this property



## Towards a Universal Theory of AMMs [arxiv](https://arxiv.org/abs/2111.12646)

We introduce a unified framework for automated market makers (AMMs) that generalizes several existing AMM designs, including constant product, constant sum, and other bonding curve-based models. By leveraging convex analysis, we demonstrate how different AMM mechanisms can be understood as specific instances within this broader theory. Our approach facilitates the systematic exploration of new AMM designs and provides insights into their economic properties, such as liquidity provision, price stability, and susceptibility to arbitrage. Additionally, we analyze the game-theoretic aspects of these mechanisms, including participant incentives and equilibrium behaviors, highlighting how different AMM designs can impact market dynamics and trader strategies.

## Bonding Curves & Liquidity Bootstrapping Pools (LBPs) [docs](https://docs.balancer.fi/guides/liquidity-bootstrapping-pools)

Liquidity Bootstrapping Pools (LBPs) utilize dynamic bonding curves to facilitate the gradual release of tokens, thereby reducing initial volatility and preventing large-scale manipulation by whales. By adjusting the weight of tokens over time, LBPs enable fair and balanced token distributions, ensuring that the market can organically discover the token price without abrupt shocks or disproportionate influence from single entities.


## Incentive-Compatible AMMs [report](https://delphidigital.io/reports/incentive-compatible-amms)

Incentive-Compatible Automated Market Makers (AMMs) are designed to align the incentives of liquidity providers and traders to ensure sustainable liquidity and minimize exploitative behaviors. This report explores various design mechanisms and strategies to enhance the robustness and fairness of AMMs, addressing challenges such as front-running, miner extractable value (MEV), and volatility management. By implementing incentive-compatible structures, AMMs can foster healthier and more resilient decentralized financial markets.




