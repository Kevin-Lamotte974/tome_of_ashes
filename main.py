import pygame
from scenes.start_scene import StartScene
from scenes.game_scene import GameScene

# Initialisation Pygame
pygame.init()
WINDOW_SIZE = (1920, 1080)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Tome of Ashes")
clock = pygame.time.Clock()

# Constantes
BG_COLOR = (28, 37, 38)

def main():
    current_scene = StartScene()
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BG_COLOR)
        next_scene = current_scene.update(events)
        current_scene.draw(screen)
        if next_scene:
            current_scene = next_scene
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()