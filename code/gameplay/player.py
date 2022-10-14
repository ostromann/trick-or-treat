import pygame
from gameplay.entity import Entity
from gameplay.support import import_folder
from settings import *


class Player(Entity):
    def __init__(self, player_name, pos, groups, obstacle_sprites):
        super().__init__(groups)

        # graphics setup
        self.import_player_assets()
        self.status ='right'
        self.image = self.animations[self.status][self.frame_index]
        
        # movement
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.obstacle_sprites = obstacle_sprites       

        # control
        self.attacking = False
        self.attack_cooldown = 200
        self.attack_time = None

        # stats
        self.stats = {
            'health': 100, 
            'energy': 60, 
            'attack': 10,
            'attack_factor': 1,
            'speed': 10,
            'range': 1,
            'projectile_speed': 1,
            }
        self.max_stats = {
            'health': 300, 
            'energy': 140, 
            'attack': 20,
            'attack_factor': 2, 
            'speed': 10,
            'range': 1,
            'projectile_speed': 1,
            }
        self.upgrade_costs = {
            'health': 100, 
            'energy': 100, 
            'attack': 100,
            'attack_factor': 100, 
            'speed': 100,
            'range': 100,
            'projectile_speed': 100,
            }
        self.health = self.stats['health']
        self.exp = 0
        self.speed = self.stats['speed']

        # damage timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_cooldown = 500

        # projectiles
        player_info = player_data[player_name]
        self.projectiles = []
        for projectile_name in player_info['projectiles']:
            self.projectiles.append(projectile_name)

    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {
            'left': [], 'right': [],
            'left_idle': [], 'right_idle': [],
            'left_attack': [], 'right_attack': [],
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self, actions):
        # Get the direction from inputs
        self.direction.x = actions['right'] - actions['left']
        self.direction.y = actions['down'] - actions['up']

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

    def get_status(self, actions):
        # change status
        self.status = 'right' if actions['right'] else self.status
        self.status = 'left' if actions['left'] else self.status

        # idle status
        if self.direction.magnitude() < 0.1:
            self.status = self.status.split('_')[0] + '_idle'
        else:
            self.status = self.status.split('_')[0]

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_cooldown:
                self.vulnerable = True



    def get_full_projectile_damage(self, projectile):
        base_damage = self.stats['attack']
        projectile_damage = projectile.damage * self.stats['attack_factor']
        # print(f"hit!  {base_damage + projectile_damage} base_dmg: {base_damage}, projectile_dmg: {projectile.damage} * {self.stats['attack_factor']}")
        return base_damage + projectile_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.spell]['strength']
        return base_damage + spell_damage

    def get_value_by_index(self,index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self,index):
        return list(self.upgrade_costs.values())[index]

    def collect(self, sprite):
        print(f'collected {sprite.amount} exp')
        self.exp += sprite.amount
        sprite.kill()

    def update(self, dt, actions):
        self.input(actions)
        self.move(dt, self.stats['speed'])
        self.cooldowns()
        self.get_status(actions)
        self.animate(dt)
        