## Get Binance BTC/USDT price feed via Ocean

This is published as a free asset in Ocean. Under the hood, it queries the Binance API.

You can see it on Ocean Market [here](https://market.oceanprotocol.com/asset/did:op:b4584760f5133b27d91c337b9c10b56448b84a1bae39b8c1037d0de33023b4dc).

### 0. Setup

From [Challenge 2](../challenges/main2.md), do:

- [x] Setup

### 1. Get Data

In Python console:

```python
BTC_USDT_did = "did:op:b4584760f5133b27d91c337b9c10b56448b84a1bae39b8c1037d0de33023b4dc"

file_name = ocean.assets.download_file(BTC_USDT_did, alice_wallet)
```

### 2. Open data

From [ETH price via Ocean + Binance](get-ethdata-ocean-binance.md)
- Apply the same approaches for here.
