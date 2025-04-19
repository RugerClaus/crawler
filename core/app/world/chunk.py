import pygame

class Chunk:
    def __init__(self, world, chunk_x, chunk_y, chunk_size):
        self.world = world
        self.chunk_x = chunk_x
        self.chunk_y = chunk_y
        self.chunk_size = chunk_size

        self.tiles = {}  # Static objects in this chunk
        self.entities = []  # Dynamic objects in this chunk (e.g., coins, enemies)

        # Load chunk-specific assets (e.g., wall image)
        self.wall_image = self.load_asset("assets/graphics/game/walls/shittywall.png")

        # Generate terrain for the chunk
        self.generate_terrain()

    def load_asset(self, path):
        """Load an asset (image or sound)."""
        try:
            return pygame.image.load(path).convert_alpha()  # Load the image and convert it for faster rendering
        except pygame.error as e:
            print(f"Failed to load asset: {path}, error: {e}")
            return None

    def generate_terrain(self):
        """Generate terrain for the chunk."""
        # Based on chunk coordinates, generate terrain.
        for y in range(self.chunk_size):
            for x in range(self.chunk_size):
                # Example: Generate walls as terrain
                if x == 0 or y == 0 or x == self.chunk_size - 1 or y == self.chunk_size - 1:
                    self.add_tile(x, y, self.wall_image, "object")

    def add_entity(self, entity):
        """Add dynamic entities (coins, enemies, etc.) to this chunk."""
        self.entities.append(entity)

    def add_tile(self, x, y, obj, layer):
        """Place a static map object in this chunk."""
        if layer not in ["ground", "object"]:
            raise ValueError("Only 'ground' or 'object' allowed in static tiles!")
        self.tiles[(x, y)] = {"ground": obj, "object": None}
        
    def is_blocked(self, x, y):
        """Check if a tile is blocked by an object."""
        return (x, y) in self.tiles and self.tiles[(x, y)]["object"] is not None

    def update(self):
        """Update all dynamic entities within the chunk."""
        for entity in self.entities:
            entity.update()

    def draw(self, camera):
        """Draw the chunk's tiles and entities."""
        for (x, y), layers in self.tiles.items():
            screen_x = (self.chunk_x * self.chunk_size + x) * self.world.tile_size
            screen_y = (self.chunk_y * self.chunk_size + y) * self.world.tile_size

            for layer_name in ["ground", "object"]:
                obj = layers[layer_name]
                if obj:
                    obj.rect.topleft = (screen_x, screen_y)
                    obj.rect = camera.apply(obj.rect)  # Adjust with camera
                    self.world.screen.blit(obj.image, obj.rect)

        # Draw dynamic entities
        for entity in self.entities:
            entity.draw(camera)
