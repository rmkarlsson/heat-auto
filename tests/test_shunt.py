import pytest
from appdaemon.apps.indoor_temp_ctrl.shunt import Shunt

class MockHass:
    def __init__(self):
        self.log_messages = []
        self.service_calls = []

    def log(self, msg):
        self.log_messages.append(msg)

    def call_service(self, service, entity_id=None):
        self.service_calls.append((service, entity_id))

    def get_state(self, entity_id=None):
        return "off"

    def run_in(self, callback, delay):
        callback(None)

@pytest.fixture
def hass():
    return MockHass()

@pytest.fixture
def shunt(hass):
    return Shunt(
        hass=hass,
        increase_entity="switch.shunt_up",
        decrease_entity="switch.shunt_down",
        max_steps=75
    )

def test_increase_once(shunt, hass):
    assert shunt.increase() is True
    assert shunt.last_direction == "up"
    assert shunt.direction_count == 1

def test_increase_75_times(shunt):
    for _ in range(75):
        assert shunt.increase() is True
    assert shunt.direction_count == 75

def test_increase_blocked_after_75(shunt, hass):
    for _ in range(75):
        shunt.increase()
    assert shunt.increase() is False

def test_direction_change_resets_counter(shunt):
    shunt.increase()
    shunt.increase()
    shunt.decrease()
    assert shunt.last_direction == "down"
    assert shunt.direction_count == 1

def test_decrease_75_times(shunt):
    for _ in range(75):
        assert shunt.decrease() is True
    assert shunt.direction_count == 75

def test_decrease_blocked_after_75(shunt, hass):
    for _ in range(75):
        shunt.decrease()
    assert shunt.decrease() is False