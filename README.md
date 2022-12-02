# Predict ETH challenges

Data science challenges to predict the future price of ETH, with prizes. Uses [ocean.py](https://github.com/oceanprotocol/ocean.py) library.

This competition is run by the Ocean core team (Ocean Protocol Foundation).

Our aim is to help people understand "data value creation flows", that is, how data can be used to create value. In this competition, it's about starting with raw data and creating feature vectors, creating models, and ultimately making predictions of the future price of ETH.

If you can predict the price of ETH accurately, you can immediately create value from it, by buying or selling ETH. More advanced use cases are in quantitative DeFi trading, yield farming or DeFi protocol development.

Then the challenge is: how accurately can _you_ predict the price of ETH? 

### Current / future challenges

- [Challenge 2](challenges/main2.md) - predictions due Dec 11, 2022

### Example End-to-End Flows

These are example full submissions to the challenge. You can use any of them as a starting point.

- [Simple](examples/end-to-end_simple.md): To-the-point example, with simple input data (just ETH price) and simple model (linear dynamical model)
- [Compare models, direct prediction](examples/end-to-end_compare-models.md): Build models that predict 1-12 hours ahead in one shot. Compare linear, SVM, RF, and NN models.

These flows are WIP, and not quite modeling end-to-end yet. Stay tuned:)
- [Gentle introduction, lots of data](examples/end-to-end-gentle.md):  Gentle intro for smooth onboarding. Uses stock data and ETH price for inputs. Builds a linear model.
- [Medium level: MA & EMA](examples/end-to-end-via-mas-and-emas.md): Use raw data, moving average (MA), and exponential moving average (EMA) data.

### Example Data Sources

These are examples of how to get data from various places. Each place has its own benefits.

Get ETH price data:
- [Via Binance direct](examples/get-ethdata-binance-direct.md) - most direct, but specific to Binance
- [Via ccxt + Binance](examples/get-ethdata-ccxt-binance.md) - unified API across 40 exchanges
- [Via Ocean + Binance](examples/get-ethdata-ocean-binance.md) - unified API across 500+ data & compute services
- [Via Ocean + TheGraph](examples/get-ethdata-ocean-thegraph.md) - like previous, but uses a GraphQL-shaped query


Get BTC price data:
- [Via Ocean + Binance](examples/get-btcdata-ocean-binance.md)

### Inspiration: ideas for data & modeling

Here are ideas to get even more accurate results.

- [More data sources](ideas/data-sources.md)
- [Modeling approaches](ideas/modeling.md)
- [Articles](ideas/articles.md) on predicting ETH, etc

### Inspiration from algorithmic trading 

Getting into the head of a trader might inspire you in your work on predicting ETH.

To help with that, check out [algorithmic trading flow README](ideas/algorithmic-trading-flow.md) does a walk-through of using the "[Freqtrade](https://github.com/freqtrade/freqtrade)" open-source trading tool with a custom trading strategy. 

### Appendix: Past challenges

- [Challenge 1](challenges/main1.md) - predictions due Oct 16, 2022
- [Challenge: web3 ATL hackathon](challenges/hack1.md) - predictions due Nov 6, 2022
