import json
import os
from core.app.entities.coin import Coin
from core.app.entities.spike import Spike

class SaveManager:
    def __init__(self, filepath="saves/save.json",):
        self.filepath = filepath

    def save(self, player, world):
        data = {
            "player": {
                "x": player.rect.x,
                "y": player.rect.y,
                "health": player.current_health,
                "potion_count": player.health_potion_count
            },
            "level": world.level,  # Save the current level
            "entities": [
                entity.to_dict()
                for entity in world.entities
            ]
        }

        # Save the data to a JSON file
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=4)
        print(f"[SAVE] Game saved to {self.filepath}")
        print(f"player coords: ({data["player"]["x"]},{data["player"]["y"]})")



    def load(self, player, world):
        if not os.path.exists(self.filepath):
            print("[SAVE] No save file found.")
            return None

        with open(self.filepath, "r") as f:
            data = json.load(f)

        self.loaded_data = data  # Store loaded data for later use

        # Load the level data and switch to the correct level
        saved_level = data.get("level")
        if saved_level is not None:
            world.level = saved_level  # Set the world to the saved level
            world.generate_map()  # Generate the map for the correct level
        else:
            print("[SAVE] No level data found, using default level.")
            world.generate_map()  # Generate the map for the default level

        # Load player data
        player.rect.centerx = data["player"]["x"]
        player.rect.centery = data["player"]["y"]
        player.current_health = data["player"]["health"]
        player.potion_count = data["player"]["potion_count"]

        # Load entities
        world.entities = []
        for entity_data in data["entities"]:
            entity_type = entity_data["type"]
            x, y = entity_data["x"], entity_data["y"]

            if entity_type == "Spike":
                grid_x = entity_data["grid_x"]
                grid_y = entity_data["grid_y"]
                damage = entity_data.get("damage", 1)
                spike = Spike(world.screen, grid_x, grid_y, world.tile_size, damage)
                spike.rect.x = x
                spike.rect.y = y
                world.entities.append(spike)

            elif entity_type == "Coin":
                coin_type = entity_data["coin_type"]
                # Get animation frames or pass an empty list
                animation_frames = []  # Assuming no animation frames are saved, fallback to empty list
                coin = Coin(world.screen, entity_data["grid_x"], entity_data["grid_y"], world.tile_size, animation_frames, coin_type)
                coin.rect.x = x
                coin.rect.y = y
                world.entities.append(coin)

        print(f"[SAVE] Game loaded from {self.filepath}")
        print(f"player coords: ({data['player']['x']},{data['player']['y']})")
        return data
