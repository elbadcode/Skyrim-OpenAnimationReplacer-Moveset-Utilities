import os
import json
import random
import shutil
from collections import namedtuple
from typing import List, Any

oar_path = os.path.join(os.path.dirname(__file__), "meshes", "actors", "character", "animations",
                        "openanimationreplacer")
dar_path = os.path.join(os.path.dirname(__file__), "meshes", "actors", "character", "animations",
                        "dynamicanimationreplacer", "_customconditions")
absdar = os.path.abspath(dar_path)
absdar = os.path.abspath(oar_path)
priority_paths= {}
priorities = []
paths = []


def list_priorities():
    with open("priority_log.txt", "a") as log_file:
        for root, dirs, files in os.walk(dar_path, topdown=False):
            files_found = False
            for file in files:
                if file.endswith(".hkx") or file.endswith("_conditions.txt"):
                    files_found = True
                    break
            if files_found:
                try:
                    config_file_path = os.path.join(root, "_conditions.txt")
                    if os.path.exists(config_file_path):
                        config_name = os.path.basename(os.path.dirname(config_file_path))

                        try:
                            prio = int(float(config_name))
                            priorities.append(prio)
                            paths.append(config_file_path)
                            print(f"path:{config_file_path}, priority: {prio}", file=log_file)
                        except ValueError:
                            print('not a number')

                except FileExistsError:
                    print('no file')

        for root, dirs, files in os.walk(oar_path, topdown=False):
            files_found = False
            for file in files:
                try:
                    if file.endswith(".hkx"):
                        files_found = True
                        break
                except UnboundLocalError:
                    print('unbound')

            if (files_found):
                try:
                    config_file_path = os.path.join(root, "config.json")

                    if os.path.exists(config_file_path):
                        if ("variant" in config_file_path):
                            break
                        create_backup(config_file_path)
                        config_file_path = config_file_path.lower()
                        try:
                            with open(config_file_path, "r+") as config_file:  # Open in read/write mode
                                print(config_file_path)
                                try:
                                    config_data = json.load(config_file)
                                    print(config_data)
                                    config_data["name"] = config_file_path
                                    try:
                                        print(f"Name: {config_file_path}", file=log_file)
                                        try:
                                            prio = config_data["priority"]
                                            print(f"Original priority: {prio}", file=log_file)
                                            priorities.append(prio)
                                            paths.append(config_file_path)
                                        except KeyError:
                                            print('oop')
                                    except UnicodeEncodeError:
                                        print('utf')
                                except json.decoder.JSONDecodeError:
                                    print('bad json')
                        except FileNotFoundError:
                            print('uea')
                except FileExistsError:
                    print('oops')


def create_backup(file_path):
    backup_path = file_path + ".bak"
    shutil.copyfile(file_path, backup_path)


def get_new_priority(current_priority, mod_type, offset=0):
    """
    Generates a new priority within a range based on mod type and offset.

    Args:
        current_priority (int): The original priority of the mod.
        mod_type (str): "oar" or "dar" depending on the mod type.
        offset (int, optional): The minimum difference between new and original priority. Defaults to 10.

    Returns:
        int: The new randomized priority.
    """
    lower_bound = current_priority - offset
    upper_bound = current_priority + offset
    # Ensure boundaries are within a valid range (adjust as needed)
    lower_bound = max(lower_bound, 1)
    upper_bound = min(upper_bound, 50000)  # Adjust upper bound as needed

    new_priority = random.randrange(lower_bound, upper_bound)
    return new_priority


def modify_config_files():
    list_priorities()
    for i in range(1, len(priorities)):

        files_found = False
        with open("priority_log.txt", "a") as log_file:
            for root, dirs, files in os.walk(dar_path, topdown=False):
                try:
                    if file.endswith(".hkx") or file.endswith("_conditions.txt"):
                        files_found = True
                        break  # No need to check further files
                except UnboundLocalError:
                    print('unbound')
                if files_found:
                    config_file_path = os.path.join(root, "_conditions.txt")
                    if os.path.exists(config_file_path):
                        config_file_path = config_file_path.lower()

                        config_name = os.path.basename(os.path.dirname(config_file_path))

                        print(f"Original DAR priority: {config_name}", file=log_file)
                        config_file_path = os.path.abspath(config_name)
                        print(f"DAR path: {config_file_path}", file=log_file)
                        prio = -1
                        try:
                            prio = int(float(config_name))
                            while prio > 40000:
                                prio = get_new_priority(prio, "dar")
                                new = os.path.join(absdar, str(prio))
                            new = os.path.join(absdar, str(prio))
                            os.chdir(dar_path)
                            try:
                                os.rename(os.path.abspath(config_name), new)
                            except FileExistsError:
                                prio = get_new_priority(prio, "oar")
                                new = os.path.join(absdar, str(prio))
                                os.rename(os.path.abspath(config_name), new)
                            print(f"New DAR priority: {new}", file=log_file)
                        except ValueError:
                            files_found = False
                            break
                files_found = False
                for root, dirs, files in os.walk(oar_path):
                    for file in files:
                        if file.endswith(".hkx"):
                            files_found = True
                            break

                try:
                    config_file_path = os.path.join(root, "config.json")
                    if os.path.exists(config_file_path):
                        create_backup(config_file_path)
                        config_Zile_path = config_file_path.lower()
                    try:
                        with open(config_file_path, "r+") as config_file:  # Open in read/write mode
                            config_data = json.load(config_file)
                            config_name = os.path.basename(os.path.dirname(config_file_path))
                            config_data["name"] = config_name
                            print(f"Name: {config_name}", file=log_file)
                            try:
                                prio = config_data["priority"]
                                print(f"Original priority: {prio}", file=log_file)
                                prio = get_new_priority(prio,'oar', 100)
                                config_data["priority"] = prio
                                print(f"New priority: {prio}", file=log_file)
                                # Overwrite the file with the updated data
                                config_file.seek(0)  # Move back to the beginning of the file
                                json.dump(config_data, config_file, indent=4)
                                config_file.truncate()  # Remove any extra content
                            except KeyError:
                                print("not a submod")
                        break
                    except FileNotFoundError:
                        print('no')
                finally:
                    print('fin')

if __name__ == "__main__":
    modify_config_files()
