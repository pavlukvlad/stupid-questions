import pygame, sys

from scripts.utils import Animation, Tileset, load_image
from scripts.player import Player
from scripts.tilemap import Tilemap
from scripts.ui import SkillsUI

class Game():
    def __init__(self):
        pygame.init()
        
        self.font = pygame.font.SysFont('data/texts/BoutiqueBitmap9x9_1.9.ttf', 24)
        self.screen = pygame.display.set_mode((960, 540))
        
        self.display_width, self.display_height = 320, 180
        
        self.display = pygame.Surface((self.display_width, self.display_height))
        self.display_2 = pygame.Surface((self.display_width, self.display_height))
        
        self.physics_display = pygame.Surface((self.display_width, self.display_height))
        self.decorations_display = pygame.Surface((self.display_width, self.display_height))
        self.background_display = pygame.Surface((self.display_width, self.display_height))
        
        self.clock = pygame.time.Clock()
        
        self.movement = [False, False]
        
        self.animations = {
            ''
            'player/idle': Animation('data/assets/Animations/Player/idle/anim1.png', img_dur=30),
            'player/run': Animation('data/assets/Animations/Player/walk/anim1.png', img_dur=6),
            'player/jump': Animation('data/assets/Animations/Player/jump/anim1.png', img_dur=7, loop=False),
            'player/wall_slide': Animation('data/assets/Animations/Player/slide/anim1.png'),
            'player/fall': Animation('data/assets/Animations/Player/fall/anim1.png'),
            'player/land': Animation('data/assets/Animations/Player/land/anim1.png', img_dur=10, loop=False)
        }
        
        self.ui = {
            'switch': SkillsUI(50,50, load_image('data/assets/spells/form_1.png'), load_image('data/assets/spells/form_2.png'), 400, 475, 10, 'Q'),
            'spell_1': SkillsUI(50,50, load_image('data/assets/spells/paralysed.png'), load_image('data/assets/spells/time_stop.png'), 460, 475, 15, 'E'),
            'spell_2': SkillsUI(50,50, load_image('data/assets/spells/x2_speed.png'), load_image('data/assets/spells/x2_speed_2.png'), 520, 475, 15, 'F'),
        }
        
        self.test_tileset = Tileset("data/assets/map_tiles/test_map/tileset.png", 16).load_tileset()
        
        self.player = Player(self, (50, 50), (8, 15))
                
        self.tilemap = Tilemap(self, tile_size=16)
        
        self.level = 'test'
        self.load_level(self.level)
              
        pygame.display.set_caption('stupid-questions')
        
    def load_level(self, level_name):
        self.tilemap.load('data/levels/' + level_name + '.json')
        
        #self.leaf_spawners = []
        #for key, tree in self.tilemap['tilemap'].items():
        #    if ':' in key:
        #        self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
        
        self.player.pos = [14, 4]
        self.player.air_time = 0
            
        self.projectiles = []
        self.particles = []
        self.sparks = []
        
        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30
    
    def run(self):
        q_pressed = False
        e_pressed = False
        f_pressed = False
        
        while True:
            self.background_display.fill((198, 183, 190))
            self.physics_display.fill((0, 0, 0))
            self.decorations_display.fill((0, 0, 0))

            self.display_2.fill((0, 0, 0, 0))
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            mpos = pygame.mouse.get_pos()
            
            self.tilemap.render(
                self.background_display,
                self.physics_display,
                self.decorations_display,
                self.test_tileset,
                offset=render_scroll,
            )
            
            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.physics_display, offset=render_scroll)
            
            display_mask = pygame.mask.from_surface(self.display)
            display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.display_2.blit(display_sillhouette, offset)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        if self.player.jump():
                            pass
                    if event.key == pygame.K_q:
                        q_pressed = True
                        self.player.form = not self.player.form
                    if event.key == pygame.K_e:
                        e_pressed = True
                    if event.key == pygame.K_f:
                        f_pressed = True
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_q:
                       q_pressed = False
                    if event.key == pygame.K_e:
                        e_pressed = False
                    if event.key == pygame.K_f:
                        f_pressed = False
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                        
                        
            self.display.blit(self.background_display, (0,0))
            
            
            self.physics_display.set_colorkey((0, 0, 0))
            self.display.blit(self.physics_display, (0,0))

            self.decorations_display.set_colorkey((0, 0, 0))
            self.display.blit(self.decorations_display, (0,0))
            
            self.display_2.blit(self.display, (0, 0))

            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), (0,0))
            
            img = self.font.render(str(int(self.clock.get_fps())), True, (1, 1, 1))
            self.screen.blit(img, (930, 10))
            
            for name, obj in self.ui.items():
                obj.form = self.player.form
                
                if name == 'switch' and q_pressed:
                    obj.render(self.screen, 'pressed')
                elif name == 'spell_1' and e_pressed:
                    obj.render(self.screen, 'pressed')
                elif name == 'spell_2' and f_pressed:
                    obj.render(self.screen, 'pressed')
                else:
                    obj.render(self.screen, mpos)
            
            pygame.display.update()
            self.clock.tick(60)
    
Game().run()