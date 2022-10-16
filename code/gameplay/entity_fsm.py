from random import randint
import time
import pygame

class EntityFSM:
  '''
  Finite state machine for entities
  '''
  def __init__(self,sprite):
    self.sprite = sprite # sprite this FSM belongs to
    self.states = {} # dict of states
    self.current_state = None # current state

  def execute(self,dt,actions):
    if self.current_state.done:
      self.current_state.cleanup(self.sprite)
      self.current_state = self.states[self.current_state.next_state]
      self.current_state.done = False
      self.current_state.startup(self.sprite)
    self.current_state.update(self.sprite,dt,actions)

##===================================
class State():
  '''
  Base State class
  '''
  def __init__(self, name, next_state = None, previous_state = None):
    self.name = name
    self.done = False
    self.next_state = next_state
    self.previous_state = previous_state
    pass
    
  def startup(self,sprite):
    pass
    
  def cleanup(self,sprite):
    pass

  def update(self,sprite,dt,actions):
    pass

class TimedState(State):
  '''
  Base TimedState class
  Automatically switches to done after duration (in miliseconds) is expired.
  '''
  def __init__(self, name, duration, next_state = None, previous_state = None):
    super().__init__(name,next_state,previous_state)
    self.duration = duration
    pass
    
  def startup(self,sprite):
    self.start_time = pygame.time.get_ticks()
    
  def cleanup(self,sprite):
    pass

  def update(self,sprite,dt,actions):
    self.check_expiry()
    pass

  def check_expiry(self):
    current_time = pygame.time.get_ticks()
    if current_time - self.start_time >= self.duration:
      self.done = True
    self.time_remaining = self.duration - (current_time - self.start_time)