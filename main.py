import pygame

from Interface import Interface
from Audio import Audio
pygame.init()

width = 1920
height = 1080
win = ((width, height))
clock = pygame.time.Clock()

pygame.display.set_caption("La Conquête Pirate")
window = pygame.display.set_mode(win, pygame.FULLSCREEN)

interface = Interface(window)
audio = Audio()

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pygame.quit()
                exit()

def main():
    run = True
    while run:
        quit_game()
        
        window.fill((0, 0, 0))
        interface.draw()
        
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()