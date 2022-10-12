import imp
import pygame


from settings import *
from debug import *
from support import *
from tile import Tile
from player import Player
from enemy import Enemy
from camera import YSortCameraGroup
from random import choice, randint
from weapon import Weapon
from particles import AnimationPlayer
from magic import MagicPlayer
from ui import UI
from upgrade import Upgrade
from projectile import Projectile
from collectibles import XP


class Level:
    def __init__(self):
        self.game_paused = False

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
        self.upgrade = Upgrade(self.player)

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        # enemy spawn settings
        self.enemy_nr = 1
        self.enemy_spawn_interval = 5000
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

                        # if style == 'grass':
                        #     random_grass_image = choice(graphics[style])
                        #     Tile(
                        #         (x,y), 
                        #         [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                        #         style, 
                        #         random_grass_image)

                        # if style == 'objects':
                        #     surf = graphics[style][int(col)]
                        #     Tile((x,y), [self.visible_sprites, self.obstacle_sprites],style, surf)

                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    'normalo',
                                    (x, y), 
                                    [self.visible_sprites], 
                                    self.obstacle_sprites, 
                                    self.create_attack, 
                                    self.destroy_weapon,
                                    self.create_magic)


    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites, self.attack_sprites])

    def destroy_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic(self, style, strength,cost):
        if style == 'heal':
            self.magic_player.heal(self.player,strength, cost, [self.visible_sprites])
        if style == 'flame':
            self.magic_player.flame(self.player,cost,[self.visible_sprites,self.attack_sprites])

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        # if target_sprite.sprite_type == 'grass':
                        #     pos = target_sprite.rect.center
                        #     offset = pygame.math.Vector2(0,75)
                        #     for leaf in range(randint(3,6)):
                        #         self.animation_player.create_grass_particles(pos-offset, [self.visible_sprites])
                        #     target_sprite.kill()
                        # else:
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
                    print(f'collected {target_sprite}')
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
        for i, projectile_name in enumerate(self.player.projectiles):
            Projectile(projectile_name,(0,0),[self.visible_sprites, self.attack_sprites],i,self.trigger_trace_particles)       

    def spawn_enemies(self):
        self.enemy_spawn_cooldown()
        if self.can_spawn:
            # print('spawn enemies!')
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
        # if current_duration >= self.level_duration:
        #     self.le
        
    def run(self):
        self.timer()
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player, self.seconds_left)

        if self.game_paused:
            self.upgrade.display()
        else:
            self.spawn_enemies()
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.visible_sprites.projectile_update(self.player)
            self.player_attack_logic()
            self.player_collect_logic()
        
        debug(self.player.projectiles)
