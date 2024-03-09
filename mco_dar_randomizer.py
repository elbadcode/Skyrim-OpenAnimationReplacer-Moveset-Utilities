import os

def modify_conditions_files():
    dar_path = os.path.join(os.path.dirname(__file__), "Meshes", "Actors", "Character", "Animations", "DynamicAnimationReplacer", "_CustomConditions")

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
                    with open(conditions_file_path, "a") as conditions_file:
                        conditions_file.write(" AND \nRandom(0.85)")
                else:  # Create the file if it doesn't exist
                    with open(conditions_file_path, "w") as conditions_file:
                        conditions_file.write("Random(0.85)")  # Modified for consistency

if __name__ == "__main__":
    modify_conditions_files()
