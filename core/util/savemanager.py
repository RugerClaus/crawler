import json
import os
from core.app.entities.coin import Coin
from core.app.entities.spike import Spike
from core.app.entities.healthpotion import HealthPotion

class SaveManager:
    def __init__(self, filepath="saves/save.json"):
        self.filepath = filepath

    def save(self, player, world):
        print(f"[SAVE] Entities before saving: {len(world.entities)}")
        data = {
            "player": {
                "x": player.rect.x,
                "y": player.rect.y,
                "health": player.current_health,
                "potion_count": player.health_potion_count,
                "money": player.money,
                "collected_items": [
                    {
                        "item_id": item_props["item_id"], 
                        "item_type": item_props["item_type"],
                        "potion_type": item_props.get("potion_type", ""),
                        "heal_amount": item_props.get("heal_amount", 0),
                        "coin_type": item_props.get("coin_type", "")
                    }
                    for item_props in player.collected_items
                ],
                "discarded_items": list(player.discarded_items)
            },
            "level": world.level,
            "entities": []
        }

        # Save entities (Coins and Health Potions)
        for entity in world.entities:
            if isinstance(entity, Coin):
                # Only save coins that are not collected by the player
                if entity.entity_id not in [item["item_id"] for item in player.collected_items]:
                    data['entities'].append({
                        'type': entity.type,
                        'grid_x': entity.grid_x,
                        'grid_y': entity.grid_y,
                        'coin_type': entity.coin_type,
                        'entity_id': entity.entity_id
                    })
            elif isinstance(entity, HealthPotion):
                # Only save health potions that are not collected by the player
                if entity.entity_id not in [item["item_id"] for item in player.collected_items]:
                    data['entities'].append({
                        'type': entity.type,
                        'grid_x': entity.grid_x,
                        'grid_y': entity.grid_y,
                        'potion_type': entity.potion_type,
                        'entity_id': entity.entity_id
                    })

        # Save the data to a JSON file
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=4)
        print(f"[SAVE] Game saved to {self.filepath}")
        print(f"[SAVE] Entities after saving: {len(world.entities)}")

    def save_exists(self):
        """Check if the save file exists."""
        return os.path.exists(self.filepath)

    def load(self, player, world):
        """Load the game save if the file exists."""
        if not self.save_exists():
            print("[SAVE] No save file found.")
            return False  # Return None or handle appropriately

        with open(self.filepath, "r") as f:
            data = json.load(f)

        self.loaded_data = data

        # Load the level data
        saved_level = data.get("level")
        if saved_level is not None:
            world.level = saved_level
            world.generate_map(player)
        else:
            print("[SAVE] No level data found, using default level.")
            world.generate_map(player)

        # Load player data
        player.rect.centerx = data["player"]["x"]
        player.rect.centery = data["player"]["y"]
        player.current_health = data["player"]["health"]
        player.health_potion_count = data["player"]["potion_count"]
        player.money = data["player"]["money"]

        # Rebuild the collected_items list using the saved item data
        player.collected_items = [
            {
                "item_id": item_data["item_id"],
                "item_type": item_data["item_type"],
                "potion_type": item_data.get("potion_type", ""),
                "heal_amount": item_data.get("heal_amount", 0),
                "coin_type": item_data.get("coin_type", "")
            }
            for item_data in data["player"]["collected_items"]
        ]

        player.discarded_items = set(data["player"]["discarded_items"])

        # Load entities
        world.entities = []
        for entity_data in data["entities"]:
            entity_type = entity_data["type"]
            x, y = entity_data["grid_x"], entity_data["grid_y"]

            if entity_type == "Coin":
                # Skip coins that have already been collected
                if entity_data["entity_id"] in [item["item_id"] for item in player.collected_items] or entity_data["entity_id"] in player.discarded_items:
                    continue
                coin_type = entity_data["coin_type"]
                coin = Coin(world.screen, entity_data["entity_id"], coin_type, 0)  # Adjust as necessary
                coin.rect.x = x
                coin.rect.y = y
                world.entities.append(coin)

            elif entity_type == "HealthPotion":
                # Skip potions that have already been collected
                if entity_data["entity_id"] in [item["item_id"] for item in player.collected_items] or entity_data["entity_id"] in player.discarded_items:
                    continue
                potion_type = entity_data["potion_type"]
                health_potion = HealthPotion(world.screen, entity_data["entity_id"], potion_type, 0)  # Adjust as necessary
                health_potion.rect.x = x
                health_potion.rect.y = y
                world.entities.append(health_potion)

        print(f"[SAVE] Game loaded from {self.filepath}")
        return data
