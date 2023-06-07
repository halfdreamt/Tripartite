class healthComp:
    def __init__(self, health):
        self.health = health
        self.maxHealth = health

    def takeDamage(self, damage):
        self.health -= damage

    def heal(self, heal):
        self.health += heal
        if self.health > self.maxHealth:
            self.health = self.maxHealth

    def isDead(self):
        return self.health <= 0
    
    def get_info(self):
        return {"health": self.health, "maxHealth": self.maxHealth}