import pygame, os
from random import choice, randint

from settings import *
from states.state import State
from states.pause_menu import PauseMenu
from states.upgrade_menu import UpgradeMenu
from gameplay.camera import YSortCameraGroup
from gameplay.collectibles import XP
from gameplay.enemy import Enemy
from gameplay.entity import Entity
from gameplay.magic import MagicPlayer
from gameplay.particles import AnimationPlayer
from gameplay.player import Player
from gameplay.projectile import Projectile
from gameplay.support import *
from gameplay.tile import Tile
from gameplay.ui import UI

class Game_World(State):
    def __init__(self, game):
        State.__init__(self,game)

        self.cumulative_dt = 0

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.collectible_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()
        self.spawn_projectiles()

        # user interface
        self.ui = UI()
        # self.upgrade = UpgradeMenu(self.game,self.player)

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        # enemy spawn settings
        self.enemy_nr = 64
        self.enemy_spawn_interval = 5000
        self.enemy_spawn_waves = 5
        self.enemy_waves_spawned = 0
        self.enemy_spawn_time = pygame.time.get_ticks()
        self.can_spawn = True
        self.enemies = [] # list of all enemies

        # level settings
        self.level_start_time = pygame.time.get_ticks()
        self.level_duration = 30 * 1000

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'objects':import_csv_layout('map/map_Objects.csv'),
            'entities': import_csv_layout('map/map_Entities.csv')
        }

        graphics= {
            'grass': import_folder('graphics/Grass'),
            'objects': import_folder('graphics/objects'),
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == 'boundary':
                                Tile((x, y), [self.obstacle_sprites],'invisible')

                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    'normalo',
                                    (x, y), 
                                    [self.visible_sprites], 
                                    self.obstacle_sprites)

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player,attack_sprite)
                        attack_sprite.hit_sprite(target_sprite)

    def projectile_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos-offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)
    
    def player_collect_logic(self):
        if self.collectible_sprites:
            collision_sprites = pygame.sprite.spritecollide(self.player,self.collectible_sprites, False)
            if collision_sprites:
                for target_sprite in collision_sprites:
                    self.player.collect(target_sprite)

    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hit_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type,pos,[self.visible_sprites])
    
    def trigger_trace_particles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type,pos,[self.visible_sprites])

    def trigger_xp_drop(self,pos,amount):
        XP(pos, [self.visible_sprites, self.collectible_sprites], amount)

    def add_exp(self,amount):
        self.player.exp +=amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def spawn_projectiles(self):
        for index, projectile_name in enumerate(self.player.projectiles):
            Projectile(projectile_name,[self.visible_sprites, self.attack_sprites],index,self.player,self.attackable_sprites)       

    def spawn_enemies(self):
        self.enemy_spawn_cooldown()
        if self.can_spawn:
            for i in range(self.enemy_nr):
                monster_name = choice(['cauldron'])
                x = randint(25,35) * TILESIZE
                y = randint(15,25) * TILESIZE

                Enemy(
                    monster_name,
                    (x,y), 
                    [self.visible_sprites, self.attackable_sprites], 
                    self.obstacle_sprites, 
                    self.damage_player,
                    self.trigger_death_particles,
                    self.add_exp,
                    self.trigger_xp_drop)
            
            self.can_spawn = False
            self.enemy_spawn_time = pygame.time.get_ticks()

    def enemy_spawn_cooldown(self):
        current_time = pygame.time.get_ticks()

        if not self.can_spawn:
                if current_time - self.enemy_spawn_time >= self.enemy_spawn_interval:
                    self.can_spawn = True

    def timer(self):
        current_time = pygame.time.get_ticks()
        current_duration = current_time - self.level_start_time
        self.seconds_left = (self.level_duration - current_duration) / 1000

    def update(self,dt,actions):
        self.cumulative_dt += dt
        self.timer()
        # Check if the game was paused 
        if actions["start"]:
            new_state = UpgradeMenu(self.game, self.player)
            new_state.enter_state()
        if self.enemy_waves_spawned < self.enemy_spawn_waves:
            self.spawn_enemies()
            self.enemy_waves_spawned += 1
        self.visible_sprites.update(dt, actions)
        self.visible_sprites.enemy_update(self.player)
        self.visible_sprites.projectile_update(dt,self.cumulative_dt,actions)
        self.player_attack_logic()
        self.player_collect_logic()
      
    def render(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player, 0)
        