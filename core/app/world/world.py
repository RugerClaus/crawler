
import json
import pygame
from core.app.world.tiles import Tile
from core.app.enitites.animate import Animation
from core.app.enitites.coin import Coin

class World:
    def __init__(self, screen, grid_width, grid_height, tile_size, starting_level):
        self.screen = screen
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.tile_size = tile_size
        self.level = starting_level
        self.tiles = {}  # Static map: {(x, y): {"ground": obj, "object": obj}}
        self.entities = []  # Dynamic objects: [Coin(), Player(), Enemy()]
        self.gold_coin_animation = None

        self.load_assets()  # <-- New method
        self.load_terrain_tiles()

    def load_assets(self):
        self.coin_animations = {
            "gold": Animation([
                pygame.image.load(f"assets/graphics/game/currency/gold_coin_{i}.png").convert_alpha()
                for i in range(1, 4)
            ], frame_delay=50),

            "silver": Animation([
                pygame.image.load(f"assets/graphics/game/currency/silver_coin_{i}.png").convert_alpha()
                for i in range(1, 4)
            ], frame_delay=50),

            "bronze": Animation([
                pygame.image.load(f"assets/graphics/game/currency/bronze_coin_{i}.png").convert_alpha()
                for i in range(1, 4)
            ], frame_delay=50),
        }

    def load_terrain_tiles(self):
        """Define different terrain tiles."""
        self.terrain_tiles = {
            "dirt": Tile("assets/graphics/game/ground/shittydirt.png"),
            "grass": Tile("assets/graphics/game/ground/grass.png"),
            "missing_texture": Tile("assets/graphics/game/undefined.png")
            # "water": Tile("assets/graphics/game/ground/water.png", is_walkable=False),
            # "stone": Tile("assets/graphics/game/ground/stone.png"),
        }

    def place_static(self, x, y, obj, layer):
        if layer not in ["ground", "object"]:
            raise ValueError("Only 'ground' or 'object' allowed in static tiles!")

        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            if (x, y) not in self.tiles:
                self.tiles[(x, y)] = {"ground": None, "object": None}
            self.tiles[(x, y)][layer] = obj

    def generate_base_terrain(self):
        # Simple fallback terrain if JSON level isn't found
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                tile_type = "missing_texture"
                tile = self.terrain_tiles.get(tile_type, self.terrain_tiles["missing_texture"])

                ground_sprite = pygame.sprite.Sprite()
                ground_sprite.image = tile.image
                ground_sprite.rect = ground_sprite.image.get_rect()

                self.place_static(x, y, ground_sprite, layer="ground")

    def load_from_json(self):
        filename = f"assets/levels/level{self.level}.json"
        wall_image = pygame.image.load("assets/graphics/game/walls/shittywall.png").convert_alpha()

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

        # --- Place walls ---
        for wall_data in data.get("walls", []):
            x, y = wall_data["x"], wall_data["y"]
            wall = pygame.sprite.Sprite()
            wall.image = wall_image
            wall.rect = wall_image.get_rect()
            self.place_static(x, y, wall, layer="object")

        # --- Place coins ---
        for coin_data in data.get("coins", []):
            x, y = coin_data["x"], coin_data["y"]
            coin_type = coin_data.get("type", "gold")
            animation = self.coin_animations.get(coin_type)

            if animation:
                coin = Coin(self.screen, x, y, self.tile_size, animation, coin_type)
                self.entities.append(coin)
            else:
                print(f"Warning: Unknown coin type '{coin_type}' at ({x},{y})")

    def is_blocked(self, x, y):
        cell = self.tiles.get((x, y))
        if not cell:
            return False  # Empty tile
        return cell["object"] is not None  # Solid object blocks movement

    def update(self):
        for entity in self.entities:
            entity.update()

    def draw(self, camera):
        # Draw static world tiles
        for (x, y), layers in self.tiles.items():
            screen_x = x * self.tile_size
            screen_y = y * self.tile_size

            for layer_name in ["ground", "object"]:
                obj = layers[layer_name]
                if obj:
                    obj.rect.topleft = (screen_x, screen_y)
                    obj.rect = camera.apply(obj.rect)  # Adjust with camera
                    self.screen.blit(obj.image, obj.rect)

        # Draw dynamic entities
        for entity in self.entities:
            entity.draw(camera)

    def increase_level(self):
        self.level += 1
