from audioop import add
import pygame

from gameplay.support import *
from gameplay.entity import Entity
from gameplay.entity_fsm import EntityFSM, TimedState, State
from settings import *

# TODO: Later
# Not necessary right now!
# class SpawnState(TimedState):
#   def startup(self, sprite):
#     sprite.vulnerable = False

# class MoveState(State):
#   def startup(self, sprite):
#     sprite.speed = sprite.move_speed
  
#   def update(self, sprite, dt, actions):
#     sprite.target_pos = sprite.player.pos
#     self.check_done(sprite)

#   def check_done(self, sprite):
#     # check if enemy is within charging distance of player
#     distance, _ = get_distance_direction_a_to_b(sprite.pos, sprite.player.pos)

#     margin = sprite.stats['charge_radius']
#     if distance <= margin:
#       self.done = True

# class PrechargeState(TimedState):
#   def startup(self, sprite):
#     pass
#     # TODO:
#     # player precharging sound
  
#   def update(self, sprite, dt, actions):
#     sprite.target_pos = sprite.player.pos
#     self.check_expiry()


# class ChargeState(State):
#   def startup(self, sprite):
#     sprite.speed = sprite.charge_speed
#     sprite.target_pos = sprite.player.pos
  
#   def update(self, sprite, dt, actions):
#     # TODO: Add red outline to sprite

#     if not self.done:
#       self.check_done
#       sprite.target_pos = sprite.player.pos
  
#   def cleanup(self, sprite):
#     sprite.has_hit_sprite = False

class Enemy(Entity):
  def __init__(self,monster_name,pos,groups,obstacle_sprites, damage_player, trigger_death_particles, add_exp, trigger_exp_drop):
    
    #general setup
    super().__init__(groups,bouncy=True)
    self.sprite_type = 'enemy'

    # graphics setup
    self.import_graphics(monster_name)
    self.status = 'idle'
    self.image = self.animations[self.status][self.frame_index]

    # movement
    self.rect = self.image.get_rect(topleft = pos)
    self.pos = pygame.math.Vector2(self.rect.center)
    self.obstacle_sprites = obstacle_sprites
    self.hitbox = self.rect.inflate(-16,-16)
    self.hitbox.center = self.pos

    # stats
    self.monster_name = monster_name
    monster_info = monster_data[self.monster_name]
    self.stats = monster_info
    self.health = monster_info['health']
    self.exp = monster_info['exp']
    self.speed = monster_info['speed']
    self.attack_damage = monster_info['damage']
    self.resistance = monster_info['resistance']
    self.attack_radius = monster_info['attack_radius']
    self.notice_radius = monster_info['notice_radius'] * 10
    self.attack_type = monster_info['attack_type']

    # player interaction
    self.can_attack = True
    self.attack_time = None
    self.attack_cooldown = 400
    self.damage_player = damage_player
    self.trigger_death_particles = trigger_death_particles
    self.add_exp = add_exp
    self.trigger_exp_drop = trigger_exp_drop

    # invincibility timer
    self.vulnerable = True
    self.hit_time = None
    self.invincibility_cooldown = 300

    # sounds
    self.death_sound = pygame.mixer.Sound('audio/death.wav')
    self.hit_sound = pygame.mixer.Sound('audio/hit.wav')
    self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
    self.death_sound.set_volume(0)#0.3)
    self.hit_sound.set_volume(0)#0.3)
    self.attack_sound.set_volume(0)#0.3)

    # FSM setup
    # TODO: LAter
    # self.fsm = EntityFSM(self)
    # self.fsm.states['spawn'] = SpawnState('spawn',MONSTER_SPAWN_DURATION,next_state='move')
    # self.fsm.states['move'] = MoveState('move', next_state='precharge')
    # self.fsm.states['precharge'] = SpawnState('spawn',self.stats['precharge_duration'],next_state='precharge')
    # self.fsm.states['charge'] = ChargeState('charge', next_state='move')
    # self.fsm.current_state = self.fsm.states['spawn']


  def import_graphics(self,name):
    self.animations = {'idle': [], 'move': [], 'attack': []}
    main_path = f'graphics/monsters/{name}/'
    for animation in self.animations.keys():
      self.animations[animation] = import_folder(main_path + animation)

  def get_player_distance_direction(self, player):
    enemy_vector = pygame.math.Vector2(self.rect.center)
    player_vector = pygame.math.Vector2(player.rect.center)
    distance = (player_vector - enemy_vector).magnitude()

    if distance > 0:
      direction = (player_vector - enemy_vector).normalize()
    else:
      direction = pygame.math.Vector2()

    return (distance,direction)

  def get_status(self, player):
    distance = self.get_player_distance_direction(player)[0]

    if distance <= self.attack_radius and self.can_attack:
      if self.status != 'attack':
        self.frame_index = 0
      self.status = 'attack'
    elif distance <= self.notice_radius:
      self.status = 'move'
    else:
      self.status = 'idle'

  def actions(self, player):
    if self.status == 'attack':
      self.attack_sound.play()
      self.attack_time = pygame.time.get_ticks()
      self.damage_player(self.attack_damage,self.attack_type)
    elif self.status == 'move':
      self.direction = self.get_player_distance_direction(player)[1]
    else:
      self.direction = pygame.math.Vector2()

  def cooldowns(self):
    current_time = pygame.time.get_ticks()

    if not self.can_attack:
      if current_time - self.attack_time >= self.attack_cooldown:
          self.can_attack = True

    if not self.vulnerable:
      if current_time - self.hit_time >= self.invincibility_cooldown:
          self.vulnerable = True

  def get_damage(self, player, attack_sprite):
    if self.vulnerable:
      self.direction = self.get_player_distance_direction(player)[1]
      crit, damage = player.get_full_projectile_damage(attack_sprite)
      self.health -= damage
      # magic damage
      self.vulnerable = False
      self.hit_time = pygame.time.get_ticks()
      self.hit_sound.play()

      return (crit, damage)
    return (False, None)

  def check_death(self):
    if self.health <= 0:
      self.kill()
      self.trigger_death_particles(self.rect.center,self.monster_name)
      # self.add_exp(self.exp)
      self.death_sound.play()
      self.trigger_exp_drop(self.rect.center,self.exp)

  def hit_reaction(self):
    if not self.vulnerable:
      self.direction *= -self.resistance

  def update(self, dt, actions):
    self.hit_reaction()
    self.move(dt,self.speed)
    self.animate(dt)
    self.cooldowns()
    self.check_death()

  def enemy_update(self, player):
    self.get_status(player)
    self.actions(player)
