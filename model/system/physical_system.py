class physical_system:
    def __init__(self, physical_component):
        # set local references
        self.physical = physical_component
        self.world = physical_component.entity.world
        self.entity = physical_component.entity

    # perform checks and such
    def update(self):
        if self.physical.health <= 0:
            self.die()
    
    def die(self):
        self.health = 0