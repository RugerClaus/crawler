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
                "health": player.current_health
            },
            "level": world.level,  # Save the current level
            "entities": [
                {
                    "type": type(entity).__name__,
                    "x": getattr(entity, 'rect', entity).x,
                    "y": getattr(entity, 'rect', entity).y,
                    "grid_x": getattr(entity, 'grid_x', 0),
                    "grid_y": getattr(entity, 'grid_y', 0),
                    "damage": getattr(entity, 'damage', 1)
                } for entity in world.entities
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
        player.rect.x = data["player"]["x"]
        player.rect.y = data["player"]["y"]
        player.current_health = data["player"]["health"]

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
                coin = Coin(x, y)
                coin.rect.x = x
                coin.rect.y = y
                coin.damage = entity_data.get("damage", 1)
                world.entities.append(coin)

        print(f"[SAVE] Game loaded from {self.filepath}")
        print(f"player coords: ({data['player']['x']},{data['player']['y']})")
        return data
