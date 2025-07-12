import pygame

class Button:
    def __init__(self, text, x, y, width, height, action):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.hovered = False
        self.active = True
        self.font = pygame.font.SysFont("arial", 16)

    def draw(self, screen):
        if not self.active:
            pygame.draw.rect(screen, (100, 100, 100), self.rect)
        else:
            color = (90, 106, 122) if self.hovered else (62, 76, 89)
            pygame.draw.rect(screen, color, self.rect)
        text_surf = self.font.render(self.text, True, (224, 224, 224))
        screen.blit(text_surf, (self.rect.x + 10, self.rect.y + 10))

    def check_hover(self, pos):
        if self.active:
            self.hovered = self.rect.collidepoint(pos)

    def click(self):
        if self.hovered and self.active:
            self.action()