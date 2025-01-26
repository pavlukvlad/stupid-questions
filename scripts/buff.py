
class Buff():
    def __init__(self, name, kd, effect, entity):
        
        self.name = name
        self.kd = kd
        self.effect = effect
        
        self.entity = entity

    def activate_effect(self):
        self.effect(self)

def X2SpeedEffect(self):
    print(self.name)

def X2SlowEffect(self):
    print(self.name)
    
def TimeStopEffect(self):
    print(self.name)

def StunEffect(self):
    print(self.name)
