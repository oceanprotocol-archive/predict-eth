# Predict ETH

This is a challenge to predict the price of ETH. With prize $$. It uses [ocean.py](https://github.com/oceanprotocol/ocean.py) library.

Predicting ETH accurately helps to make $ in buying / selling ETH, DeFi trading, yield farming or DeFi protocol development. And, you can sell your predictions as a datafeed, for others to do the same. 

Then the challenge is: how accurately can _you_ predict ETH? 

### Current / future challenges

- [Challenge 3](challenges/main3.md) - predictions due Feb 20, 2023

### Example End-to-End Flows

These are example full submissions to the challenge. You can use any of them as a starting point.

- [Simple](examples/end-to-end_simple.md): To-the-point example, with simple input data (just ETH price) and simple model (linear dynamical model)
- [Model optimization](examples/end-to-end_optimized.md): Same as [Simple](examples/end-to-end_simple.md) with added optimization using cross-validation to select best hyperparameters.
- [Compare models](examples/end-to-end_compare-models.md): Build models that predict 1-12 hours ahead in one shot. Compare linear, SVM, RF, and NN models.

### Example Data Sources

These are examples of how to get data from various places. Each place has its own benefits.

Get ETH price data:
- [Via Binance direct](examples/get-ethdata-binance-direct.md) - most direct, but specific to Binance
- [Via ccxt + Binance](examples/get-ethdata-ccxt-binance.md) - unified API across 40 exchanges
- [Via Ocean + Binance](examples/get-ethdata-ocean-binance.md) - unified API across 500+ data & compute services
- [Via Ocean + TheGraph](examples/get-ethdata-ocean-thegraph.md) - like previous, but uses a GraphQL-shaped query

### Inspiration: ideas for data & modeling

Here are ideas to get even more accurate results.

- [More data sources](ideas/data-sources.md)
- [Modeling approaches](ideas/modeling.md)
- [Articles](ideas/articles.md) on predicting ETH, etc

### Inspiration from algorithmic trading 

Getting into the head of a trader might inspire you in predicting ETH.

To help with that, the [algorithmic trading flow README](ideas/algorithmic-trading-flow.md) does a walk-through of the "[Freqtrade](https://github.com/freqtrade/freqtrade)" open-source trading tool with a custom trading strategy. 

### Appendix: Past challenges

- [Challenge 1](challenges/main1.md) - predictions due Oct 16, 2022
- [Challenge: web3 ATL hackathon](challenges/hack1.md) - predictions due Nov 6, 2022
- [Challenge 2](challenges/main2.md) - predictions due Dec 11, 2022

### Development (WIP)

- [Developers flow](developers.md) - to further develop predict-eth
- [Release process](release-process.md) - to do a new release of predict-eth