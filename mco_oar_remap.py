import os
import json
import random
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
                
                if os.path.exists(config_file_path):
                    create_backup(config_file_path)
                    config_file_path = config_file_path.lower()
                    with open(config_file_path, "r+") as config_file:  # Open in read/write mode
                        config_data = json.load(config_file)
                        config_name = os.path.basename(os.path.dirname(config_file_path))
                        config_data["name"] = config_name
                        config_data["priority"] = random.randrange(93030024,99930024)

                        # Overwrite the file with the updated data
                        config_file.seek(0)  # Move back to the beginning of the file
                        json.dump(config_data, config_file, indent=4)
                        config_file.truncate()  # Remove any extra content
                    break

if __name__ == "__main__":
    modify_config_files()
