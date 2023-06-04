class spiritual_component:
    def __init__(self, entity, type):
        self.entity = entity
        self.type = type
        self.health = 20

    def update(self):
        if self.health <= 0:
            self.die()
    
    def die(self):
        health = 0