import os
import json

import shutil

def create_backup(file_path):
    backup_path = file_path + ".bak"
    shutil.copyfile(file_path, backup_path)

def modify_config_files():
    oar_path = os.path.join(os.path.dirname(__file__), "meshes", "actors", "character", "animations", "openanimationreplacer")

    for root, dirs, files in os.walk(oar_path):
        for file in files:
            if file.startswith("mco_") and file.endswith(".hkx"):
                config_file_path = os.path.join(root, "config.json")
                create_backup(config_file_path)
                config_file_path = config_file_path.lower()
                if os.path.exists(config_file_path):
                    with open(config_file_path, "r+") as config_file:  # Open in read/write mode
                        config_data = json.load(config_file)

                        # Add the new condition
                        new_condition = {
                            "condition": "Random",
                            "requiredVersion": "1.0.0.0",
                            "Random value": {
                                "min": 0.0,
                                "max": 1.0
                            },
                            "Comparison": "<",
                            "Numeric value": {
                                "value": 0.85
                            }
                        }
                        config_data["conditions"].append(new_condition)

                        # Overwrite the file with the updated data
                        config_file.seek(0)  # Move back to the beginning of the file
                        json.dump(config_data, config_file, indent=4)
                        config_file.truncate()  # Remove any extra content
                    break

if __name__ == "__main__":
    modify_config_files()
