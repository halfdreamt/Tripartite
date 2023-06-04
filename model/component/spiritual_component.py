class spiritual_component:
    def __init__(self, entity):
        self.entity = entity
        self.health = 20

    def update(self):
        if self.health <= 0:
            self.die()
    
    def die(self):
        health = 0