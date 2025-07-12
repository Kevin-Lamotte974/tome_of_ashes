class Enemy:
    def __init__(self, name, health, strength, wave):
        self.name = name
        self.max_health = health * (1 + wave * 0.1)
        self.health = self.max_health
        self.strength = strength * (1 + wave * 0.1)