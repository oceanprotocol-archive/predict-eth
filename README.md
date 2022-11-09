# Predict ETH challenges

Data science challenges to predict the future price of ETH, with prizes. Uses [ocean.py](https://github.com/oceanprotocol/ocean.py) library.

### Current / future challenges

- [Challenge 2](challenges/main2.md) - predictions due Dec 11, 2022

### Example End-to-End Flows

Predict ETH price 1-12 ahead with various approaches:
- [Via raw data from Ocean and linear models](examples/predict-eth-ocean-data-linear-models.md)
- [Via raw data, moving average (MA), and exponential moving average (EMA)](examples/real-time-raw-mas-emas.md)

### Example Data Sources

Get ETH price data with various approaches:
- [Via Binance direct](examples/get-data-binance-direct.md) - most direct, but specific to Binance
- [Via ccxt + Binance](examples/get-data-ccxt-binance.md) - unified API across 40 exchanges
- [Via Ocean + Binance](examples/get-data-ocean-binance.md) - unified API across 500+ data & compute services
- [Via Ocean + TheGraph](examples/get-data-ocean-the-graph.md) - like previous, but uses a GraphQL-shaped query

### Data & Modeling Ideas

Here are ideas to get even more accurate results.

- [More data sources](ideas/data-sources.md)
- [Modeling approaches](ideas/modeling.md)
- [Articles](ideas/articles.md) on predicting ETH, etc

### Appendix: Past challenges

- [Challenge 1](challenges/main1.md) - predictions due Oct 16, 2022
- [Challenge: web3 ATL hackathon](challenges/hack1.md) - predictions due Nov 6, 2022
