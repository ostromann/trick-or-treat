import pygame
from random import random
from gameplay.entity import Entity
from gameplay.support import import_folder
from settings import *


class Player(Entity):
    def __init__(self, player_name, pos, groups, obstacle_sprites):
        super().__init__(groups, bouncy=True)

        # graphics setup
        self.import_player_assets()
        self.status ='right'
        self.image = self.animations[self.status][self.frame_index]
        
        # movement
        self.rect = self.image.get_rect(topleft=pos) # topleft because this pos comes from the 64 64 gridworld in tiled
        self.pos = pygame.math.Vector2(self.rect.center)
        self.hitbox = self.rect.inflate(-16,-16)
        self.hitbox.center = self.pos
        self.obstacle_sprites = obstacle_sprites    

        # control
        self.attacking = False
        self.attack_cooldown = 200
        self.attack_time = None

        # stats
        self.level = 1
        self.level_ups = 0
        self.previous_exp_threshold = 0
        self.next_exp_threshold = BASE_EXP_THRESHOLD
        self.stats = player_data[player_name]
       
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
        crit = False
        base_damage = self.stats['attack']
        projectile_damage = projectile.damage * self.stats['attack_factor']
        damage = base_damage + projectile_damage
        if random() < self.stats['crit_chance']:
            crit = True
            damage = damage * self.stats['crit_damage']
        return crit, damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.spell]['strength']
        return base_damage + spell_damage

    def get_value_by_index(self,index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self,index):
        return list(self.upgrade_costs.values())[index]

    def check_level_up(self):
        # Linear progression curve
        if self.exp >= self.next_exp_threshold:
            self.previous_exp_threshold = self.next_exp_threshold
            self.next_exp_threshold = self.previous_exp_threshold + self.level * BASE_EXP_INCREASE
            self.level += 1
            self.level_ups += 1

    def update(self, dt, actions):
        self.input(actions)
        self.move(dt, self.stats['speed'])
        self.cooldowns()
        self.get_status(actions)
        self.animate(dt)
        self.check_level_up()

    

        
