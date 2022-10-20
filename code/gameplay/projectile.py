import pygame
from math import sin, cos, pi

from settings import *
from gameplay.support import *
from gameplay.entity import Entity
from gameplay.entity_fsm import EntityFSM, State, TimedState

class CooldownState(TimedState): 
  def update(self,sprite,dt,actions):
    sprite.target_pos = sprite.get_queuing_pos()
    self.check_expiry()    

class ReadyState(State):
  def update(self,sprite,dt,actions):
    sprite.target_pos = sprite.get_queuing_pos()
    if len(sprite.attackable_sprites) > 0:
      self.check_done(sprite)

  def check_done(self,sprite):
    closest_enemy = get_closest_sprite_of_group(sprite, sprite.attackable_sprites)
    distance, _ = get_distance_direction_a_to_b(sprite.pos, closest_enemy.pos)

    if distance < sprite.range:
      self.done = True

class AttackState(State):
  def startup(self,sprite):
    sprite.has_hit_sprite = False
    sprite.speed = sprite.attack_speed
    if len(sprite.attackable_sprites) > 0:
      closest_enemy = get_closest_sprite_of_group(sprite, sprite.attackable_sprites)
      sprite.target_pos = closest_enemy.pos
    else:
      self.done = True

  def update(self,sprite,dt,actions):
    if not self.done:
      self.check_done(sprite)

  def cleanup(self, sprite):
    sprite.has_hit_sprite = False
    

  def check_done(self, sprite):
    self.done = sprite.has_hit_sprite or self.max_distance_reached(sprite) or self.target_position_reached(sprite)
    
  def max_distance_reached(self, sprite):
    distance, _ = get_distance_direction_a_to_b(sprite.pos, sprite.player.pos)
    margin = 50 # diamaeter of the players projectile queuing radius
    if distance >= sprite.range + margin:
      return True
    return False

  def target_position_reached(self, sprite):
    distance, _ = get_distance_direction_a_to_b(sprite.pos, sprite.target_pos)
    margin = 0.01
    if distance <= margin:
      return True
    return False


      
class ReturnState(State):
  def startup(self,sprite):
    sprite.speed = sprite.return_speed
    
  def update(self,sprite,dt,actions):
    #sprite.target_pos = sprite.get_queuing_pos()
    sprite.target_pos = sprite.player.pos
    self.check_done(sprite)
      
  def check_done(self, sprite):
    # check if projectile has reached player
    distance, _ = get_distance_direction_a_to_b(sprite.pos, sprite.player.pos)

    margin = sprite.player.stats['projectile_queuing_radius']
    if distance <= margin:
      self.done = True

##===================================

class Projectile(Entity):
  def __init__(self, projectile_name, groups, index, player, attackable_sprites):#, damage_enemy):# trigger_impact_particles)

    #general setup
    super().__init__(groups)
    self.sprite_type = 'projectile'
    self.index = index # index to keep track of position in queue
    self.attackable_sprites = attackable_sprites
    self.player = player # player this projectile belongs to

    # graphics setup
    self.import_graphics(projectile_name)
    self.status = 'ready'
    self.image = self.animations[self.status][self.frame_index]
    self.frame_index = 0
    self.animation_speed = 0.15

    # movement
    self.dt_cumulative = 0
    self.rect = self.image.get_rect(topleft = self.get_queuing_pos())
    self.pos = pygame.math.Vector2(self.rect.center)
    self.target_pos = self.pos

    # stats
    self.projectile_name = projectile_name
    projectile_info = projectile_data[self.projectile_name]
    self.attack_speed = projectile_info['speed']
    self.speed = self.attack_speed
    self.return_speed = projectile_info['return_speed']
    self.damage = projectile_info['damage']
    self.range = projectile_info['range']
    self.attack_type = projectile_info['attack_type']

    # FSM setup
    self.fsm = EntityFSM(self)
    self.fsm.states['cooldown'] = CooldownState('cooldown',projectile_info['cooldown'],next_state='ready')
    self.fsm.states['ready'] = ReadyState('ready', next_state='attack')
    self.fsm.states['attack'] = AttackState('attack', next_state='return')
    self.fsm.states['return'] = ReturnState('return',next_state='cooldown')
    self.fsm.current_state = self.fsm.states['ready']

    self.has_hit_sprite = False # integrate this into FSM somehow

    # # sounds
    # self.attack_sound = pygame.mixer.Sound(projectile_info['attack_sound'])

  def import_graphics(self,name):
    self.animations = {'ready': [], 'attack': [], 'return': [], 'recharge': []}
    main_path = f'graphics/projectiles/{name}/'
    for animation in self.animations.keys():
      self.animations[animation] = import_folder(main_path + animation)

  def flicker(self):
    # Overwrite to disable flickering for projectiles
    pass

  def hit_sprite(self,sprite):
    self.has_hit_sprite = True

  def get_queuing_pos(self):
    pos = pygame.math.Vector2()
    x_amplitude = self.player.stats['projectile_queuing_radius']
    y_amplitude = self.player.stats['projectile_queuing_radius'] / 2
    # TODO: angular_velocity = # degree / s
    phase_shift = self.index * 360 / len(self.player.projectiles) * pi/180    
    x = x_amplitude * sin((self.dt_cumulative * pi * 2 + phase_shift))
    y = y_amplitude * cos((self.dt_cumulative * pi * 2 + phase_shift))

    pos.x = self.player.pos.x + x
    pos.y = self.player.pos.y + y
    return pos 

  def move(self, dt):
    distance, direction = get_distance_direction_a_to_b(self.pos, self.target_pos)

    if distance <= (direction * self.speed * dt * 60).magnitude():
      self.pos = self.target_pos

    else:
      self.pos += direction * self.speed * dt * 60

    self.rect.centerx = round(self.pos.x)
    self.rect.centery = round(self.pos.y)

  def update(self, dt, actions):
    self.animate(dt)
    
  def projectile_update(self, dt, cumulative_dt, actions):
    self.dt_cumulative = cumulative_dt
    self.fsm.execute(dt,actions)
    self.move(dt)

