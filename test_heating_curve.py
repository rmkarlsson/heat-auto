import pytest
from appdaemon.apps.indoor_temp_ctrl.heating_curve import HeatingCurve

@pytest.fixture
def curve():
    table = {
        -30: 55,
        -25: 52,
        -20: 50,
        -15: 47,
        -10: 45,
        -5: 42,
        0: 38,
        5: 34,
        10: 30,
        15: 25,
    }
    return HeatingCurve(table)

def test_exact_lookup(curve):
    assert curve.get(-20) == 50

def test_interpolation(curve):
    result = curve.get(-17.5)
    assert abs(result - 48.5) < 0.01

def test_below_min(curve):
    assert curve.get(-40) == 55

def test_above_max(curve):
    assert curve.get(20) == 25
