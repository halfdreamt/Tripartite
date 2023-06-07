class positionComp:
    def __init__(self, x, y, world):
        self.x = x
        self.y = y
        self.world = world

    def get_info(self):
        return {"x": self.x, "y": self.y}