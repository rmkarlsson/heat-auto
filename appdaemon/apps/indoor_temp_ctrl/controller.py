import appdaemon.plugins.hass.hassapi as hass
from .heating_curve import HeatingCurve
from .shunt import Shunt

class IndoorTempCtrl(hass.Hass):

    def initialize(self):
        self.framledning_sensor = "sensor.d1mini_framledningstemperatur"
        self.weather_entity = "weather.forecast_home"

        # Värmekurva
        heating_table = {
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
        self.curve = HeatingCurve(heating_table)

        # Shunt
        self.shunt = Shunt(
            hass=self,
            increase_entity="switch.0x54ef44100120aedb_l1",
            decrease_entity="switch.0x54ef44100120aedb_l2",
            max_steps=75
        )
        self.run_every(self.loop, "now", 30)
        self.log("indoor_temp_ctrl startad")

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

        self.log(f"Outdoor: {outdoor_temp}°C, actutal heat in: {fram_temp}°C, target heat in: {target_temp}°C, Diff: {diff:.2f}°C")

        # 5. Deadband ±2°C
        if abs(diff) <= 2:
            self.log("Within deadband (±2°C), no shunt adjustement")
            return

        # 6. Styr shunten
        if diff > 2:
            self.shunt.increase()
        elif diff < -2:
            self.shunt.decrease()
