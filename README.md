# Predict ETH challenges

Data science challenges to predict the future price of ETH, with prizes. Uses [ocean.py](https://github.com/oceanprotocol/ocean.py) library.

### Current / future challenges

- [Challenge 2](challenges/main2.md) - predictions due Dec 11, 2022

### Example End-to-End Flows

Predict ETH price 1-12 ahead with various approaches:
- [Gentle introduction](examples/end-to-end-gentle.md) - to make onboarding easy as possible. Uses ETH data from ccxt, stock data from Ocean, and linear models
- [Simple](examples/end-to-end-via-raw-ocean-data-and-linear-models.md) - uses ETH data from Ocean, and linear models
- [Medium level: MA & EMA](examples/end-to-end-via-mas-and-emas.md) - Uses raw data, moving average (MA), and exponential moving average (EMA) data
- [Model comparison for direct prediction 1-12 hours](../examples/model_example_direct_prediction.md)
### Example Data Sources

Get ETH price data - various approaches:
- [Via Binance direct](examples/get-ethdata-binance-direct.md) - most direct, but specific to Binance
- [Via ccxt + Binance](examples/get-ethdata-ccxt-binance.md) - unified API across 40 exchanges
- [Via Ocean + Binance](examples/get-ethdata-ocean-binance.md) - unified API across 500+ data & compute services
- [Via Ocean + TheGraph](examples/get-ethdata-ocean-thegraph.md) - like previous, but uses a GraphQL-shaped query


Get BTC price data:
- [Via Ocean + Binance](examples/get-btcdata-ocean-binance.md)

### Data & Modeling Ideas

Here are ideas to get even more accurate results.

- [More data sources](ideas/data-sources.md)
- [Modeling approaches](ideas/modeling.md)
- [Articles](ideas/articles.md) on predicting ETH, etc


### Appendix: Past challenges

- [Challenge 1](challenges/main1.md) - predictions due Oct 16, 2022
- [Challenge: web3 ATL hackathon](challenges/hack1.md) - predictions due Nov 6, 2022
