from random import randint
import sys
import pygame

WIDTH, HEIGHT = 1280, 960
FPS = 60


class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.transform.scale(pygame.image.load(
            'assets/tree.png').convert_alpha(), (64, 64))
        self.rect = self.image.get_rect(topleft=pos)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.transform.scale(pygame.image.load(
            'assets/player_single.png').convert_alpha(), (64, 64))
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 8

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # ground
        self.ground_surf = pygame.transform.scale(pygame.image.load(
            'assets/TilesetGraveyard_512x512_transparent.png').convert_alpha(), (2048, 2048))
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, player):
        # Camera following player
        self.center_target_camera(player)

        # Background colour
        self.display_surface.fill('#477861')

        # ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        # active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.bottom):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)


class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Trick or Treat!')
        self.clock = pygame.time.Clock()

        # setup
        self.camera_group = CameraGroup()
        self.player = Player((640, 360), self.camera_group)

        # Spawn random elements
        for i in range(20):
            random_x = randint(0, 2000)
            random_y = randint(0, 2000)
            Tree((random_x, random_y), self.camera_group)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.camera_group.update()
            self.camera_group.custom_draw(self.player)

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
