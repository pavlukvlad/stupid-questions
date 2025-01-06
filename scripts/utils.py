import os

import pygame

BASE_IMG_PATH = 'C:/Users/shize/Downloads/ninja_game/data/images/'


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img
    
def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(pygame.image.load(BASE_IMG_PATH + path + "/" + img_name).convert())
    return images


class Images():
    def __init__(self, tileset, tile_size):
        self.tileset = tileset
        self.tile_size = tile_size
        self.tileset_image = pygame.image.load(self.tileset).convert()
        self.tileset_image.set_colorkey((0, 0, 0))
        
    def load_tileset(self):

        tileset_width, tileset_height = self.tileset_image.get_size()
    
        tiles = {}
        tile_count = '-1'
        for y in range(0, tileset_height, self.tile_size):
            for x in range(0, tileset_width, self.tile_size):
                tile_count = f'{int(tile_count)+1}'
                
                tile = self.tileset_image.subsurface(pygame.Rect(x, y, self.tile_size, self.tile_size))
                tiles[tile_count] = tile
                

        return tiles
    

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
    
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)]