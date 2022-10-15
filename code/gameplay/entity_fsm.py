from random import randint
import time
import pygame

class EntityFSM:
  '''
  Finite state machine for entities
  '''
  def __init__(self,sprite, index):
    self.index = index # index of this state machine. for debugging only
    self.sprite = sprite # sprite this FSM belongs to
    self.states = {} # dict of states
    self.current_state = None # current state

  def execute(self,dt,actions):
    print(self.index, self.current_state.name)
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
  def __init__(self, name, next_state):
    self.name = name
    self.done = False
    self.next_state = next_state
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
  def __init__(self, name, next_state, duration):
    self.name = name
    self.done = False
    self.next_state = next_state
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
      



# class Char:
#   def __init__(self):

#     self.cooldown_time = 4
    
#     # FSM setup
#     self.fsm = EntityFSM(self)
#     self.fsm.states['cooldown'] = CooldownState('cooldown', 'ready', self.cooldown_time)
#     self.fsm.states['ready'] = ReadyState('ready', 'attack')
#     self.fsm.states['attack'] = AttackState('attack', 'return')
#     self.fsm.states['return'] = ReturnState('return','cooldown')

#   def update(self, dt, actions):
#     self.fsm.execute(dt,actions)

# ##===================================

# if __name__ == "__main__":
#   light = Char()

#   light.fsm.set_state('ready')
#   dt = 0
#   actions = None

#   for i in range(200):
#     time.sleep(0.5)
#     light.fsm.execute(dt,actions)