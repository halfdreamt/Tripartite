class wanderSystem:
    def __init__(self, wanderRadius, wanderDistance, wanderJitter):
        self.wanderRadius = wanderRadius
        self.wanderDistance = wanderDistance
        self.wanderJitter = wanderJitter
        self.entites = []

    def component_updated(self, component):
        if component.get_name() == "movement":
            self.entities.append(component.entity)