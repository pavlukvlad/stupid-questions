import pygame

class UI():
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
    
        self.x = x
        self.y = y
        
        self.original_width = width
        self.original_height = height
        
        self.original_x = x
        self.original_y = y
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class SkillsUI(UI):
    def __init__(self, width, height, img, img_2, x, y, kd, key):
        super().__init__(width, height, x, y)
        
        self.img = img
        self.img_2 = img_2
        self.form = True
        self.kd = kd
        self.hover = False
        self.key = key
        
        self.kd_time = 0
        self.hover_end_time = 0 
        self.active = True

        self.font = pygame.font.Font("data/texts/LuckiestGuy-Regular.ttf", 12)

    def render(self, surf, mpos):
        current_time = pygame.time.get_ticks()
        
        if mpos == 'pressed' or self.rect.collidepoint(mpos):
            self.hover = True
            self.hover_end_time = current_time + 40
        elif current_time < self.hover_end_time:
            self.hover = True
        else:
            self.hover = False

        if self.hover:
            self.width = int(self.original_width * 1.2)
            self.height = int(self.original_height * 1.2)
            self.x = self.original_x - (self.width - self.original_width) // 2
            self.y = self.original_y - (self.height - self.original_height) // 2
        else:
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

        key_text = self.font.render(self.key, True, (0, 0, 0))
        key_width, key_height = key_text.get_size()
        square_size = max(key_width, key_height) + 4

        square_x = self.x - 1
        square_y = self.y - 1

        text_x = square_x + (square_size - key_width) // 2
        text_y = square_y + (square_size - key_height) // 2
        
        
        if not self.active and self.kd_time != 0:
            elapsed_seconds = (pygame.time.get_ticks() - self.kd_time) // 1000
            time_left = max(self.kd - elapsed_seconds, 0)

            if time_left <= 0:
                self.active = True
                self.kd_time = 0

        if self.kd_time == 0 and not self.active:
            self.kd_time = pygame.time.get_ticks()

        if not self.active:
            elapsed_time = pygame.time.get_ticks() - self.kd_time
            cooldown_progress = elapsed_time / (self.kd * 1000)

            if cooldown_progress < 1:
                
                overlay_height = int(self.height * cooldown_progress)+4
                overlay_surface = pygame.Surface((scaled_img.get_width(), self.height), pygame.SRCALPHA)
                overlay_surface.fill((0, 0, 0, 128))

                final_overlay = pygame.Surface((scaled_img.get_width(), scaled_img.get_height()+4 - overlay_height), pygame.SRCALPHA)
                final_overlay.blit(overlay_surface, (0, 0), (0, overlay_height, scaled_img.get_width(), scaled_img.get_height() - overlay_height))

                final_overlay = pygame.transform.scale(final_overlay, (final_overlay.get_width() - 6, final_overlay.get_height()))
                surf.blit(final_overlay, (self.x + 4, self.y + 4))
        
        pygame.draw.rect(surf, (255, 255, 255), (square_x - 1, square_y - 1, square_size, square_size))
        pygame.draw.rect(surf, (0, 0, 0), (square_x - 1, square_y - 1, square_size, square_size), 2)

        
        surf.blit(key_text, (text_x, text_y))

class BuffUI(UI):
    def __init__(self, width, height, img, x, y, duration):
        super().__init__(width, height, x, y)
        
        self.img = img
        self.duration = duration
        self.start_time = pygame.time.get_ticks()

    def render(self, surf):
        scaled_img = pygame.transform.scale(self.img, (self.width, self.height))
        surf.blit(scaled_img, (self.x, self.y))

        elapsed_seconds = (pygame.time.get_ticks() - self.start_time) // 1000
        time_left = max(self.duration - elapsed_seconds, 0)

        font = pygame.font.Font('data/texts/LuckiestGuy-Regular.ttf', 12)
        time_text = font.render(f'{time_left}s', True, (255, 255, 255))
        surf.blit(time_text, (self.x + self.width + 5, self.y))

        if time_left <= 0:
            pass