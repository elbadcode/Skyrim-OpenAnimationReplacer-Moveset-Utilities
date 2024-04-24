import os
import json
import random
import shutil


def create_backup(file_path):
    backup_path = file_path + ".bak"
    shutil.copyfile(file_path, backup_path)


def modify_config_files():
    oar_path = os.path.join(os.path.dirname(__file__), "meshes", "actors", "character", "animations",
                            "openanimationreplacer")
    dar_path = os.path.join(os.path.dirname(__file__), "meshes", "actors", "character", "animations",
                            "dynamicanimationreplacer", "_customconditions")
    absdar = os.path.abspath(dar_path)
    check = []
    with open("priority_log.txt", "a") as log_file:

        for root, dirs, files in os.walk(oar_path):
            files_found = False
            for file in files:
                if file.endswith(".hkx"):
                    files_found = True
                    break
            if files_found:
                for file in files:
                    try:
                        config_file_path = os.path.join(root, "user.json")

                        if os.path.exists(config_file_path):
                            create_backup(config_file_path)
                            config_file_path = config_file_path.lower()
                            with open(config_file_path, "r+") as config_file:  # Open in read/write mode
                                try:
                                    config_data = json.load(config_file)
                                    config_name = os.path.basename(os.path.dirname(config_file_path))
                                    config_data["name"] = config_name
                                    print(f"Name: {config_name}", file=log_file)
                                    prio = config_data["priority"]
                                    print(prio)
                                    print(f"Original priority: {prio}", file=log_file)
#Change these
                                    prio = random.randrange(10, 69000)
                                    while prio in check:
                                        prio = random.randrange(10, 69090)
                                    config_data["priority"] = prio
                                    check.append(prio)
                                    print(f"New priority: {prio}", file=log_file)
                                    # Overwrite the file with the updated data
                                    config_file.seek(0)  # Move back to the beginning of the file
                                    json.dump(config_data, config_file, indent=2)
                                    config_file.truncate()  # Remove any extra content
                                except json.decoder.JSONDecodeError:
                                    print("json error")
                    except FileExistsError:
                        try:
                            config_file_path = os.path.join(root, "config.json")

                            if os.path.exists(config_file_path):
                                create_backup(config_file_path)
                                config_file_path = config_file_path.lower()
                                with open(config_file_path, "r+") as config_file:  # Open in read/write mode
                                    try:
                                        config_data = json.load(config_file)
                                        config_name = os.path.basename(os.path.dirname(config_file_path))
                                        config_data["name"] = config_name
                                        print(f"Name: {config_name}", file=log_file)
                                        prio = config_data["priority"]
                                        print(prio)
                                        print(f"Original priority: {prio}", file=log_file)
#Change these
                                        prio = random.randrange(10, 69000)
                                        while prio in check:
                                            prio = random.randrange(10, 69090)
                                        config_data["priority"] = prio
                                        check.append(prio)
                                        print(f"New priority: {prio}", file=log_file)
                                        # Overwrite the file with the updated data
                                        config_file.seek(0)  # Move back to the beginning of the file
                                        json.dump(config_data, config_file, indent=2)
                                        config_file.truncate()  # Remove any extra content
                                    except json.decoder.JSONDecodeError:
                                        print("json error")
                        except FileExistsError:
                            print('oop')


if __name__ == "__main__":
    modify_config_files()
