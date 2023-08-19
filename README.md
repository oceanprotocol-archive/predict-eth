# Challenge DF

Challenge DF is a data science competition, run as part of Ocean Data Farming (DF). Each week, there is 5,000 OCEAN available, going to those who predict the price of ETH with the lowest error.

**To participate, follow: [Challenge DF Instructions](challenges/challenge-df.md)**

More info: ["Introducing Challenge DF"](https://blog.oceanprotocol.com/introducing-challenge-data-farming-378bba28fc97).

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
- [Articles](ideas/articles.md) on predicting ETH, etc

### Inspiration from algorithmic trading 

Getting into the head of a trader might inspire you in predicting ETH.

To help with that, the [algorithmic trading flow README](ideas/algorithmic-trading-flow.md) does a walk-through of the "[Freqtrade](https://github.com/freqtrade/freqtrade)" open-source trading tool with a custom trading strategy. 

### Appendix: Past challenges

Before Challenge DF, we held monthly "Predict-ETH" Challenges from Oct 2022 to Jul 2023 (7 total). Here they are:

- [Predict-ETH Round 1](challenges/main1.md) - predictions due Oct 16, 2022 at 23.59 UTC. [Announcement](https://blog.oceanprotocol.com/ocean-protocol-announces-the-launch-of-the-eth-prediction-challenge-7b1f04cc820e)
- [Predict-ETH special: web3 ATL hackathon](challenges/hack1.md) - predictions due Nov 6, 2022
- [Predict-ETH Round 2](challenges/main2.md) - predictions due Dec 11, 2022 at 23.59 UTC. [Announcement](https://blog.oceanprotocol.com/ocean-protocol-challenge-predict-eth-price-2nd-edition-9400212a30db), [Winners](https://blog.oceanprotocol.com/introducing-the-winners-of-the-eth-price-prediction-data-challenge-edition-2-6acdccb9271)
- [Predict-ETH Round 3](challenges/main3.md) - predictions due Mon Feb 20, 2023 at 23.59 UTC. [Announcement](https://blog.oceanprotocol.com/ocean-protocol-launches-the-3rd-edition-of-predict-eth-ccb7e6a62bf7), [Winners](https://blog.oceanprotocol.com/introducing-the-winners-of-the-predict-eth-3-data-challenge-f4ed7fb8e467)
- [Predict-ETH Round 4](challenges/main4.md) - predictions due Wed Apr 5, 2023 at 23.59 UTC.. [Announcement](https://blog.oceanprotocol.com/predict-eth-4-dive-into-decentralized-data-355f2281509e), [Winners](https://blog.oceanprotocol.com/here-are-the-winners-of-the-predict-eth-round-4-data-challenge-1672b36c0af9)
- [Predict-ETH Round 5](challenges/main5.md) - predictions due Wed May 3, 2023  at 23.59 UTC. [Announcement](https://blog.oceanprotocol.com/predict-eth-round-5-data-challenge-is-live-d031b4ca971a), [Winners](https://medium.com/@TeamOcean/here-are-the-winners-of-the-predict-eth-round-5-data-challenge-95f71bcade95)
- [Predict-ETH Round 6](challenges/main6.md) - predictions due Wed Jun 7, 2023 at 23.59 UTC. [Announcement](https://blog.oceanprotocol.com/predict-eth-round-6-data-challenge-is-live-d305502888f9), [Winners](https://blog.oceanprotocol.com/here-are-the-winners-of-the-predict-eth-round-6-data-challenge-9b8e8f786170)
- [Predict-ETH Round 7](challenges/main7.md) - predictions due Wed Jul 5, 2023 at 23.59 UTC [Announcement](https://blog.oceanprotocol.com/predict-eth-round-7-data-challenge-is-live-9be6d7faa4a1), [Winners](https://blog.oceanprotocol.com/here-are-the-winners-of-the-predict-eth-round-7-data-challenge-d5ec1c2056e0)

### Appendix: Predict-eth library

Predict-eth is a [library on pypi](https://pypi.org/project/predict-eth/).

To install: `pip3 install predict-eth`

To further develop it :
- [Developers flow](developers.md)
- [Release process](release-process.md)
