import pygame


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # creating the floor
        self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def center_target_camera(self, target):
        # Camera following player
        self.offset.x = target.pos.x - self.half_w#target.rect.centerx - self.half_w
        self.offset.y = target.pos.y - self.half_h#target.rect.centery - self.half_h

    def custom_draw(self, player):
        self.center_target_camera(player)

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            # draw shadow
            self.draw_shadow(sprite)

            # draw sprite
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

            # draw outline rect for debugging
            # outline_rect = pygame.Rect(offset_pos[0],offset_pos[1],sprite.rect.width, sprite.rect.height)
            # pygame.draw.rect(self.display_surface,(255,0,0),outline_rect,2)

    def draw_shadow(self, sprite):
        pass
    #TODO:
        # offset_pos = sprite.rect.topleft - self.offset
        # shadow_rect = (offset_pos[0],offset_pos[1] + sprite.rect.height*0.95, sprite.rect.width, sprite.rect.height * 0.1)
        # pygame.draw.ellipse(self.display_surface,(60,60,60,128), shadow_rect)



    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') if sprite.sprite_type == 'enemy']
        for sprite in enemy_sprites:
            sprite.enemy_update(player)

    def projectile_update(self,dt,cumulative_dt,actions):
        projectile_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') if sprite.sprite_type == 'projectile']
        for sprite in projectile_sprites:
            sprite.projectile_update(dt, cumulative_dt, actions)

    def collectible_update(self,player,dt):
        collectible_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') if sprite.sprite_type == 'collectible']
        for sprite in collectible_sprites:
            sprite.collectible_update(player,dt)

