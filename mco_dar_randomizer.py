import os

import shutil

def create_backup(file_path):
    backup_path = file_path + ".bak"
    if os.path.exists(backup_path) :
        backup_path = backup_path + "2"
    shutil.copyfile(file_path, backup_path)

def modify_conditions_files():
    dar_path = os.path.join(os.path.dirname(__file__), "meshes", "actors", "character", "animations", "dynamicanimationreplacer", "_customconditions")

    for folder in os.listdir(dar_path):
        folder_path = os.path.join(dar_path, folder)
        if os.path.isdir(folder_path):  # Check if it's a folder
            conditions_file_path = os.path.join(folder_path, "_conditions.txt")
            mco_files_found = False  # Initialize flag

            for file in os.listdir(folder_path):
                if file.startswith("mco_") and file.endswith(".hkx"):
                    mco_files_found = True
                    break  # No need to check further files

            if mco_files_found:  # Proceed only if mco_...hkx files were found
                if os.path.exists(conditions_file_path):
                     create_backup(conditions_file_path)
                     conditions_file_path = conditions_file_path.lower()
                     with open(conditions_file_path, "r+") as conditions_file:
                        content = conditions_file.read()
                        if content.rstrip().endswith("Random(0.85)") :
                            pass
                        elif content.rstrip()[-1:] == ")":  # Check if the last non-whitespace character is ')':
                            conditions_file.write(" AND \nRandom(0.85)")
                        elif content.rstrip().endswith("AND") or content.rstrip().endswith("OR"):
                            conditions_file.write("\nRandom(0.85)")  # Add newline if not following ')'
                else:
                    with open(conditions_file_path, "w") as conditions_file:
                        conditions_file.write("Random(0.85)")

if __name__ == "__main__":
    modify_conditions_files()
