
import pygame


import pygame


class SkillsUI():
    def __init__(self, width, height, img, img_2, x, y, kd):
        self.form = 1
        
        self.width = width
        self.height = height
        self.original_width = width
        self.original_height = height 
        
        self.img = img
        self.img_2 = img_2
        
        self.x = x
        self.y = y
        self.original_x = x
        self.original_y = y
        
        self.kd = kd
        self.pressed = False
        
        self.hover = False
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def action(self, description):
        pass
    
    def render(self, surf, mpos):

        if self.rect.collidepoint(mpos):
            self.hover = True
            self.width = int(self.original_width * 1.2)
            self.height = int(self.original_height * 1.2)
            self.x = self.original_x - (self.width - self.original_width) // 2
            self.y = self.original_y - (self.height - self.original_height) // 2 
            
        else:
            self.hover = False
            self.width = self.original_width
            self.height = self.original_height
            self.x = self.original_x
            self.y = self.original_y
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        scaled_img = pygame.transform.scale(self.img, (self.width, self.height))
        
        surf.blit(scaled_img, (self.x, self.y))
        
        if self.pressed:
            start_ticks = pygame.time.get_ticks()
            elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
            time_left = max(self.kd - elapsed_seconds, 0)
            
            if time_left <= 0:
                self.pressed = False