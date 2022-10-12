import pygame
import os


# TODO: do this later, if the loading becomes too large of a problem
# class SpritesheetHandler:
#   def __init__(self):
#     self.spritesheets = {
#       'monsters': os.path.join('graphics', 'monsters.png'),
#       'particles': os.path.join('graphics', 'particles.png'),
#       'player': os.path.join('graphics', 'player.png')
#     }

# class Spritesheet(pygame.sprite.Sprite):
#     def __init__(self, filename, *groups):
#         super().__init__(*groups)
#         self.filename = filename
#         self.spritesheet = pygame.image.load(filename).convert_alpha()

#     def get_sprite(self, x, y, w, h, scale):
#         sprite = pygame.Surface((w, h), pygame.SRCALPHA)
#         sprite.blit(self.spritesheet, (0, 0), (x*w, y*h, w, h))
#         sprite = pygame.transform.scale(sprite,(w*scale, h*scale))
#         return sprite


