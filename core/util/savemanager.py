import json
import os
from core.app.entities.coin import Coin
from core.app.entities.healthpotion import HealthPotion

class SaveManager:
    def __init__(self, slot):
        self.slot = slot
        self.filepath = f"saves/save_slot_{self.slot}.json"

    def save(self, player, world, version):
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
            "entities": [],
            "version": version
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
        return os.path.exists(self.filepath)

    def load(self, player, world, version):
        if not self.save_exists():
            print("[SAVE] No save file found.")
            return False  # Return None or handle appropriately

        with open(self.filepath, "r") as f:
            data = json.load(f)

        self.loaded_data = data

        # Check if the version in the save file matches the current game version
        save_version = data.get("version")
        if save_version != version:
            print(f"Save version {save_version} is outdated. Migrating to version {version}...")
            self.handle_version_migration(data, save_version, version)

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

        player.discarded_items = data["player"]["discarded_items"]

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

    def handle_version_migration(self, save_data, old_version, new_version):
        # Migration logic based on version differences
        if old_version == "1.0" and new_version == "1.1":
            self.migrate_v1_to_v2(save_data)
        elif old_version == "1.1" and new_version == "1.2":
            self.migrate_v2_to_v3(save_data)
        # Add more migrations as needed
        
        # Update the save file with the new version
        save_data["version"] = new_version
        self.save_game(save_data)

    def migrate_v1_to_v2(self, save_data):
        # Example migration: Add a new player attribute in v1.1
        if "player_health" in save_data["player"]:
            save_data["player"]["health"] = save_data["player"]["player_health"]
            del save_data["player"]["player_health"]

    def migrate_v2_to_v3(self, save_data):
        # Example migration: Add a new feature in v1.2
        save_data["world_data"]["new_feature"] = "default_value"

    def save_game(self, save_data):
        # Save the data back to the file
        with open(self.filepath, 'w') as f:
            json.dump(save_data, f, indent=4)
        print("[SAVE] Game updated to the latest version.")
