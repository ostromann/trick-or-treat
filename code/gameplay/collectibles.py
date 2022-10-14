import pygame
from gameplay.support import *

class Collectible(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)

  def import_graphics(self,name):
    self.animations = {'idle': []}
    main_path = f'graphics/collectibles/{name}/'
    for animation in self.animations.keys():
      self.animations[animation] = import_folder(main_path + animation)


class XP(Collectible):
  def __init__(self, pos, groups, amount):
    super().__init__(groups)
    self.sprite_type = 'collectible'

    self.frame_index = 0
    self.animation_speed = 0.15

    # graphics setup
    self.import_graphics('xp')
    self.status = 'idle'
    self.image = self.animations[self.status][self.frame_index]

    self.rect = self.image.get_rect(topleft = pos)
    self.hitbox = self.rect

    # interaction setup
    self.amount = amount

  def animate(self):
    animation = self.animations[self.status]

    # loop over the frame_index
    self.frame_index += self.animation_speed
    self.frame_index %= len(animation)

    # set the image
    self.image = animation[int(self.frame_index)]
    self.rect = self.image.get_rect(center = self.hitbox.center)

  def update(self,dt,actions):
    self.animate()