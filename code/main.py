from random import randint
import sys
import pygame
from level import Level
from settings import *


class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Trick or Treat!')
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('#477861')
            self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
 