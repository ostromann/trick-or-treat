import pygame
from math import sin, cos, pi

from settings import *
from gameplay.support import *
from gameplay.entity import Entity

class Projectile(Entity):
  def __init__(self, projectile_name, pos, groups, index, attackable_sprites):#, damage_enemy):# trigger_impact_particles)

    #general setup
    super().__init__(groups)
    self.sprite_type = 'projectile'
    self.attackable_sprites = attackable_sprites

    # graphics setup
    self.import_graphics(projectile_name)
    self.status = 'ready'
    self.image = self.animations[self.status][self.frame_index]
    self.frame_index = 0
    self.animation_speed = 0.15

    # movement
    self.rect = self.image.get_rect(topleft = pos)
    self.pos = pygame.math.Vector2(self.rect.center)
    self.target_pos = self.pos

    # stats
    self.index = index # index to keep track of position in queue
    self.projectile_name = projectile_name
    projectile_info = projectile_data[self.projectile_name]
    self.attack_speed = projectile_info['speed']
    self.speed = self.attack_speed
    self.return_speed = projectile_info['return_speed']
    self.damage = projectile_info['damage']
    self.range = projectile_info['range']
    self.attack_type = projectile_info['attack_type']

    # timing
    self.return_time = None
    self.return_cooldown = projectile_info['cooldown']

    # status booleans
    # TODO: Maybe good to put into a state machine?
    self.can_attack = True
    self.enemy_in_range = False
    self.attacking = False
    self.returning = False
    self.cooling_down = False

    self.target_enemy = None

    # sounds
    self.attack_sound = pygame.mixer.Sound(projectile_info['attack_sound'])

  def import_graphics(self,name):
    self.animations = {'ready': [], 'attack': [], 'return': [], 'recharge': []}
    main_path = f'graphics/projectiles/{name}/'
    for animation in self.animations.keys():
      self.animations[animation] = import_folder(main_path + animation)

  def get_distance_direction_to_sprite(self, sprite):
    '''
    Get distance and direction to another sprite
    '''
    own_vector = pygame.math.Vector2(self.rect.center)
    other_vector = pygame.math.Vector2(sprite.rect.center)
    distance = (other_vector - own_vector).magnitude()

    if distance > 0:
      direction = (other_vector - own_vector).normalize()
    else:
      direction = pygame.math.Vector2()
    return (distance,direction)

  def get_distance_to_pos(self, pos):
    '''
    Get distance to a 2D-position
    '''
    own_vector = pygame.math.Vector2(self.rect.center)
    other_vector = pygame.math.Vector2(pos)
    distance = (other_vector - own_vector).magnitude()

    return distance

  def get_distance_direction_to_pos(self, pos):
    '''
    Get distance and direction to a 2D-position
    '''
    own_vector = pygame.math.Vector2(self.rect.center)
    other_vector = pygame.math.Vector2(pos)
    distance = (other_vector - own_vector).magnitude()

    if distance > 0:
      direction = (other_vector - own_vector).normalize()
    else:
      direction = pygame.math.Vector2()
    return (distance,direction)


  def get_dist_pos_to_group(self, group):
    '''
    Return a sorted list of distance to all attackable sprites
    '''
    dist_pos = []
    for sprite in group:
      distance = self.get_distance_to_pos(sprite.rect.center)
      dist_pos.append((distance,sprite.rect.center))

    return sorted(dist_pos, 
       key=lambda x: x[0])

  def get_closest_sprite_from_list(self, sprite_list):
    '''
    Return distance, direction and sprite of the closest sprite in list of sprite
    '''
    min_distance = 100000
    distance = min_distance
    closest_sprite = None
    for sprite in sprite_list:
      distance, direction = self.get_distance_direction_to_sprite(sprite)
      if distance < min_distance:
        min_distance = distance
        closest_sprite = sprite

    return distance, direction, closest_sprite

  def flicker(self):
    # Overwrite to disable flickering for projectiles
    pass
  
  def cooldowns(self):
    current_time = pygame.time.get_ticks()
    if self.status == 'recharge':
      if current_time - self.return_time >= self.return_cooldown:
        self.status = 'ready'
  
  def get_queue_pos_at_player(self,player):
    '''
    Projectile is queing at player (circling around it)
    '''
    x_amplitude = 50
    y_amplitude = 25
    phase_shift = self.index * 360 / len(player.projectiles) * pi/180    
    x = x_amplitude * sin((pygame.time.get_ticks()/200 + phase_shift))
    y = y_amplitude * cos((pygame.time.get_ticks()/200 + phase_shift))

    self.pos.x = player.pos.x + x
    self.pos.y = player.pos.y + y

    return self.pos

  def get_status(self):
    if self.status == 'ready':
      closest_enemy_dist_pos = self.get_dist_pos_to_group(self.attackable_sprites)[0]
      distance = closest_enemy_dist_pos[0]

      if distance < self.range:
        self.target_pos = closest_enemy_dist_pos[1]
        self.status = 'attack'
        self.speed = self.attack_speed
    
    if self.status == 'attack':
      distance = self.get_distance_to_pos(self.target_pos)
      print(f'{self.index}: {distance}')
      if distance <= 200:
        self.status = 'return'
        self.speed = self.return_speed
    
    if self.status == 'return':
      distance = self.get_distance_to_pos(self.target_pos)
      if distance <= 0.1:
        self.status = 'recharge'
        self.speed = self.attack_speed
        self.return_time = pygame.time.get_ticks()
    
    print(f'{self.index}: {self.status}')
    
  def actions(self, player):
    if self.status == 'attack':
      pass
      # closest_enemy_dist_pos = self.get_dist_pos_to_group(self.attackable_sprites)[0]
      # self.target_pos = closest_enemy_dist_pos[1]
    
    if self.status == 'return' or self.status == 'recharge' or self.status == 'ready':
      self.target_pos = self.get_queue_pos_at_player(player)

  def move(self, dt, speed):
    distance, direction = self.get_distance_direction_to_pos(self.target_pos)

    if distance <= (direction * speed * dt * 60).magnitude():
      self.pos = self.target_pos

    else:
      self.pos += self.direction * speed * dt * 60
      self.rect.centerx = round(self.pos.x)
      self.rect.centery = round(self.pos.y)

  def update(self, dt, actions):
    self.animate(dt)
    self.cooldowns()
    
  def projectile_update(self, player, dt, actions):
    # TODO: Check why there is a delay at the beginning of the round
    self.get_status()
    self.actions(player)
    self.move(dt, self.speed)

