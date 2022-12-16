
## Developing pybundlr

This README is for those further improving the pybundlr library.

### Installation from source

In a new terminal:

```console
#clone the repo and enter into it
git clone https://github.com/oceanprotocol/pybundlr
cd pybundlr

#Create & activate venv
python -m venv venv
source venv/bin/activate

#Install modules in the environment
pip3 install -r requirements.txt
```

### Set envvars

Some tests need an Ethereum account holding >0 ETH. If you need, go create one and get some ETH.

Then, from the terminal:
```console
export REMOTE_TEST_PRIVATE_KEY1=<your account private key>
```

### Testing

From the terminal:
```console
pytest
```

### Usage

From the same terminal: `python`

Then, in Python console:
```python
# (do the same as in the main README)
```
