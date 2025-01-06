import pygame, sys

from scripts.utils import Animation, Images, load_image, load_images
from scripts.tilemap import Tilemap

class Level():
    def __init__(self):
        pass
    
    def load_level(self, map):
        self.tilemap.load('data/maps/' + str(map) + '.json')
        
        self.leaf_spawners = []
    
        self.projectiles = []
        self.particles = []
        self.sparks = []
        
        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30

class Game():
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((960, 540))
        self.display = pygame.Surface((320, 240), pygame.SRCALPHA)
        
        self.clock = pygame.time.Clock()
        
        self.test_tileset = Images("data/assets/map_tiles/test_map/tileset.png", 16)
        self.test_tileset.load_tileset()
        
        pygame.display.set_caption('stupid-questions')
    
    def run(self):
        while True:
            self.display.fill((0, 0, 0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            
            pygame.display.update()
            self.clock.tick(60)
    
Game().run()