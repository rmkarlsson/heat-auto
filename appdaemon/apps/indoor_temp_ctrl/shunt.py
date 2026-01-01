class Shunt:
    def __init__(self, hass, increase_entity, decrease_entity, max_steps=75):
        self.hass = hass
        self.increase_entity = increase_entity
        self.decrease_entity = decrease_entity
        self.max_steps = max_steps

        self.last_direction = None   # "up", "down" eller None
        self.direction_count = 0

    def _can_move(self, direction):
        if self.last_direction != direction:
            return True
        return self.direction_count < self.max_steps

    def _register_move(self, direction):
        if self.last_direction == direction:
            self.direction_count += 1
        else:
            self.last_direction = direction
            self.direction_count = 1

    def increase(self):
        if not self._can_move("up"):
            self.hass.log("Shunt: Kan inte öka mer, bottnad uppåt")
            return False

        self.hass.log("Shunt: Ökar (aktiverar relä i 1 sekund)")
        self.hass.call_service("switch/turn_on", entity_id=self.increase_entity)
        self.hass.run_in(lambda _: self.hass.call_service("switch/turn_off", entity_id=self.increase_entity), 1)

        self._register_move("up")
        return True

    def decrease(self):
        if not self._can_move("down"):
            self.hass.log("Shunt: Kan inte minska mer, bottnad nedåt")
            return False

        self.hass.log("Shunt: Minskar (aktiverar relä i 1 sekund)")
        self.hass.call_service("switch/turn_on", entity_id=self.decrease_entity)
        self.hass.run_in(lambda _: self.hass.call_service("switch/turn_off", entity_id=self.decrease_entity), 1)

        self._register_move("down")
        return True
