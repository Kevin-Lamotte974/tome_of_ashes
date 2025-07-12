import time

class Player:
    def __init__(self, name):
        self.name = name
        self.mana = 10
        self.strength = 5
        self.endurance = 50
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100
        self.gold = 0
        self.fragments = 0
        self.spells = {}
        self.allies = []
        self.prestige_bonus = 1.0
        self.achievements = {"Enemies Defeated": 0}
        self.last_time = time.time()

    def gain_xp(self, amount):
        amount = int(amount * self.prestige_bonus)
        self.xp += amount
        messages = []
        while self.xp >= self.xp_to_next_level:
            self.level += 1
            self.xp -= self.xp_to_next_level
            self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
            self.mana += 5
            self.strength += 2
            self.endurance += 10
            messages.append(f"Niveau {self.level} atteint !")
        return messages

    def check_achievements(self):
        messages = []
        if self.achievements["Enemies Defeated"] >= 50:
            self.gold += 100
            messages.append("Succès : Chasseur de monstres ! +100 or.")
            self.achievements["Enemies Defeated"] = -999
        return messages