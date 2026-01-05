class Shunt:
    def __init__(self, hass, increase_entity, decrease_entity, max_steps=75):
        self.hass = hass
        self.increase_entity = increase_entity
        self.decrease_entity = decrease_entity
        self.max_steps = max_steps

        self.last_direction = None   # "up", "down" eller None
        self.direction_count = 0

    def _can_move(self, direction):
        if self.hass.get_state(entity_id=self.increase_entity) == "on" or self.hass.get_state(entity_id=self.decrease_entity) == "on":
            self.hass.log("Illegal shunt action: Not possible to move when shunt is on")
            self.hass.call_service("switch/turn_off", entity_id=self.increase_entity)
            self.hass.call_service("switch/turn_off", entity_id=self.decrease_entity)
            return False

        if self.last_direction != direction:
            return True
        self.hass.log("_can_move: " + str(self.direction_count))
        return self.direction_count < self.max_steps

    def _register_move(self, direction):
        if self.last_direction == direction:
            self.direction_count += 1
        else:
            self.last_direction = direction
            self.direction_count = 1
        self.hass.log("dir_cnt:" +  str(self.direction_count))

    def increase(self):
        if not self._can_move("up"):
            self.hass.log("Shunt: Max opened, no possible to increase more, no action")
            return False

        self.hass.log("Shunt: Increase (open active for 2 sekund)")
        self.hass.call_service("switch/turn_on", entity_id=self.increase_entity)
        self.hass.run_in(lambda _: self.hass.call_service("switch/turn_off", entity_id=self.increase_entity), 2)

        self._register_move("up")
        return True

    def decrease(self):
        if not self._can_move("down"):
            self.hass.log("Shunt: Max closed, no possible to decrease more, no action")
            return False

        self.hass.log("Shunt: Decrease (close active for 2 sekund)")
        self.hass.call_service("switch/turn_on", entity_id=self.decrease_entity)
        self.hass.run_in(lambda _: self.hass.call_service("switch/turn_off", entity_id=self.decrease_entity), 2)

        self._register_move("down")
        return True
