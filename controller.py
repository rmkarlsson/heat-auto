import appdaemon.plugins.hass.hassapi as hass
from .heating_curve import HeatingCurve
from .shunt import Shunt

class IndoorTempCtrl(hass.Hass):

    def terminate(self):
        self.log("Gracefull shutdown in apps")
        self.log("Power off shunt")
        self.shunt.hass.call_service("switch/turn_off", entity_id=self.shunt.increase_entity)
        self.shunt.hass.call_service("switch/turn_off", entity_id=self.shunt.decrease_entity)


    def initialize(self):
        self.framledning_sensor = "sensor.d1mini_framledningstemperatur"
        self.weather_entity = "weather.forecast_home"

        # Värmekurva
        heating_table = {
            -30: 40,
            -25: 38,
            -20: 34,
            -15: 34,
            -10: 32,
            -5: 30,
            0: 28,
            5: 25,
            10: 23,
            15: 21,
        }
        self.curve = HeatingCurve(heating_table)

        # Shunt
        self.shunt = Shunt(
            hass=self,
            increase_entity="switch.0x54ef44100120aedb_l2",
            decrease_entity="switch.0x54ef44100120aedb_l1",
            max_steps=75
        )
        self.run_every(self.loop, "now", 60)
        self.log("indoor_temp_ctrl startad")
        self.temp_log_state = False

    def loop(self, kwargs):
        # 1. Framledning
        fram_temp = self.get_state(self.framledning_sensor)
        if fram_temp is None:
            self.log("Missing framledningstemperatur")
            return
        fram_temp = float(fram_temp)

        # 2. Utetemp
        outdoor_temp = self.get_state(self.weather_entity, attribute="temperature")
        if outdoor_temp is None:
            self.log("Missing outdoor temperatur")
            return
        outdoor_temp = float(outdoor_temp)

        # 3. Målfamledning
        target_temp = self.curve.get(outdoor_temp)

        # 4. Diff
        diff = target_temp - fram_temp
        if not self.temp_log_state:
            self.log(f"Outdoor: {outdoor_temp}, Fwd: {fram_temp}, Target: {target_temp}, Diff: {diff:.2f}")
            self.temp_log_state = True

        # 5. Deadband ±2°C
        if abs(diff) <= 2:
            return

        self.temp_log_state = False

        # 6. Styr shunten
        if diff > 2:
            self.shunt.increase()
        elif diff < -2:
            self.shunt.decrease()
