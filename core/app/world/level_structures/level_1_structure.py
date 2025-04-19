import pygame
from core.app.entities.coin import Coin
from core.app.entities.spike import Spike

def draw_house_tiles(terrain_tiles):
    house_tiles = []

    #house floor
    for x in range(50, 69):
        for y in range(50, 69):
            tile = terrain_tiles.get("floor", terrain_tiles["missing_texture"])

            ground_sprite = pygame.sprite.Sprite()
            ground_sprite.image = tile.image
            ground_sprite.rect = tile.image.get_rect()

            house_tiles.append(((x, y), ground_sprite))


    #house yard
    for x in range(52, 68):
        for y in range(70, 79):
            tile = terrain_tiles.get("grass", terrain_tiles["missing_texture"])

            ground_sprite = pygame.sprite.Sprite()
            ground_sprite.image = tile.image
            ground_sprite.rect = tile.image.get_rect()

            house_tiles.append(((x, y), ground_sprite))

    #house yard path
    for x in range(58,62):
        for y in range(70,79):
            tile = terrain_tiles.get("stone", terrain_tiles["missing_texture"])

            ground_sprite = pygame.sprite.Sprite()
            ground_sprite.image = tile.image
            ground_sprite.rect = tile.image.get_rect()

            house_tiles.append(((x, y), ground_sprite))

    return house_tiles

def draw_building_walls(object_tiles):
    #house walls
    building_wall_tiles = []

    #top wall
    for x in range(50,70):
        for y in range(49,50):
            tile = object_tiles.get("wall", object_tiles["missing_texture"])

            ground_sprite = pygame.sprite.Sprite()
            ground_sprite.image = tile.image
            ground_sprite.rect = tile.image.get_rect()

            building_wall_tiles.append(((x, y), ground_sprite))

    #bottom wall left half
    for x in range(50,58):
        for y in range(69,70):
            tile = object_tiles.get("wall", object_tiles["missing_texture"])

            ground_sprite = pygame.sprite.Sprite()
            ground_sprite.image = tile.image
            ground_sprite.rect = tile.image.get_rect()

            building_wall_tiles.append(((x, y), ground_sprite))

    #bottom wall right half
    for x in range(62,70):
        for y in range(69,70):
            tile = object_tiles.get("wall", object_tiles["missing_texture"])

            ground_sprite = pygame.sprite.Sprite()
            ground_sprite.image = tile.image
            ground_sprite.rect = tile.image.get_rect()

            building_wall_tiles.append(((x, y), ground_sprite))

    #left wall
    for x in range(49,50):
        for y in range(49,70):
            tile = object_tiles.get("wall", object_tiles["missing_texture"])

            ground_sprite = pygame.sprite.Sprite()
            ground_sprite.image = tile.image
            ground_sprite.rect = tile.image.get_rect()

            building_wall_tiles.append(((x, y), ground_sprite))

    #right wall
    for x in range(69,70):
        for y in range(50,69):
            tile = object_tiles.get("wall", object_tiles["missing_texture"])

            ground_sprite = pygame.sprite.Sprite()
            ground_sprite.image = tile.image
            ground_sprite.rect = tile.image.get_rect()

            building_wall_tiles.append(((x, y), ground_sprite))


    return building_wall_tiles

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

def draw_level_border(object_tiles):
    level_border_tiles = []

    #top level border
    for x in range(12,112):
        for y in range(11,12):
            tile = object_tiles.get("wall", object_tiles["missing_texture"])

            ground_sprite = pygame.sprite.Sprite()
            ground_sprite.image = tile.image
            ground_sprite.rect = tile.image.get_rect()

            level_border_tiles.append(((x, y), ground_sprite))
    
    #bottom level border
    for x in range(12,112):
        for y in range(111,112):
            tile = object_tiles.get("wall", object_tiles["missing_texture"])

            ground_sprite = pygame.sprite.Sprite()
            ground_sprite.image = tile.image
            ground_sprite.rect = tile.image.get_rect()

            level_border_tiles.append(((x, y), ground_sprite))

    #left level border
    for x in range(11,12):
        for y in range(11,112):
            tile = object_tiles.get("wall", object_tiles["missing_texture"])

            ground_sprite = pygame.sprite.Sprite()
            ground_sprite.image = tile.image
            ground_sprite.rect = tile.image.get_rect()

            level_border_tiles.append(((x, y), ground_sprite))

    #right level border
    for x in range(111,112):
        for y in range(11,112):
            tile = object_tiles.get("wall", object_tiles["missing_texture"])

            ground_sprite = pygame.sprite.Sprite()
            ground_sprite.image = tile.image
            ground_sprite.rect = tile.image.get_rect()

            level_border_tiles.append(((x, y), ground_sprite))

    return level_border_tiles

def draw_spike_tiles(world):
    positions = [(65, 65)]
    for grid_x, grid_y in positions:
        spike = Spike(
            world.screen,  # pass the screen or surface here
            grid_x,
            grid_y,
            world.tile_size,
        )
        world.entities.append(spike)

def draw_coin_tiles(world, coin_frames):
    positions = [(55, 55), (60, 60), (65, 65)]
    for grid_x, grid_y in positions:
        coin = Coin(
            world.screen,  # pass the screen or surface here
            grid_x,
            grid_y,
            world.tile_size,
            coin_frames["gold"],  # or use another type's frames
            "gold"  # define the coin type for value assignment
        )
        world.entities.append(coin)
