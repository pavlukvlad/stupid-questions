import sys
import pygame
from scripts.utils import Tileset
from scripts.tilemap import Tilemap

RENDER_SCALE = 3.0
MINIMAP_TILE_SIZE = 16
OFFSET_POS = 860, 40

offsets = {
    "left": (-1, 0),
    "right": (1, 0),
    "up": (0, -1),
    "down": (0, 1),
    "left_up": (-1, -1),
    "right_up": (1, -1),
    "left_down": (-1, 1),
    "right_down": (1, 1),
}

positions = {
    "left": [5, 21],
    "right": [37, 21],
    "up": [21, 5],
    "down": [21, 37],
    "left_up": [5, 5],
    "right_up": [37, 5],
    "left_down": [5, 37],
    "right_down": [37, 37],
}

class Editor:
    def __init__(self):
        pygame.init()

        self.font = pygame.font.SysFont('data/texts/BoutiqueBitmap9x9_1.9.ttf', 14)
        pygame.display.set_caption('editor')
        self.screen = pygame.display.set_mode((960, 540))

        self.display_width, self.display_height = 320, 180
        self.physics_display = pygame.Surface((self.display_width, self.display_height))
        self.decorations_display = pygame.Surface((self.display_width, self.display_height))
        self.background_display = pygame.Surface((self.display_width, self.display_height))

        self.clock = pygame.time.Clock()
        self.tileset = Tileset("data/assets/map_tiles/test_map/tileset.png", 16).load_tileset()
        self.tilemap = Tilemap(self, tile_size=16)

        self.movement = [False, False, False, False]
        self.scroll = [0, 0]
        self.clicking = False
        self.right_clicking = False

        self.tile_list = list(self.tileset)
        self.tile_group = 0
        self.type = ';'

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicking = True
                if event.button == 3:
                    self.right_clicking = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.clicking = False
                if event.button == 3:
                    self.right_clicking = False

            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

            if event.type == pygame.KEYUP:
                self.handle_keyup(event.key)

    def handle_keydown(self, key):
        if key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
            self.movement[[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN].index(key)] = True

        elif key == pygame.K_q:
            self.type = {':': '|', '|': ';', ';': ':'}[self.type]

        elif key == pygame.K_t:
            self.tilemap.save('map.json')

        elif key in (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s):
            step = {pygame.K_a: -1, pygame.K_d: 1, pygame.K_w: -22, pygame.K_s: 22}[key]
            self.tile_group = (self.tile_group + step) % len(self.tile_list)

    def handle_keyup(self, key):
        if key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
            self.movement[[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN].index(key)] = False

    def render_tile_preview(self, mpos):
        tile_pos = (
            int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size),
            int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size),
        )
        current_tile_img = self.tileset[self.tile_list[self.tile_group]].copy()

        if self.type == '|':
            current_tile_img.set_alpha(100)

        self.decorations_display.blit(
            current_tile_img, (
                tile_pos[0] * self.tilemap.tile_size - self.scroll[0],
                tile_pos[1] * self.tilemap.tile_size - self.scroll[1],
            ),
        )

        if self.clicking:
            self.tilemap.tilemap[f"{tile_pos[0]}{self.type}{tile_pos[1]}"] = {
                'tile_id': self.tile_list[self.tile_group],
                'pos': tile_pos,
            }

        if self.right_clicking:
            tile_loc = f"{tile_pos[0]}{self.type}{tile_pos[1]}"
            self.tilemap.tilemap.pop(tile_loc, None)

    def render_minimap(self):
        for key, (dx, dy) in offsets.items():
            index = (self.tile_group + dx + dy * 22) % len(self.tile_list)
            tile_img = pygame.transform.scale(
                self.tileset[self.tile_list[index]].copy(),
                (MINIMAP_TILE_SIZE, MINIMAP_TILE_SIZE),
            )
            tile_img.set_alpha(100)
            self.screen.blit(tile_img, (positions[key][0] + OFFSET_POS[0], positions[key][1] + OFFSET_POS[1]))

        current_tile_img = pygame.transform.scale(
            self.tileset[self.tile_list[self.tile_group]].copy(),
            (MINIMAP_TILE_SIZE, MINIMAP_TILE_SIZE),
        )
        self.screen.blit(current_tile_img, (881, 61))

    def run(self):
        while True:
            self.background_display.fill((0, 0, 0))
            self.physics_display.fill((0, 0, 0))
            self.decorations_display.fill((0, 0, 0))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            self.tilemap.render(
                self.background_display,
                self.decorations_display,
                self.tileset,
                offset=render_scroll,
            )

            self.handle_events()

            mpos = (
                pygame.mouse.get_pos()[0] / RENDER_SCALE,
                pygame.mouse.get_pos()[1] / RENDER_SCALE,
            )
            self.render_tile_preview(mpos)

            self.screen.blit(
                pygame.transform.scale(self.background_display, self.screen.get_size()), (0, 0)
            )

            self.screen.blit(
                pygame.transform.scale(self.background_display, self.screen.get_size()), (0, 0)
            )

            self.decorations_display.set_colorkey((0, 0, 0))
            self.screen.blit(
                pygame.transform.scale(self.decorations_display, self.screen.get_size()), (0, 0)
            )

            img = self.font.render({';': 'PHYSICS_TILES', ':': 'DECORATION_TILES', '|': 'BACKGROUND_TILES'}[self.type], True, (255, 255, 255))
            self.screen.blit(img, (850, 15))

            self.render_minimap()
            pygame.display.update()
            self.clock.tick(60)

Editor().run()