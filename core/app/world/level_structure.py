import pygame

def draw_house_floor(terrain_tiles):
    house_floor_tiles = []
    for x in range(50, 69):
        for y in range(50, 69):
            tile = terrain_tiles.get("floor", terrain_tiles["missing_texture"])

            ground_sprite = pygame.sprite.Sprite()
            ground_sprite.image = tile.image
            ground_sprite.rect = tile.image.get_rect()

            house_floor_tiles.append(((x, y), ground_sprite))

    return house_floor_tiles

def draw_house_yard(terrain_tiles):
    house_yard_tiles = []
    for x in range(52, 68):
        for y in range(70, 79):
            tile = terrain_tiles.get("grass", terrain_tiles["missing_texture"])

            ground_sprite = pygame.sprite.Sprite()
            ground_sprite.image = tile.image
            ground_sprite.rect = tile.image.get_rect()

            house_yard_tiles.append(((x, y), ground_sprite))

    return house_yard_tiles

def draw_house_front_yard_path(terrain_tiles):
    house_front_yard_path_tiles = []
    for x in range(58,62):
        for y in range(70,79):
            tile = terrain_tiles.get("stone", terrain_tiles["missing_texture"])

            ground_sprite = pygame.sprite.Sprite()
            ground_sprite.image = tile.image
            ground_sprite.rect = tile.image.get_rect()

            house_front_yard_path_tiles.append(((x, y), ground_sprite))
    return house_front_yard_path_tiles

def draw_default_tiles(grid_height,grid_width,terrain_tiles):
    default_tiles = []
    for y in range(grid_height):
        for x in range(grid_width):
            tile_type = "missing_texture"
            tile = terrain_tiles.get(tile_type, terrain_tiles["missing_texture"])

            ground_sprite = pygame.sprite.Sprite()
            ground_sprite.image = tile.image
            ground_sprite.rect = ground_sprite.image.get_rect()

            default_tiles.append(((x,y),ground_sprite))

    return default_tiles