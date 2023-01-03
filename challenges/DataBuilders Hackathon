# Gitcoin Open Data Hackathon using Ocean Protocol
In the Ocean Protocol <> Gitcoin ODC Hackathon, contestants are incentivised to use Ocean's technology to find insightful anti-Sybil algorithms and to package anti-Sybil algorithms into composable legos with a fully decentrealised approach.


## 0. Key Details

- Kickoff: Jan 5th, 2023
- Submission deadline: Tuesday Jan 31st, 2023 at 23:59 UTC
- Total Prize pool: $40,000 in bounties

### 0.1 Outline of this README
This readme describes 2 different ways that participants can use to get free bonus points during the hackathon:

1. Publish your algorithms as ERC721 using the [Ocean Market](https://market.oceanprotocol.com/publish/1) frontend
2. Use Ocean [Data NFTs](https://docs.oceanprotocol.com/core-concepts/datanft-and-datatoken#what-is-a-data-nft) as [ERC725Y](https://github.com/ERC725Alliance/erc725/blob/main/docs/ERC-725.md) via [Ocean.py](https://github.com/oceanprotocol/ocean.py) or [Ocean.js](https://github.com/oceanprotocol/ocean.js)

## 1. Use Ocean Market frontend

Ocean Market provides a convenient interface for individuals and organizations to publish their data. Data assets can be datasets, algorithms,images, location information, audio, video, sales data, or combinations of all!

To publish on the Ocean Marketplace, you must first get MATIC or ETH to pay for gas fees, and host your assets on a decentralized storage like Arweave.
To host your data assets on Arweave you have two options, A and B. 

**Option A: Webapp, using [arweave.app](https://www.ardrive.io)**
For more info, access the [Ocean Docs](https://docs.oceanprotocol.com/using-ocean-market/asset-hosting#arweave) 

**Option B: In code, using [pybundlr library](https://github.com/oceanprotocol/pybundlr)** 

Once the above is completed, take the transaction ID and head over to [Ocean Market](https://market.oceanprotocol.com/publish/1) to get started with publishing. If you need more information feel free to ask for support in our dedicated [Discord channel](https://discord.gg/JK4rq7KBGh) or visit our [docs](https://docs.oceanprotocol.com/using-ocean-market/marketplace-publish-data-asset).


## 2. Use Ocean Data NFTs as ERC725Y

The ERC725y feature enables the NFT owner to input and update information in a key-value store. These values can be viewed externally by anyone and are highly useful building blocks for various Sybil protection approaches. Ocean has a first-class implementation of it, deployed on many networks, and with drivers. 

### 2.1 Via Ocean.py

Before getting started, ensure that you've already [installed Ocean.py](https://github.com/oceanprotocol/ocean.py/blob/main/READMEs/install.md) and [set it up remotely](https://github.com/oceanprotocol/ocean.py/blob/main/READMEs/setup-remote.md)


#### 2.1.1 Publish data NFT

In Python console:
```python
from ocean_lib.models.arguments import DataNFTArguments
data_nft = ocean.data_nft_factory.create(DataNFTArguments('NFT1', 'NFT1'), alice)
```

#### 2.1.2 Add key-value pair to data NFT

```python
# Key-value pair
key = "fav_color"
value = b"blue"
# prep key for setter
from web3.main import Web3
key_hash = Web3.keccak(text=key)  # Contract/ERC725 requires keccak256 hash
# set
data_nft.setNewData(key_hash, value, {"from": alice})
```

#### 2.1.3 Retrieve value from data NFT

```python
value2_hex = data_nft.getData(key_hash)
value2 = value2_hex.decode('ascii')
print(f"Found that {key} = {value2}")
```

That's it! All data was stored and retrieved from on-chain without using Ocean Provider or Ocean Aquarius (though the latter can help for fast querying & retrieval).

This way, we can also encrypt the data. Under the hood, it uses [ERC725](https://erc725alliance.org/), which augments ERC721 with a well-defined way to set and get key-value pairs.

If you need more information about Ocean ERC725y feel free to ask for support in our dedicated [Discord channel](https://discord.gg/JK4rq7KBGh). Alternatively, you can visit the full [README](https://github.com/oceanprotocol/ocean.py/blob/main/READMEs/key-value-flow.md) or our [docs](https://docs.oceanprotocol.com/core-concepts/datanft-and-datatoken#implementation-in-ocean-protocol).


### 2.2 Via Ocean.Js

Before getting started, ensure that you've already [installed Ocean.js]() and [set it up remotely]()

Using Ocean Data NFTs as [ERC725Y](https://github.com/ERC725Alliance/erc725/blob/main/docs/ERC-725.md) via Ocean.js can be helpful for dApp developers, particularly if you have prior experience with javascript.

The process involves creating a Data NFT (which represents the base-IP on-chain) and a datatoken (which will be used to purchase the dataset). Access the full [README](https://github.com/oceanprotocol/ocean.js/blob/main/CodeExamples.md#8-using-erc725-key-value-store) to get started.

If you need more information about Ocean ERC725y feel free to ask for support in our dedicated [Discord channel](https://discord.gg/JK4rq7KBGh) or visit our [docs](https://docs.oceanprotocol.com/core-concepts/datanft-and-datatoken#implementation-in-ocean-protocol).
