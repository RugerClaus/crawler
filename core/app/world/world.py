import pygame
from core.app.world.tiles import Tile
from core.app.world.level_structures.level_1_structure import *
from core.app.entities.character.enemy import Enemy #for testing will handle this elsewhere once I'm sure the enemy class works.

class World:
    def __init__(self, screen, grid_width, grid_height, tile_size, starting_level):
        self.screen = screen
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.tile_size = tile_size
        self.level = starting_level
        self.tiles = {}  # Static map: {(x, y): {"ground": obj, "object": obj}}
        self.entities = []  # Dynamic objects: [Coin(), Player(), Enemy()]
        self.buildings = []
        self.damaging_tiles = []
        self.gold_coin_animation = None
        self.enemies = []

        self.load_assets()  # <-- New method
        self.load_terrain_tiles()
        self.load_object_tiles()
        self.load_foreground_tiles()

        self.coin_positions = {
            "coin_0": (52,52,"gold"),
            "coin_1": (55,52,"silver"),
            "coin_2": (57,52,"bronze"),
            "coin_3": (59,52,"bronze")
        }
        self.health_potion_positions = {
            "health_potion_0": (82,52,"small"),
            "health_potion_1": (85,52,"small"),
            "health_potion_2": (88,52,"small"),
            "health_potion_3": (91,52,"small")
        }

    def reset(self, starting_level=1):
        self.level = starting_level
        self.tiles.clear()
        self.entities.clear()
        self.buildings.clear()
        self.damaging_tiles.clear()
        self.gold_coin_animation = None

        self.coin_positions = {
            "coin_0": (52, 52, "gold"),
            "coin_1": (55, 52, "silver"),
            "coin_2": (57, 52, "bronze"),
            "coin_3": (59, 52, "bronze")
        }
        self.health_potion_positions = {
            "health_potion_0": (82, 52, "small"),
            "health_potion_1": (85, 52, "small"),
            "health_potion_2": (88, 52, "small"),
            "health_potion_3": (91, 52, "small")
        }

    def load_assets(self):
        self.coin_frames = {
            "gold": [
                pygame.image.load(f"assets/graphics/game/currency/gold_coin_{i}.png").convert_alpha()
                for i in range(1, 4)
            ],
            "silver": [
                pygame.image.load(f"assets/graphics/game/currency/silver_coin_{i}.png").convert_alpha()
                for i in range(1, 4)
            ],
            "bronze": [
                pygame.image.load(f"assets/graphics/game/currency/bronze_coin_{i}.png").convert_alpha()
                for i in range(1, 4)
            ]
        }
        self.potion_frames = {
            "health_potion": pygame.image.load("assets/graphics/game/items/potion/health_potion.png")
        }

    def load_foreground_tiles(self):
        self.foreground_tiles = {
            "building_roof": Tile("assets/graphics/game/foreground/building_roof.png")
        }

    def load_terrain_tiles(self):
        """Define different terrain tiles."""
        self.terrain_tiles = {
            "dirt": Tile("assets/graphics/game/ground/shittydirt.png"),
            "grass": Tile("assets/graphics/game/ground/grass.png"),
            "missing_texture": Tile("assets/graphics/game/undefined.png"),
            "floor": Tile("assets/graphics/game/ground/floor.png"),
            # "water": Tile("assets/graphics/game/ground/water.png", is_walkable=False),
            "stone": Tile("assets/graphics/game/ground/stone.png")
        }
    def load_object_tiles(self):
        self.object_tiles = {
            "wall": Tile("assets/graphics/game/walls/shittywall.png",is_walkable=False),
            "wall2": Tile("assets/graphics/game/walls/wall2.png", is_walkable=False),
            "missing_texture": Tile("assets/graphics/game/undefined.png")
        }

    def place_static(self, x, y, obj, layer):
        valid_layers = ["ground", "object", "foreground"]
        if layer not in valid_layers:
            raise ValueError(f"Invalid layer '{layer}'. Allowed layers: {valid_layers}")

        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            if (x, y) not in self.tiles:
                self.tiles[(x, y)] = {key: None for key in valid_layers}
            self.tiles[(x, y)][layer] = obj

    def generate_map(self,player):

        if self.level == 1:
            default_tiles = draw_default_tiles(self.grid_height,self.grid_width,self.terrain_tiles)
            for (position, sprite) in default_tiles:
                x, y = position
                self.place_static(x, y, sprite, layer="ground")
            house_tiles = draw_house_tiles(self.terrain_tiles)
            for (position, sprite) in house_tiles:
                x, y = position
                self.place_static(x, y, sprite, layer="ground")
            building_wall_tiles = draw_building_walls(self.object_tiles)
            for (position, sprite) in building_wall_tiles:
                x, y = position
                self.place_static(x, y, sprite, layer="object")
            level_border_tiles = draw_level_border(self.object_tiles)
            for (position, sprite) in level_border_tiles:
                x, y = position
                self.place_static(x, y, sprite, layer="object")
            draw_spike_tiles(self)
            draw_coin_tiles(self,self.coin_frames,player,self.coin_positions)
            draw_health_potion_tiles(self,self.potion_frames,player,self.health_potion_positions)
        else:
            print("level not found")
            


    def is_blocked(self, x, y,sound=None):
        cell = self.tiles.get((x, y))
        if not cell:
            return False
        if cell["object"]:
            
            if sound is not None:
                sound("bump_wall")
            return True
        if cell["ground"] is None:
            print(f"No ground at {x}, {y}")
            return True
        return False

    def update(self):
        for entity in self.entities:
            entity.update()
        for enemy in self.enemies:
            enemy.update()

    def draw(self, camera, debug=False):
       
        for (x, y), layers in self.tiles.items():
            for layer_name in ["ground", "object"]:
                obj = layers.get(layer_name)
                if obj:
                    obj.rect.topleft = (x * self.tile_size, y * self.tile_size)
                    obj.rect = camera.apply(obj.rect)
                    self.screen.blit(obj.image, obj.rect)

        # Draw all dynamic entities (player, coins, etc.)
        for entity in self.entities:
            entity.draw(camera)


    def draw_foreground(self, camera, debug=False):

        for (x, y), layers in self.tiles.items():
            obj = layers.get("foreground")
            if obj:
                obj.rect.topleft = (x * self.tile_size, y * self.tile_size)
                obj.rect = camera.apply(obj.rect)
                
                if debug:

                    debug_image = self.tint_surface(obj.image, (255, 0, 0))
                    self.screen.blit(debug_image, obj.rect)
                else:
                    self.screen.blit(obj.image, obj.rect)

    def tint_surface(self, surface, tint_color):
        tinted = surface.copy()
        tinted.fill(tint_color + (0,), special_flags=pygame.BLEND_RGBA_ADD)
        return tinted
    
    def generate_enemy(self):
        enemy = Enemy(self.screen,self,grid_x=58,grid_y=58,tile_size=self.tile_size)
        self.enemies.append(enemy)
        if enemy in self.enemies:
            print(f"Enemy added at: ({enemy.grid_x},{enemy.grid_y})")

    def has_line_of_sight(self, start_x, start_y, end_x, end_y):
        x0, y0 = int(start_x), int(start_y)
        x1, y1 = int(end_x), int(end_y)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        x, y = x0, y0
        n = 1 + dx + dy
        x_inc = 1 if x1 > x0 else -1
        y_inc = 1 if y1 > y0 else -1
        error = dx - dy

        dx *= 2
        dy *= 2

        for _ in range(n):
            if self.is_blocked(x, y):
                return False  # Wall in the way

            if error > 0:
                x += x_inc
                error -= dy
            else:
                y += y_inc
                error += dx

        return True  # No walls blocking
