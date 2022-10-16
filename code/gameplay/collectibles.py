import pygame
from gameplay.support import *
from gameplay.entity import Entity
from gameplay.entity_fsm import EntityFSM, State, TimedState


class DroppedState(State):  
  def update(self,sprite,dt,actions):
    # TODO: SFX
    # sprite.drop_sound.play()
    self.check_done(sprite)
    pass

  def check_done(self, sprite):
    distance, _ = get_distance_direction_a_to_b(sprite.pos, sprite.player.pos)

    margin = sprite.player.stats['item_pull_range'] * 2
    if distance <= margin:
      self.done = True

class PulledSoftState(State):
  def startup(self,sprite):
    sprite.speed = sprite.player.stats['item_pull_force'] / 2
    sprite.target_pos = sprite.player.pos
    
  def update(self,sprite,dt,actions):
    sprite.target_pos = sprite.player.pos
    self.check_done(sprite)
      
  def check_done(self, sprite):
    distance, _ = get_distance_direction_a_to_b(sprite.pos, sprite.player.pos)

    margin = sprite.player.stats['item_pull_range']
    if distance <= margin:
      self.done = True

class PulledStrongState(State):
  def startup(self,sprite):
    sprite.speed =  sprite.player.stats['item_pull_force']
    sprite.target_pos = sprite.player.pos
    
  def update(self,sprite,dt,actions):
    sprite.target_pos = sprite.player.pos
    self.check_done(sprite)
      
  def check_done(self, sprite):
    if pygame.sprite.collide_rect(sprite, sprite.player):    
      self.done = True

class CollectedState(State):
  def startup(self,sprite):
    # TODO: SFX

    sprite.player.exp += sprite.amount
    sprite.kill()




class Collectible(Entity):
  def __init__(self, groups, player):
    super().__init__(groups)

    self.player = player

    # FSM setup
    self.fsm = EntityFSM(self)
    self.fsm.states['dropped'] = DroppedState('dropped', next_state='pulled_soft')
    self.fsm.states['pulled_soft'] = PulledSoftState('dropped', next_state='pulled_strong')
    self.fsm.states['pulled_strong'] = PulledStrongState('pulled_strong', next_state='collected')
    self.fsm.states['collected'] = CollectedState('collected')
    self.fsm.current_state = self.fsm.states['dropped']

  def import_graphics(self,name):
    self.animations = {'idle': []}
    main_path = f'graphics/collectibles/{name}/'
    for animation in self.animations.keys():
      self.animations[animation] = import_folder(main_path + animation)


class XP(Collectible):
  def __init__(self, pos, groups, amount, player):
    super().__init__(groups, player)
    self.sprite_type = 'collectible'

    self.frame_index = 0
    self.animation_speed = 0.15

    # graphics setup
    self.import_graphics('xp')
    self.status = 'idle'
    self.image = self.animations[self.status][self.frame_index]
    self.rect = self.image.get_rect(topleft = pos)

    # movemnet
    self.pos = pygame.math.Vector2(self.rect.center)
    self.speed = 0
    self.target_pos = self.pos

    # interaction setup
    self.amount = amount
    self.velocity = pygame.math.Vector2()

  def flicker(self):
    # Overwrite to disable flickering for XP
    pass

  def move(self, dt):
    distance, direction = get_distance_direction_a_to_b(self.pos, self.target_pos)

    if distance <= (direction * self.speed * dt * 60).magnitude():
      self.pos = self.target_pos

    else:
      self.pos += direction * self.speed * dt * 60

    self.rect.centerx = round(self.pos.x)
    self.rect.centery = round(self.pos.y)

  def update(self,dt,actions):
    self.animate(dt)
    self.move(dt)

  def collectible_update(self,dt,actions):
    self.fsm.execute(dt,actions)
    pass
