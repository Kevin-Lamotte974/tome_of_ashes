import json
import os
from core.game import Game
from entities.player import Player

def save_game(game):
    if game.player:
        data = {
            "name": game.player.name,
            "mana": game.player.mana,
            "strength": game.player.strength,
            "endurance": game.player.endurance,
            "level": game.player.level,
            "xp": game.player.xp,
            "xp_to_next_level": game.player.xp_to_next_level,
            "gold": game.player.gold,
            "fragments": game.player.fragments,
            "spells": game.player.spells,
            "allies": game.player.allies,
            "prestige_bonus": game.player.prestige_bonus,
            "achievements": game.player.achievements
        }
        with open("data/save.json", "w") as f:
            json.dump(data, f)
        game.log_message("Jeu sauvegardé !")

def load_game():
    try:
        with open("data/save.json", "r") as f:
            data = json.load(f)
        game = Game()
        game.player = Player(data["name"])
        game.player.mana = data["mana"]
        game.player.strength = data["strength"]
        game.player.endurance = data["endurance"]
        game.player.level = data["level"]
        game.player.xp = data["xp"]
        game.player.xp_to_next_level = data["xp_to_next_level"]
        game.player.gold = data["gold"]
        game.player.fragments = data["fragments"]
        game.player.spells = data["spells"]
        game.player.allies = data["allies"]
        game.player.prestige_bonus = data["prestige_bonus"]
        game.player.achievements = data["achievements"]
        game.calculate_offline_bonus()
        game.log_message("Partie chargée !")
        return game
    except FileNotFoundError:
        return None