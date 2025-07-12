import time
import random
from entities.player import Player
from entities.enemy import Enemy

class Game:
    def __init__(self):
        self.player = None
        self.enemies = [
            Enemy("Mutant errant", 20, 5, 1),
            Enemy("Drone rouillé", 50, 2, 1)
        ]
        self.wave = 1
        self.log = []
        self.combat_active = False
        self.combat_enemy = None
        self.combat_timer = 0

    def log_message(self, message):
        self.log.append(message)
        if len(self.log) > 20:
            self.log.pop(0)

    def calculate_offline_bonus(self):
        if self.player:
            elapsed = time.time() - self.player.last_time
            bonus_mana = int(elapsed // 60)
            if bonus_mana > 0:
                bonus_mana = min(bonus_mana, 1440)
                self.player.mana += bonus_mana
                self.log_message(f"+{bonus_mana} mana gagné hors ligne !")
            self.player.last_time = time.time()

    def train(self):
        if self.player and self.player.mana >= 5:
            self.player.strength += 1
            self.player.mana -= 5
            messages = self.player.gain_xp(10)
            self.log_message("Tu t'entraînes dans les ruines... Force +1 !")
            for msg in messages:
                self.log_message(msg)
            if random.random() < 0.05:
                self.random_event()

    def meditate(self):
        if self.player:
            self.player.mana += 5 * self.player.prestige_bonus
            messages = self.player.gain_xp(5)
            self.log_message("Tu médites sous un ciel rouge... Mana +5 !")
            for msg in messages:
                self.log_message(msg)
            if self.player.level >= 5 and "Aura de mana" not in self.player.spells:
                self.player.spells["Aura de mana"] = {"level": 1, "type": "passive", "effect": 1}
                self.log_message("Sort passif 'Aura de mana' appris ! +1 mana/seconde.")
            if random.random() < 0.05:
                self.random_event()

    def explore_dungeon(self):
        if self.player and self.player.mana >= 10 and self.player.endurance > 0 and not self.combat_active:
            self.combat_active = True
            self.combat_enemy = random.choice(self.enemies)
            self.combat_enemy.wave = self.wave
            self.combat_enemy.health = self.combat_enemy.max_health
            self.combat_timer = time.time()
            self.log_message(f"Vague {self.wave}: Un {self.combat_enemy.name} apparaît !")

    def update_combat(self):
        if self.combat_active and self.combat_enemy:
            if time.time() - self.combat_timer >= 1:
                spell_dmg = sum(spell["effect"] for spell, data in self.player.spells.items() if data["type"] == "active")
                ally_dmg = len(self.player.allies) * 5
                self.combat_enemy.health -= self.player.strength + spell_dmg + ally_dmg
                self.player.mana -= 10
                self.player.endurance -= self.combat_enemy.strength
                self.log_message(f"[COMBAT] Tu infliges {self.player.strength + spell_dmg + ally_dmg} dégâts !")
                if self.combat_enemy.health <= 0:
                    gold = int(random.randint(5, 15) * self.player.prestige_bonus)
                    fragments = int(random.randint(1, 3) * self.player.prestige_bonus)
                    self.player.gold += gold
                    self.player.fragments += fragments
                    self.player.achievements["Enemies Defeated"] += 1
                    messages = self.player.gain_xp(30)
                    self.log_message(f"{self.combat_enemy.name} vaincu ! +{gold} or, +{fragments} fragments.")
                    for msg in messages + self.player.check_achievements():
                        self.log_message(msg)
                    self.wave += 1
                    if random.random() < 0.1:
                        self.log_message("Fragment de journal : 'La Pierre Philosophale a tout consumé...'")
                    self.combat_active = False
                elif self.player.mana < 10 or self.player.endurance <= 0:
                    self.log_message("Tu fuis le combat !")
                    self.combat_active = False
                    self.wave = 1
                self.combat_timer = time.time()
                if random.random() < 0.05:
                    self.random_event()

    def random_event(self):
        event = random.choice(["Marchand", "Embuscade"])
        if event == "Marchand":
            self.log_message("Un marchand propose un sort rare pour 100 or.")
        elif event == "Embuscade":
            self.log_message("Une embuscade ! Un ennemi surprise attaque !")
            self.explore_dungeon()