import imp
import pygame

from settings import *
from debug import *
from support import *
from tile import Tile
from player import Player
from camera import YSortCameraGroup
from random import choice


class Level:
    def __init__(self):

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):

        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'objects':import_csv_layout('map/map_Objects.csv'),
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
                            

        self.player = Player((1500, 2200), [self.visible_sprites], self.obstacle_sprites)


    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.direction)
