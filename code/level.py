import imp
import pygame


from settings import *
from debug import *
from support import *
from tile import Tile
from player import Player
from enemy import Enemy
from camera import YSortCameraGroup
from random import choice
from weapon import Weapon
from ui import UI


class Level:
    def __init__(self):

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

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

                        if style == 'grass':
                            random_grass_image = choice(graphics[style])
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites],style, random_grass_image)

                        if style == 'objects':
                            surf = graphics[style][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites],style, surf)

                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x, y), 
                                    [self.visible_sprites], 
                                    self.obstacle_sprites, 
                                    self.create_attack, self.destroy_weapon,
                                    self.create_spell)
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                
                                Enemy(monster_name,(x,y), [self.visible_sprites], self.obstacle_sprites)


                        
                            
        

    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites])

    def destroy_weapon(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_spell(self, style, strength,cost):
        print(style, strength, cost)

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.ui.display(self.player)
