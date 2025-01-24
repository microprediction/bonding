In no particular order. The scope is robust diversified portfolios and things that help, **but focused on bonding curves and related game-theoretic properties**. To add to this list or correct an entry, ideally:

1. Fork the repo (top right)  
2. Edit this file.  
3. Submit a pull request (also possible with a click or two).  

Or file an [issue](https://github.com/microprediction/bonding/issues).




## Bancor Protocol Whitepaper [pdf](https://www.securities.io/bancor-whitepaper/)

The Bancor Protocol is a decentralized liquidity network that allows for the automatic and continuous trading of tokens through the use of smart tokens equipped with a built-in smart contract. These smart tokens can be bought and sold directly by users, without the need for a traditional order book, by relying on a mathematically defined pricing mechanism known as a bonding curve.


## Uniswap v2 Whitepaper [pdf](https://app.uniswap.org/whitepaper.pdf)

This technical whitepaper explains some of the design decisions behind the Uniswap
v2 core contracts. It covers the contracts’ new features—including arbitrary pairs
between ERC20s, a hardened price oracle that allows other contracts to estimate the
time-weighted average price over a given interval, “flash swaps” that allow traders to
receive assets and use them elsewhere before paying for them later in the transaction,
and a protocol fee that can be turned on in the future. It also re-architects the contracts
to reduce their attack surface. This whitepaper describes the mechanics of Uniswap v2’s
“core” contracts including the pair contract that stores liquidity providers’ funds—and
the factory contract used to instantiate pair contracts.



## Introducing the Equilibrium Bonding Market [medium](https://blog.oceanprotocol.com/introducing-the-equilibrium-bonding-market-e7db528e0eff)
Fang Gong

This article presents a new automated market maker design that overcomes issues with bonding curves, for application to curation and staking. It is called “equilibrium bonding market” because it provides the equilibrium price of the bonded token.




## Curve Finance Whitepaper (“Stableswap”) [pdf](https://curve.fi/files/crypto-pools-paper.pdf)

Curve Finance is a decentralized exchange optimized for low slippage swaps between assets with similar values, such as stablecoins. The Stableswap algorithm introduces a specialized bonding curve that maintains high capital efficiency and minimal price impact, enabling large trades with minimal slippage. This whitepaper details the mathematical foundations of Stableswap, its implementation, and the benefits it offers for stable asset trading within the DeFi ecosystem.


## Bonding Curves & Liquidity Bootstrapping Pools (LBPs) [docs](https://docs.balancer.fi/guides/liquidity-bootstrapping-pools)

Liquidity Bootstrapping Pools (LBPs) utilize dynamic bonding curves to facilitate the gradual release of tokens, thereby reducing initial volatility and preventing large-scale manipulation by whales. By adjusting the weight of tokens over time, LBPs enable fair and balanced token distributions, ensuring that the market can organically discover the token price without abrupt shocks or disproportionate influence from single entities.


## Incentive-Compatible AMMs [report](https://delphidigital.io/reports/incentive-compatible-amms)

Incentive-Compatible Automated Market Makers (AMMs) are designed to align the incentives of liquidity providers and traders to ensure sustainable liquidity and minimize exploitative behaviors. This report explores various design mechanisms and strategies to enhance the robustness and fairness of AMMs, addressing challenges such as front-running, miner extractable value (MEV), and volatility management. By implementing incentive-compatible structures, AMMs can foster healthier and more resilient decentralized financial markets.


## Aragon Fundraising Whitepaper [repo](https://github.com/aragon/whitepaper)

The Aragon Network is an Aragon organization that provides infrastructure and services to users of the Aragon platform, and is governed by ANT holders. The existing Aragon infrastructure enables users to create and manage organizations. Each Aragon organization exists as a set of smart contracts that define the organization's stakeholders and their associated rights and privileges. However, some rights and privileges require subjective constraints that cannot be encoded in a smart contract directly.

The Aragon Court is a decentralized oracle protocol developed and maintained by the Aragon Network. The Aragon Court can be used by organizations, including the Aragon Network itself, to resolve subjective disputes with binary outcomes. When combined with the existing Aragon infrastructure, it enables an organization to create Proposal Agreements that define subjective constraints on an organization's operation and can be enforced by minority stakeholders.



## The Curation Markets Whitepaper [medium](https://medium.com/@simondlr/introducing-curation-markets-trade-popularity-of-memes-information-with-code-70bf6fed9881)
Simon de la Rouviere

Curation markets are designed to incentivize communities to collectively organize information using token bonding curves as a mechanism for value discovery and coordination. This whitepaper explores how bonding curves establish a pricing function for curated tokens, allowing participants to stake on particular content, topics, or projects. The model’s game-theoretic underpinnings encourage collaboration, as individuals are rewarded for contributing to the shared knowledge pool and accurately signaling valuable information.



