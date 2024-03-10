import os
import shutil
import re

def create_backup(file_path):
    backup_path = file_path + ".bak"
    shutil.copyfile(file_path, backup_path)

def modify_conditions_files():
    dar_path = os.path.join(os.path.dirname(__file__), "meshes", "actors", "character", "animations", "dynamicanimationreplacer", "_customconditions")

    for folder in os.listdir(dar_path):
        folder_path = os.path.join(dar_path, folder)
        if os.path.isdir(folder_path):  # Check if it's a folder
            for file in os.listdir(folder_path):
                  conditions_file_path = os.path.join(folder_path, "_conditions.txt")
                  create_backup(conditions_file_path)
                  conditions_file_path = conditions_file_path.lower()
                  print(folder_path + " " + conditions_file_path)
                  if os.path.exists(conditions_file_path):
                      with open(conditions_file_path, "r+") as conditions_file:
                        content = conditions_file.read()
                        regex = r"\b(AND+)\s+\1\b"
                        modified_content = re.sub(regex, "AND", content )

                        # Write the modified content back to the file
                        conditions_file.seek(0)
                        conditions_file.write(modified_content)
                        conditions_file.truncate()
                        print(f"Modified _conditions.txt file: {conditions_file_path}")

if __name__ == "__main__":
  modify_conditions_files()
