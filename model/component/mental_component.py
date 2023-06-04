from model.system.mental_system import mental_system

class mental_component:
    def __init__(self, entity):
        # set local data and references
        self.entity = entity
        self.map = entity.world.map

        # TODO: this should be more dynamic, hard coding health and willWander is bad
        self.health = 20
        self.willWander = True

        # initialize mental system; behavior
        self.mental_system = mental_system(self)