import pygame
from settings import *

class DamageIndicator:
	def __init__(self):
		pass

	def create_damage_indication(self, pos, groups, amount, crit, color = None):
		DamageNumberEffect(pos, groups, amount, crit, color)


class DamageNumberEffect(pygame.sprite.Sprite):
	def __init__(self,pos,groups, amount, crit, color = None):
		super().__init__(groups)
		self.sprite_type = 'ui'
		self.fade_out_speed = DAMAGE_INDICATOR_FADEOUT_TIME
		
		if crit:
			font_size = DAMAGE_INDICATOR_CRIT_FONT_SIZE
			font_color = DAMAGE_INDICATOR_CRIT_TEXT_COLOR
		else:
			font_size = DAMAGE_INDICATOR_FONT_SIZE
			font_color = DAMAGE_INDICATOR_TEXT_COLOR
		
		if color:
			font_color = color

		self.font = pygame.font.Font(DAMAGE_INDICATOR_FONT, font_size)
		self.text_surf = self.font.render(f'{int(amount)}', True, font_color)
		self.pos = pygame.math.Vector2(pos)
		x = round(self.pos.x)
		y = round(self.pos.y)
		self.rect = self.text_surf.get_rect(center = (x,y))
		self.image = self.text_surf

		self.lifetime = 0
		

	def animate(self,dt):
		self.lifetime += dt
		if self.lifetime > DAMAGE_INDICATOR_FADEOUT_TIME:
			self.kill()
		
		self.pos.y += -40 * dt		
		self.rect.centery = round(self.pos.y)
		self.image = self.text_surf.convert_alpha()
		self.image.set_alpha(255 - (self.lifetime/DAMAGE_INDICATOR_FADEOUT_TIME)**4 * 255)
	
	def update(self,dt,actions):
		self.animate(dt)
