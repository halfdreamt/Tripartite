from model.component.need import need

class life:
    def __init__(self, health, thirst):
        self.moveVectorStack = []
        self.needs = []
        self.health = health
        self.thirst = thirst
            
    # adds a need to the needs array
    def addNeed(self, priorty, name):
        self.needs.append(need(priorty, name))

    # adjust need priority
    def adjustNeed(self, name, priority):
        for need in self.needs:
            if need.name == name:
                need.priority = priority
                return True
        return False