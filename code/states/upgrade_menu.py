from tkinter.tix import TEXT
import pygame
from states.state import State
from settings import *

class UpgradeMenu(State):
  def __init__(self,game,player):
    State.__init__(self,game)
    # general setup
    self.display_surface = pygame.display.get_surface()
    self.player = player
    self.attribute_nr = len(self.player.stats)
    self.attribute_names = list(self.player.stats.keys())
    self.max_values = list(self.player.max_stats.values())
    self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

    # item creation
    self.height = self.display_surface.get_size()[1] * 0.8
    self.width = self.display_surface.get_size()[0] // 6
    self.create_items()

    # selection system
    self.selection_index = 0
    self.selection_time = None
    self.selection_time_cooldown = 200
    self.can_move = True

  def input(self):
    keys = pygame.key.get_pressed()

    if self.can_move:
      if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_nr - 1:
        self.selection_index += 1
        self.can_move = False
        self.selection_time = pygame.time.get_ticks()
        pass
      elif keys[pygame.K_LEFT] and self.selection_index >= 1:
        self.selection_index -= 1
        self.can_move = False
        self.selection_time = pygame.time.get_ticks()

      if keys[pygame.K_SPACE]:
        self.can_move = False
        self.selection_time = pygame.time.get_ticks()
        self.item_list[self.selection_index].trigger(self.player)

  def selection_cooldown(self):
    if not self.can_move:
      current_time = pygame.time.get_ticks()
      if current_time - self.selection_time >= self.selection_time_cooldown:
        self.can_move = True
    
  def create_items(self):
    self.item_list = []

    for i in range(self.attribute_nr):
      # horizontal position
      full_width = self.display_surface.get_size()[0]
      increment = full_width // self.attribute_nr
      left = (i * increment) + (increment - self.width) // 2
      # vertical position
      top = self.display_surface.get_size()[1] * 0.1

      # create the object
      item = Item(left,top,self.width, self.height, i,self.font)
      self.item_list.append(item)

  def update(self,delta_time, actions):
    pass

  def render(self):
    self.input()
    self.selection_cooldown()
    for index, item in enumerate(self.item_list):

      # get attributes
      name = self.attribute_names[index]
      value = self.player.get_value_by_index(index)
      max_value = self.max_values[index]
      cost = self.player.get_cost_by_index(index)
      
      item.display(self.display_surface,self.selection_index, name,value, max_value, cost)


class Item:
  def __init__(self, l,t,w,h,index,font):
    self.rect = pygame.Rect(l,t,w,h)
    self.index = index
    self.font = font

  def display_names(self, surface, name, cost, selected):
    # title
    
    title_surf = self.font.render(name, False, TEXT_COLOR_SELECTED if selected else TEXT_COLOR)
    title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))

    # cost
    cost_surf = self.font.render(f'{int(cost)} XP', False, TEXT_COLOR_SELECTED if selected else TEXT_COLOR)
    cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom + pygame.math.Vector2(0,-20))

    # draw
    surface.blit(title_surf, title_rect)
    surface.blit(cost_surf, cost_rect)

  def display_bar(self,surface, value, max_value, selected):
    # drawing setup
    top = self.rect.midtop + pygame.math.Vector2(0,60)
    bottom = self.rect.midbottom + pygame.math.Vector2(0,-60)
    color = BAR_COLOR_SELECTED if selected else BAR_COLOR

    # bar setup
    full_height = bottom[1] - top[1]
    relative_number = (value / max_value) * full_height
    value_rect = pygame.Rect(top[0] - 15,bottom[1] - relative_number,30,10)

    # draw elements
    pygame.draw.line(surface,color,top,bottom,8)
    pygame.draw.rect(surface,color,value_rect)

  def trigger(self, player):
    upgrade_attribute = list(player.stats.keys())[self.index]
    print(upgrade_attribute)

    if player.exp >= player.upgrade_costs[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
      player.exp -= player.upgrade_costs[upgrade_attribute]
      player.stats[upgrade_attribute] *= 1.2
      player.upgrade_costs[upgrade_attribute] *= 1.4

    if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
      player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]


  
  def display(self,surface, selection_num, name, value, max_value, cost):
    selected = selection_num == self.index
    bg_color = UPGRADE_BG_COLOR_SELECTED if selected else UI_BG_COLOR
      
    pygame.draw.rect(surface,bg_color,self.rect)
    pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
    self.display_names(surface, name, cost, selected)
    self.display_bar(surface,value,max_value,selected)
    
      
