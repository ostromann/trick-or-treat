import pygame
from settings import *
from support import *
from math import sin, cos, pi

class Projectile(pygame.sprite.Sprite):
  def __init__(self, projectile_name, pos, groups, index, trigger_trace_particles):#, damage_enemy):# trigger_impact_particles)

    #general setup
    super().__init__(groups)
    self.sprite_type = 'projectile'

    self.frame_index = 0
    self.animation_speed = 0.15

    # graphics setup
    self.import_graphics(projectile_name)
    self.status = 'idle'
    self.image = self.animations[self.status][self.frame_index]

    # Particle setup
    self.trigger_trace_particles = trigger_trace_particles

    # movement
    self.rect = self.image.get_rect(topleft = pos)
    self.hitbox = self.rect.inflate(0,-10)

    # stats
    self.index = index # index to keep track of position in queue
    self.projectile_name = projectile_name
    projectile_info = projectile_data[self.projectile_name]
    self.speed = projectile_info['speed']
    self.return_speed = projectile_info['return_speed']
    self.damage = projectile_info['damage']
    self.range = projectile_info['range']
    self.attack_type = projectile_info['attack_type']

    # timing
    self.return_time = None
    self.return_cooldown = 300

    # enemy interaction
    self.can_attack = True
    self.attack_time = None
    self.attack_cooldown = 400
    self.target_enemy = None
    # self.damage_enemy = damage_enemy
    # self.trigger_impact_particles = trigger_impact_particles

    # sounds
    self.attack_sound = pygame.mixer.Sound(projectile_info['attack_sound'])

  def import_graphics(self,name):
    self.animations = {'idle': [], 'attack': [], 'return': []}
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


  def animate(self):
    animation = self.animations[self.status]

    # loop over the frame_index
    self.frame_index += self.animation_speed
    self.frame_index %= len(animation)

    # set the image
    self.image = animation[int(self.frame_index)]
    self.rect = self.image.get_rect(center = self.hitbox.center)
  
  def cooldowns(self):
    '''
    count down in cooldowns
    '''
    current_time = pygame.time.get_ticks()

    if not self.can_attack:
      if current_time - self.return_time >= self.return_cooldown:
        self.can_attack = True
  
  def queue_at_player(self,player):
    '''
    Projectile is queing at player (circling around it)
    '''
    x_amplitude = 50
    y_amplitude = 25
    phase_shift = self.index * 360 / len(player.projectiles) * pi/180    
    x = x_amplitude * sin((pygame.time.get_ticks()/500 + phase_shift))
    y = y_amplitude * cos((pygame.time.get_ticks()/500 + phase_shift))

    self.hitbox.x = player.rect.centerx + x - 12
    self.hitbox.y = player.rect.centery + y

    self.rect.center = self.hitbox.center

  def move_to_sprite(self, target_sprite, player, returning):
    '''
    Projectile moves towards target sprite.
    Boolean for return speed
    '''
    speed = self.return_speed if returning else self.speed
    direction = self.get_distance_direction_to_sprite(target_sprite)[1]
    if direction.magnitude() != 0:
        direction = direction.normalize()

    self.hitbox.x += direction.x * speed * player.stats['projectile_speed']
    self.hitbox.y += direction.y * speed * player.stats['projectile_speed']
    
    self.rect.center = self.hitbox.center
    # TODO: These particles are super slow. not good
    # self.trigger_trace_particles(self.rect.center,'trace')

  def hit_sprite(self,sprite):
    # TODO: potentially check if it is the right target enemy
    # for now, just any hit will suffice
    # if sprite == self.target_enemy:
    self.status = 'return'

  def get_status(self, player, enemies):

    # projectile is returning (first set on hit_sprite())
    if self.status == 'return':
      distance, _ = self.get_distance_direction_to_sprite(player)
      if distance <= 50:
        self.return_time = pygame.time.get_ticks()
        self.can_attack = False
        self.status = 'idle'
    
    # projectile is idle
    elif self.status == 'idle':

      # projectile is ready to attack (cooldown over)
      if self.can_attack and len(enemies) > 0:
        distance, _, closest_enemy = self.get_closest_sprite_from_list(enemies)

        # enemy is within distance
        if distance <= self.range * player.stats['range']:
          self.target_enemy = closest_enemy
          self.status = 'attack'

    # projectile is attacking and will do so until it hits something
    elif self.status == 'attack':
      self.status = 'attack'
    
  def actions(self, player):
    # This is necessary because target enemy might disappear before actions are called!
    if self.target_enemy:
      if len(self.target_enemy.groups()) < 2:
        self.target_enemy = None
        self.status = 'return'
    
    if self.status == 'attack':    
      # self.attack_sound.play()
      self.attack_time = pygame.time.get_ticks()
      self.move_to_sprite(self.target_enemy, player, False)

    elif self.status == 'idle':
      self.queue_at_player(player)
    elif self.status == 'return':
      self.move_to_sprite(player, player, True)

  def update(self):
    self.animate()
    self.cooldowns()


  def projectile_update(self, player, enemies):
    # TODO: Check why there is a delay at the beginning of the round
    self.get_status(player, enemies)
    self.actions(player)

