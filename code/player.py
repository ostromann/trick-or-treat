from asyncio import create_subprocess_shell
from tkinter.ttk import Style
import pygame
from entity import Entity
from support import import_folder
from settings import *


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites,create_attack,destroy_weapon, create_spell):
        super().__init__(groups)
        self.image = pygame.transform.scale(pygame.image.load(
            'assets/player_single.png').convert_alpha(), (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # graphics setup
        self.import_player_assets()
        self.status ='down'

        # control
        self.attacking = False
        self.attack_cooldown = 200
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

        # weapon
        self.create_attack = create_attack
        self.destroy_weapon = destroy_weapon
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.switching_weapon = False
        self.weapon_switch_time = None
        self.weapon_switch_cooldown = 400

        # spells
        self.create_spell = create_spell
        self.spell_index = 0
        self.spell = list(magic_data.keys())[self.spell_index]
        self.switching_spell = False
        self.spell_switch_time = None
        self.spell_switch_cooldown = 400

        # stats
        self.stats = {
            'health': 100, 
            'energy': 60, 
            'attack': 10, 
            'magic': 4, 
            'speed': 5,
            }
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']

        # damage timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_cooldown = 500

    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
            'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': [],
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if self.attacking:
            self.direction *= 0
        else:
            keys = pygame.key.get_pressed()

            # movement input
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status ='right'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status ='left'
            else:
                self.direction.x = 0
            
            # attack input
            if keys[pygame.K_SPACE] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            # magic input
            if keys[pygame.K_LCTRL] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.spell_index]
                strength = list(magic_data.values())[self.spell_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.spell_index]['cost']

                self.create_spell(style, strength, cost)

            # Switch weapon
            if keys[pygame.K_q] and not self.switching_weapon:
                self.switching_weapon = True
                self.weapon_switch_time = pygame.time.get_ticks()
                self.weapon_index = (self.weapon_index + 1) % len(weapon_data)
                self.weapon = list(weapon_data.keys())[self.weapon_index]

            # Switch spell
            if keys[pygame.K_e] and not self.switching_spell:
                self.switching_spell = True
                self.spell_switch_time = pygame.time.get_ticks()
                self.spell_index = (self.spell_index + 1) % len(magic_data)
                self.spell = list(magic_data.keys())[self.spell_index]

    def get_status(self):
        # idle status
        if self.direction.magnitude() < 0.1:
            self.status = self.status.split('_')[0] + '_idle'

        # attacking status
        if self.attacking:
            self.status = self.status.split('_')[0]  + '_attack'

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_weapon()
        
        if self.switching_weapon:
            if current_time - self.weapon_switch_time >= self.weapon_switch_cooldown:
                self.switching_weapon = False

        if self.switching_spell:
            if current_time - self.spell_switch_time >= self.spell_switch_cooldown:
                self.switching_spell = False

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_cooldown:
                self.vulnerable = True


    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame_index
        self.frame_index += self.animation_speed
        self.frame_index %= len(animation)

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.spell]['strength']
        return base_damage + spell_damage

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy =  self.stats['energy']

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.energy_recovery()
