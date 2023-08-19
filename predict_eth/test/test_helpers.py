from pytest import approx

from predict_eth import helpers


def test_calc_nmse():
    # super-basic test; a more thorough version is at
    # github.com/oceanprotocol/df-py/blob/main/df_py/challenge/test/test_nmse.py
    y = [1.0, 1.1, 1.2]
    yhat = [1.0 + 0.1, 1.1 - 0.05, 1.2 + 0.15]
    nmse = helpers.calc_nmse(y, yhat)
    assert nmse == approx(0.7)
