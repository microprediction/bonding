In no particular order. The scope is robust diversified portfolios and things that help, **but focused on bonding curves and related game-theoretic properties**. To add to this list or correct an entry, ideally:

1. Fork the repo (top right)  
2. Edit this file.  
3. Submit a pull request (also possible with a click or two).  

Or file an [issue](https://github.com/microprediction/bonding/issues).


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



## Bancor Protocol Whitepaper [pdf](https://bancor.network/static/Bancor_Protocol_Whitepaper_en.pdf)

The Bancor Protocol is a decentralized liquidity network that allows for the automatic and continuous trading of tokens through the use of smart tokens equipped with a built-in smart contract. These smart tokens can be bought and sold directly by users, without the need for a traditional order book, by relying on a mathematically defined pricing mechanism known as a bonding curve.

---

## Bonding Curves in Continuous Token Models [medium](https://medium.com/@simondlr/bonding-curves-in-continuous-token-models-6681749e0c50)

Bonding curves are a fundamental concept in the design of continuous token models. They provide a mathematical relationship between the supply of a token and its price, enabling the seamless issuance and redemption of tokens. By defining this relationship, bonding curves facilitate automated market making and ensure continuous liquidity without relying on traditional exchange order books.

---

## Uniswap v2 Whitepaper [pdf](https://uniswap.org/whitepaper.pdf)

Uniswap is a fully decentralized protocol for automated liquidity provision on Ethereum. It uses a constant product formula (x * y = k) to maintain liquidity pools, enabling users to trade ERC-20 tokens directly from their wallets without relying on traditional order books. This whitepaper details the protocol's design, economic incentives, and potential applications within the decentralized finance (DeFi) ecosystem.

---

## Gnosis Protocol: The OWL Token [docs](https://docs.gnosis.io/protocol/docs/introduction1/)

The OWL token is designed to leverage bonding curves for dynamic token issuance and pricing within the Gnosis Protocol. By utilizing a bonding curve mechanism, the OWL token ensures continuous liquidity and adjusts its price based on supply and demand, thereby providing a robust and automated market-making solution that mitigates common issues such as front-running and price manipulation.

---

## Balancer Whitepaper [pdf](https://balancer.fi/whitepaper)

Balancer is an automated portfolio manager and trading platform that allows users to create self-balancing cryptocurrency portfolios. By enabling customizable weightings of multiple tokens within a liquidity pool, Balancer provides dynamic pricing and automated rebalancing, acting as a generalization of automated market makers. This whitepaper explores the underlying mechanics, economic incentives, and potential applications of Balancer within the decentralized finance (DeFi) landscape.

---

## Bonding Curves, Explored [blog](https://blog.oceanprotocol.com/bonding-curves-explored-bdp-2b046184f28e)

Bonding curves are a powerful tool in the decentralized finance ecosystem, providing a mathematical framework for dynamic token pricing and liquidity management. In this exploration, we delve into the mechanics of bonding curves, their implementation in smart contracts, and the economic incentives they create for participants. By understanding these elements, developers can design more robust and incentive-aligned token economies.

---

## Game Theoretic Properties of Bonding Curves [block.science](https://block.science/) 

This study examines the game-theoretic aspects of bonding curves within automated market makers (AMMs). By analyzing participant strategies and equilibrium behaviors, we explore how different bonding curve designs influence market dynamics, liquidity provision, and resistance to arbitrage. The findings provide insights into designing bonding curves that promote fair and efficient markets, enhancing the robustness of decentralized financial systems.

---

## Towards a Universal Theory of AMMs [arxiv](https://arxiv.org/abs/2111.12646)

We introduce a unified framework for automated market makers (AMMs) that generalizes several existing AMM designs, including constant product, constant sum, and other bonding curve-based models. By leveraging convex analysis, we demonstrate how different AMM mechanisms can be understood as specific instances within this broader theory. Our approach facilitates the systematic exploration of new AMM designs and provides insights into their economic properties, such as liquidity provision, price stability, and susceptibility to arbitrage. Additionally, we analyze the game-theoretic aspects of these mechanisms, including participant incentives and equilibrium behaviors, highlighting how different AMM designs can impact market dynamics and trader strategies.

---

## Curve Finance Whitepaper (“Stableswap”) [pdf](https://curve.fi/files/crypto-pools-paper.pdf)

Curve Finance is a decentralized exchange optimized for low slippage swaps between assets with similar values, such as stablecoins. The Stableswap algorithm introduces a specialized bonding curve that maintains high capital efficiency and minimal price impact, enabling large trades with minimal slippage. This whitepaper details the mathematical foundations of Stableswap, its implementation, and the benefits it offers for stable asset trading within the DeFi ecosystem.

---

## Bonding Curves & Liquidity Bootstrapping Pools (LBPs) [docs](https://docs.balancer.fi/guides/liquidity-bootstrapping-pools)

Liquidity Bootstrapping Pools (LBPs) utilize dynamic bonding curves to facilitate the gradual release of tokens, thereby reducing initial volatility and preventing large-scale manipulation by whales. By adjusting the weight of tokens over time, LBPs enable fair and balanced token distributions, ensuring that the market can organically discover the token price without abrupt shocks or disproportionate influence from single entities.

---

## Incentive-Compatible AMMs [report](https://delphidigital.io/reports/incentive-compatible-amms)

Incentive-Compatible Automated Market Makers (AMMs) are designed to align the incentives of liquidity providers and traders to ensure sustainable liquidity and minimize exploitative behaviors. This report explores various design mechanisms and strategies to enhance the robustness and fairness of AMMs, addressing challenges such as front-running, miner extractable value (MEV), and volatility management. By implementing incentive-compatible structures, AMMs can foster healthier and more resilient decentralized financial markets.

---

## Aragon Fundraising Whitepaper [pdf](https://github.com/aragon/fundraising/raw/master/docs/Aragon%20Fundraising%20Whitepaper.pdf)

Aragon Fundraising aims to provide a framework for decentralized organizations to raise capital and manage finances using a bonding curve model. By leveraging a continuous token issuance process, organizations can enable stakeholders to seamlessly enter or exit a project while maintaining transparent and accountable governance. This paper outlines the core components, theoretical foundations, and practical considerations for implementing Aragon Fundraising within the Aragon ecosystem.

---

## The Curation Markets Whitepaper [pdf](https://tokensummit.com/curation-markets-whitepaper)

Curation markets are designed to incentivize communities to collectively organize information using token bonding curves as a mechanism for value discovery and coordination. This whitepaper explores how bonding curves establish a pricing function for curated tokens, allowing participants to stake on particular content, topics, or projects. The model’s game-theoretic underpinnings encourage collaboration, as individuals are rewarded for contributing to the shared knowledge pool and accurately signaling valuable information.

---

## Reflexer Labs: RAI Whitepaper [pdf](https://reflexer.finance/whitepaper)

RAI is introduced as a non-pegged stable asset governed by a reflex-bonding mechanism that dynamically adjusts interest rates based on market conditions. By departing from traditional peg-based designs, RAI seeks to achieve greater stability and independence from fiat-denominated collateral. This whitepaper presents the theoretical foundations, incentive structures, and protocol mechanics aimed at creating a more resilient form of decentralized money.

---

## Hummingbot Whitepaper [pdf](https://hummingbot.io/Hummingbot_Whitepaper.pdf)

Hummingbot is an open-source software client that allows users to create and run high-frequency trading bots across various cryptocurrency exchanges and DeFi protocols. While not exclusively focused on bonding curves, it provides insight into algorithmic market making and liquidity provision strategies that intersect with bonding curve designs. This whitepaper discusses architecture, supported strategies, and how Hummingbot contributes to a more efficient and transparent market infrastructure.

