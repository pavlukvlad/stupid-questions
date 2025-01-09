import pygame, sys

from scripts.utils import Animation, Tileset
from scripts.player import PhysicsEntity, Player
from scripts.tilemap import Tilemap

class Game():
    def __init__(self):
        pygame.init()
         
        self.screen = pygame.display.set_mode((960, 540))
        self.display = pygame.Surface((320, 240), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((320, 240))
        
        self.clock = pygame.time.Clock()
        
        self.movement = [False, False]
        
        self.animations = {
            'player/idle': Animation('data/assets/Animations/Player/idle/anim1.png', img_dur=6),
            'player/run': Animation('data/assets/Animations/Player/walk/anim1.png', img_dur=4),
            'player/jump': Animation('data/assets/Animations/Player/jump/anim1.png'),
            'player/slide': Animation('data/assets/Animations/Player/slide/anim1.png'),
            'player/fall': Animation('data/assets/Animations/Player/fall/anim1.png'),
            'player/land': Animation('data/assets/Animations/Player/land/anim1.png')
        }
        
        self.test_tileset = Tileset("data/assets/map_tiles/test_map/tileset.png", 16)
        self.test_tileset.load_tileset()
        
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
        
        
        self.player.pos = [0,0]
        self.player.air_time = 0
            
        self.projectiles = []
        self.particles = []
        self.sparks = []
        
        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30
    
    def run(self):
        while True:
            self.display.fill((0, 0, 0, 0))
            self.display_2.fill((0, 0, 0, 0))
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)
            
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
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
            
            self.display_2.blit(self.display, (0, 0))

            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)
    
Game().run()