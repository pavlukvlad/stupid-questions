import pygame

class SkillsUI():
    def __init__(self, width, height, img, img_2, x, y, kd, key):
        self.form = 1
        
        self.width = width
        self.height = height
        self.original_width = width
        self.original_height = height 
        
        self.img = img
        self.img_2 = img_2
        
        self.form = True
        
        self.x = x
        self.y = y
        self.original_x = x
        self.original_y = y
        
        self.kd = kd
        self.pressed = False
        
        self.hover = False
        
        self.key = key
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Load the font
        self.font = pygame.font.Font("data/texts/BoutiqueBitmap9x9_1.9.ttf", 12)  # Adjust size if needed

    def action(self, description, width, height):
        pass
    
    def render(self, surf, mpos):

        if mpos == 'pressed' or self.rect.collidepoint(mpos):
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
        

        if self.form:
            scaled_img = pygame.transform.scale(self.img, (self.width, self.height))
        else:
            scaled_img = pygame.transform.scale(self.img_2, (self.width, self.height))
        surf.blit(scaled_img, (self.x, self.y))

        font = pygame.font.Font('data/texts/LuckiestGuy-Regular.ttf', 13)

        key_text = font.render(self.key, True, (0, 0, 0)) 
        key_width, key_height = key_text.get_size()
        square_size = max(key_width, key_height) + 4 

        square_x = self.x - 1
        square_y = self.y - 1
        pygame.draw.rect(surf, (255, 255, 255), (square_x-1, square_y-1, square_size, square_size))
        pygame.draw.rect(surf, (0, 0, 0), (square_x-1, square_y-1, square_size, square_size), 2)

        text_x = square_x + (square_size - key_width) // 2
        text_y = square_y + (square_size - key_height) // 2
        surf.blit(key_text, (text_x, text_y))
        
        if self.pressed:
            start_ticks = pygame.time.get_ticks()
            elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
            time_left = max(self.kd - elapsed_seconds, 0)
            
            if time_left <= 0:
                self.pressed = False