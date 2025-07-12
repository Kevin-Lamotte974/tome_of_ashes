import pygame

class Bar:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen, ratio):
        pygame.draw.rect(screen, (50, 50, 50), self.rect)
        pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, self.rect.width * ratio, self.rect.height))