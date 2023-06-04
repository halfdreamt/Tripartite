from model.system.mental_system import mental_system

class mental_component:
    def __init__(self, entity, type):
        self.entity = entity
        self.health = 20
        self.type = type
        self.moveDirection = None
        self.willWander = True
        self.pendingMove = False
        self.mental_system = mental_system(self)