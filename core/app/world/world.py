
import json
import pygame
from core.app.world.tiles import Tile
from core.app.entities.animate import Animation
from core.app.entities.coin import Coin
from core.app.world.level_structure import *

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
        self.gold_coin_animation = None

        self.load_assets()  # <-- New method
        self.load_terrain_tiles()
        self.load_foreground_tiles()


    def load_assets(self):
        # Only load images once, store frames, not Animation instances
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

    def place_static(self, x, y, obj, layer):
        valid_layers = ["ground", "object", "foreground"]
        if layer not in valid_layers:
            raise ValueError(f"Invalid layer '{layer}'. Allowed layers: {valid_layers}")

        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            if (x, y) not in self.tiles:
                self.tiles[(x, y)] = {key: None for key in valid_layers}
            self.tiles[(x, y)][layer] = obj

    def generate_base_terrain(self):
        # Simple fallback terrain if JSON level isn't found
        default_tiles = draw_default_tiles(self.grid_height,self.grid_width,self.terrain_tiles)
        for (position, sprite) in default_tiles:
            x, y = position
            self.place_static(x, y, sprite, layer="ground")
        house_floor_tiles = draw_house_floor(self.terrain_tiles)
        for (position, sprite) in house_floor_tiles:
            x, y = position
            self.place_static(x, y, sprite, layer="ground")
        house_yard_tiles = draw_house_yard(self.terrain_tiles)
        for (position, sprite) in house_yard_tiles:
            x, y = position
            self.place_static(x, y, sprite, layer="ground")
        house_front_yard_path_tiles = draw_house_front_yard_path(self.terrain_tiles)
        for (position, sprite) in house_front_yard_path_tiles:
            x, y = position
            self.place_static(x, y, sprite, layer="ground")

    def load_from_json(self):
        filename = f"assets/levels/level{self.level}.json"

        with open(filename, "r") as f:
            data = json.load(f)

        # --- Place terrain from JSON ---
        for tile_data in data.get("terrain", []):
            x, y = tile_data["x"], tile_data["y"]
            tile_type = tile_data.get("type", "grass")  # Default to grass
            tile = self.terrain_tiles.get(tile_type, self.terrain_tiles["grass"])

            ground_sprite = pygame.sprite.Sprite()
            ground_sprite.image = tile.image
            ground_sprite.rect = tile.image.get_rect()

            self.place_static(x, y, ground_sprite, layer="ground")

        # --- Place building tiles ---
        for tile_data in data.get("building_tiles", []):
            if "x" not in tile_data or "y" not in tile_data:
                continue  # Skip invalid entries
            x, y = tile_data["x"], tile_data["y"]
            tile_type = tile_data.get("type", "building_roof")
            tile = self.foreground_tiles.get(tile_type, self.foreground_tiles["building_roof"])

            roof_sprite = pygame.sprite.Sprite()
            roof_sprite.image = tile.image
            roof_sprite.rect = tile.image.get_rect()

            self.place_static(x, y, roof_sprite, layer="foreground")

        # --- Place walls as terrain-like tiles ---
        for wall_data in data.get("walls", []):
            if "x" not in wall_data or "y" not in wall_data:
                continue  # Skip invalid entries

            x, y = wall_data["x"], wall_data["y"]
            wall_type = wall_data.get("type", "shittywall")  # Default to "shittywall" if no type is provided

            # Select the correct wall image based on the wall type
            wall_image = pygame.image.load("assets/graphics/game/walls/shittywall.png").convert_alpha()

            # Create a wall sprite
            wall = pygame.sprite.Sprite()
            wall.image = wall_image
            wall.rect = wall_image.get_rect()

            # Place the wall just like other tiles
            self.place_static(x, y, wall, layer="object")  # "object" layer to keep walls separate

        # --- Place coins ---
        for coin_data in data.get("coins", []):
            x, y = coin_data["x"], coin_data["y"]
            coin_type = coin_data.get("type", "gold")
            frames = self.coin_frames.get(coin_type)

            if frames:
                if coin_type == "gold":
                    animation = Animation(frames, 5)  # create a new instance!
                elif coin_type == "silver":
                    animation = Animation(frames, 10)  # create a new instance!
                elif coin_type == "bronze":
                    animation = Animation(frames, 15)  # create a new instance!
                coin = Coin(self.screen, x, y, self.tile_size, animation, coin_type)
                self.entities.append(coin)
            else:
                print(f"Warning: Unknown coin type '{coin_type}' at ({x},{y})")


    def is_blocked(self, x, y):
        cell = self.tiles.get((x, y))
        if not cell:
            return False
        if cell["object"]:
            print(f"Blocked by object at {x}, {y}")
            return True
        if cell["ground"] is None:
            print(f"No ground at {x}, {y}")
            return True
        return False

    def update(self):
        for entity in self.entities:
            entity.update()

    def draw(self, camera, debug=False):
       # Draw ground and objects first
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
        # Draw the foreground layer (above player and entities)
        for (x, y), layers in self.tiles.items():
            obj = layers.get("foreground")
            if obj:
                obj.rect.topleft = (x * self.tile_size, y * self.tile_size)
                obj.rect = camera.apply(obj.rect)
                
                if debug:
                    # Apply semi-transparent red tint for debugging
                    debug_image = self.tint_surface(obj.image, (255, 0, 0))
                    self.screen.blit(debug_image, obj.rect)
                else:
                    self.screen.blit(obj.image, obj.rect)

    def tint_surface(self, surface, tint_color):
        tinted = surface.copy()
        tinted.fill(tint_color + (0,), special_flags=pygame.BLEND_RGBA_ADD)
        return tinted