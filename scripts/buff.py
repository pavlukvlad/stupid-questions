
from scripts.ui import BuffUI

class Buff():
    def __init__(self, name, duration, effect, entity, image):
        
        self.name = name
        self.duration = duration
        self.effect = effect
        
        self.entity = entity
        
        self.ui = BuffUI(name, image, duration, 50, 50)

    def activate_effect(self):
        self.effect(self)

def X2SpeedEffect(self):
    if self.ui.end:
        self.entity.move_speed = 0.1
    else:
        self.entity.move_speed = 1

def X2GravityEffect(self):
    if self.ui.end:
        self.entity.slowdown = 1
    else:
        self.entity.slowdown = 0.1

def TimeStopEffect(self):
    print(self.name)

def StunEffect(self):
    print(self.name)
