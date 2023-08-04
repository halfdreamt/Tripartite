from model.world import World

class modelManager:
    def __init__(self, master_data):

        # Initialize the world with master data (primarily model data)
        self.world = World(master_data)

    def get_map(self):
        return self.world.map  
    
    def get_time(self):
        return self.world.time
    
    def tick(self):
        self.world.tick()

    def get_entity_at(self, x, y):
        return self.world.entity_manager.get_entity_at(x, y)
    
    def get_world_info(self):
        world_data = {
            "map": self.world.map,
            "time": self.world.time
        }
        return world_data