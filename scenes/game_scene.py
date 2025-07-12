import pygame
from ui.button import Button
from ui.bar import Bar
from core.save_load import save_game

class GameScene:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("arial", 16)
        self.buttons = [
            Button("S'entraîner", 20, 150, 150, 40, self.game.train),
            Button("Méditer", 20, 200, 150, 40, self.game.meditate),
            Button("Explorer donjon", 20, 250, 150, 40, self.game.explore_dungeon),
            Button("Rechercher sort", 20, 300, 150, 40, lambda: self.game.log_message("Sort non implémenté")),
            Button("Invoquer allié", 20, 350, 150, 40, lambda: self.game.log_message("Allié non implémenté")),
            Button("Interagir", 20, 400, 150, 40, lambda: self.game.log_message("Narration non implémentée")),
            Button("Prestige", 20, 450, 150, 40, lambda: self.game.log_message("Prestige non implémenté")),
            Button("Sauvegarder", 20, 500, 150, 40, lambda: save_game(self.game)),
            Button("Quitter", 20, 550, 150, 40, self.quit)
        ]
        self.buttons[-2].active = game.player.level >= 20 if game.player else False
        self.xp_bar = Bar(20, 110, 200, 20, (76, 175, 80))
        self.choice_active = None

    def update(self, events):
        if self.game.player and "Aura de mana" in self.game.player.spells:
            self.game.player.mana += self.game.player.spells["Aura de mana"]["effect"] / 60
        if self.game.combat_active:
            self.game.update_combat()
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                for btn in self.buttons:
                    btn.check_hover(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.buttons:
                    btn.click()
        return None

    def draw(self, screen):
        screen.fill((28, 37, 38))
        stats_text = (f"Nom: {self.game.player.name}\nNiveau: {self.game.player.level} | XP: {self.game.player.xp}/{self.game.player.xp_to_next_level}\n"
                      f"Mana: {self.game.player.mana:.1f} | Force: {self.game.player.strength}\n"
                      f"Endurance: {self.game.player.endurance:.1f}\nOr: {self.game.player.gold} | Fragments: {self.game.player.fragments}")
        y = 10
        for line in stats_text.split("\n"):
            screen.blit(self.font.render(line, True, (224, 224, 224)), (20, y))
            y += 20
        self.xp_bar.draw(screen, self.game.player.xp / self.game.player.xp_to_next_level if self.game.player else 0)
        for btn in self.buttons:
            btn.draw(screen)
        y = 150
        for msg in self.game.log[-10:]:
            screen.blit(self.font.render(msg, True, (224, 224, 224)), (600, y))
            y += 20
        if self.game.combat_active and self.game.combat_enemy:
            pygame.draw.rect(screen, (50, 50, 50), (300, 300, 200, 20))
            ratio = max(self.game.combat_enemy.health / self.game.combat_enemy.max_health, 0)
            pygame.draw.rect(screen, (200, 50, 50), (300, 300, 200 * ratio, 20))
            screen.blit(self.font.render(f"{self.game.combat_enemy.name} - Vague {self.game.wave}", True, (224, 224, 224)), (300, 270))

    def quit(self):
        save_game(self.game)
        pygame.quit()
        exit()