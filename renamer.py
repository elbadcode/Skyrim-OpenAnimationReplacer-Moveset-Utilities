import os
import re
import shutil

KEY_MAPPINGS = {
    801: "forward",
    802: "left",
    803: "backward",
    804: "right",
}


def organize_files(folder_path):
  """
  Scans a folder, moves files to corresponding variant folders,
  iterating for duplicates.
  """
  os.chdir(folder_path)
  for filename in os.listdir(folder_path):
    # Extract base filename without extension
    base_filename, ext = os.path.splitext(filename)

    # Skip non-hkx files
    if ext.lower() != ".hkx":
      continue

    # Construct variant folder name
    variant_folder = f"_variants_{base_filename}"

    # Construct destination path with incrementing number for duplicates
    destination_path = os.path.join(variant_folder, "1.hkx")
    i = 1
    while os.path.exists(destination_path):
      i += 1
      destination_path = os.path.join(variant_folder, f"{i}.hkx")

    # Create variant folder if it doesn't exist
    if not os.path.exists(variant_folder):
      os.makedirs(variant_folder)

    # Move the file to the destination path 
    source_path = os.path.join(folder_path, filename)
    print(source_path)
    print(destination_path)
    os.rename(source_path, os.path.join(folder_path,destination_path))

  print(f"Finished organizing files in {folder_path}")


def search_and_rename(root_dir):
    parent_path = os.getcwd()
    """
    Searches for _conditions.txt files in subfolders, checks for magic effects, and renames folders.

    Args:
        root_dir (str): The directory to start searching from.
    """

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "_conditions.txt":
                filepath = os.path.join(dirpath, filename)
                with open(filepath, "r") as file:
                    new_dir = ""
                    content = file.read()
                    print(content)
                    match = re.search(r"HasMagicEffect\(\"Keytrace\.esp\"\|0x([0-9A-F]{3})\)", content)
                    if match:
                        key_code = int(match.group(1))
                        if key_code in KEY_MAPPINGS:
                            new_name = KEY_MAPPINGS[key_code]
                            old_dir = dirpath
                            new_dir = os.path.join(os.path.dirname(dirpath), new_name)
                            if old_dir != new_name:
                                print(f"Renaming folder '{old_dir}' to '{new_name}'")
                                print(old_dir)
                                print(new_dir)
                                os.chdir(os.path.dirname(parent_path))
                                os.makedirs(new_dir, exist_ok=True)
                                for _file in os.listdir(old_dir):
                                    if _file.endswith(".hkx"):
                                        base_filename = os.path.basename(_file)
                                        print(new_dir)
                                        print(base_filename)
                                        print(_file)
                                        new_file = os.path.join(new_dir,base_filename)
                                        print(new_file)
                                        shutil.copy(os.path.join(old_dir,_file),os.path.join(new_dir,new_file))
                        organize_files(new_dir) 
                        os.chdir(os.path.dirname(parent_path))


           
if __name__ == "__main__":
    search_and_rename(os.getcwd())  # Start from the current working directory
    print("Completed searching for conditions.txt files and renaming subfolders.")
            