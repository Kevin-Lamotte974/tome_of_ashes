import pygame
from ui.button import Button
from scenes.game_scene import GameScene
from core.game import Game
from core.save_load import load_game
from entities.player import Player

class StartScene:
    def __init__(self):
        self.name_input = ""
        self.font = pygame.font.SysFont("arial", 24)
        self.font_small = pygame.font.SysFont("arial", 16)
        self.buttons = [
            Button("Commencer", 300, 300, 150, 40, self.start_game),
            Button("Charger", 300, 350, 150, 40, self.load_game)
        ]

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                for btn in self.buttons:
                    btn.check_hover(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.buttons:
                    btn.click()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return self.start_game()
                elif event.key == pygame.K_BACKSPACE:
                    self.name_input = self.name_input[:-1]
                else:
                    self.name_input += event.unicode
        return None

    def draw(self, screen):
        screen.fill((28, 37, 38))
        screen.blit(self.font.render("Tome of Ashes", True, (224, 224, 224)), (300, 100))
        screen.blit(self.font_small.render("Entrez votre nom :", True, (224, 224, 224)), (300, 200))
        screen.blit(self.font_small.render(self.name_input, True, (224, 224, 224)), (300, 250))
        for btn in self.buttons:
            btn.draw(screen)

    def start_game(self):
        if self.name_input.strip():
            game = Game()
            game.player = Player(self.name_input)
            game.calculate_offline_bonus()
            return GameScene(game)
        return None

    def load_game(self):
        game = load_game()
        if game:
            return GameScene(game)
        return None