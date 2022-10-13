import pygame
from settings import *

class UI:
  def __init__(self):
    
    # general
    self.display_surface = pygame.display.get_surface()
    self.display_w, self.display_h = self.display_surface.get_size()
    self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

    # bar setup
    self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
    self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)
    self.exp_bar_rect = pygame.Rect(0,self.display_h - 20, self.display_w, 20)
    self.bar_overlay = pygame.image.load('graphics/misc/bar_alpha.png').convert_alpha()

    # convert weapon dictionary
    self.weapon_graphics = []
    for weapon in weapon_data.values():
      path = weapon['graphic']
      weapon = pygame.image.load(path).convert_alpha()
      self.weapon_graphics.append(weapon)

    # convert spell dictionary
    self.spell_graphics = []
    for spell in magic_data.values():
      path = spell['graphic']
      spell = pygame.image.load(path).convert_alpha()
      self.spell_graphics.append(spell)



  def show_bar(self, current, maximum, bg_rect, color):
    #draw bg
    pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

    # converting stat to pixel
    ratio = current / maximum
    current_width = bg_rect.width * ratio
    current_rect = bg_rect.copy()
    current_rect.width = current_width

    pygame.draw.rect(self.display_surface, color, current_rect)

    self.display_surface.blit(pygame.transform.scale(self.bar_overlay,bg_rect.size),bg_rect)

    # pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

  def show_exp(self, exp):
    text_surf = self.font.render(f'{int(exp)} XP', False, TEXT_COLOR)
    x = self.display_surface.get_size()[0] - 20
    y = self.display_surface.get_size()[1] - 20
    text_rect = text_surf.get_rect(bottomright = (x,y))

    pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
    self.display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,20),3)

  def selection_box(self,left,top, has_switched):
    bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
    pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
    if has_switched:
      pygame.draw.rect(self.display_surface,UI_BORDER_COLOR_ACTIVE,bg_rect, 3)
    else:
      pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect, 3)

    return bg_rect

  def weapon_overlay(self,weapon_index, has_switched):
    bg_rect = self.selection_box(10,630, has_switched)
    weapon_surf = self.weapon_graphics[weapon_index]
    weapon_rect = weapon_surf.get_rect(center = bg_rect.center)
    
    self.display_surface.blit(weapon_surf, weapon_rect)

  def spell_overlay(self,spell_index, has_switched):
    bg_rect = self.selection_box(80,635, has_switched)
    spell_surf = self.spell_graphics[spell_index]
    spell_rect = spell_surf.get_rect(center = bg_rect.center)
    
    self.display_surface.blit(spell_surf, spell_rect)

  def timer(self,seconds):     
    text_surf = self.font.render(f'{int(seconds)}', False, TEXT_COLOR)
    x = self.display_surface.get_size()[0] // 2
    y = 20
    text_rect = text_surf.get_rect(midtop = (x,y))

    pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
    self.display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,20),4)


  def display(self, player, seconds_left):
    self.show_bar(player.health, player.stats['health'], self.health_bar_rect,HEALTH_COLOR)
    # self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect,ENERGY_COLOR)
    self.show_bar(player.exp, 20, self.exp_bar_rect,EXP_COLOR)

    # self.show_exp(player.exp)
    self.timer(seconds_left)

    # self.weapon_overlay(player.weapon_index, player.switching_weapon)
    # self.spell_overlay(player.spell_index, player.switching_spell)
    # self.selection_box(80,635) # magic
    

  