import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, dt, speed):
        self.pos += self.direction * speed * dt * 60
        
        self.rect.centerx = round(self.pos.x)
        self.collision('horizontal')

        self.rect.centery = round(self.pos.y)
        self.collision('vertical')
        

    def collision(self, direction):
        if direction == 'horizontal':
                for sprite in self.obstacle_sprites:
                        if sprite.rect.colliderect(self.rect):
                                if self.direction.x > 0:    # moving right
                                        self.pos.x = sprite.rect.left - self.rect.width / 2
                                elif self.direction.x < 0:    # moving left
                                        self.pos.x = sprite.rect.right + self.rect.width / 2
                                self.rect.centerx = round(self.pos.x)

        if direction == 'vertical':
                for sprite in self.obstacle_sprites:
                        if sprite.rect.colliderect(self.rect):
                                if self.direction.y > 0:    # moving down
                                        self.pos.y = sprite.rect.top - self.rect.height / 2
                                elif self.direction.y < 0:    # moving up
                                        self.pos.y = sprite.rect.bottom + self.rect.height / 2
                                self.rect.centery = round(self.pos.y)

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0: 
                return 255
        else: 
                return 0

    def animate(self,dt):
        animation = self.animations[self.status]

        # loop over the frame_index
        self.frame_index += self.animation_speed * dt * 60
        self.frame_index %= len(animation)

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.rect.center)

        self.flicker()

    def flicker(self):
        # flickering after being hit
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)    
