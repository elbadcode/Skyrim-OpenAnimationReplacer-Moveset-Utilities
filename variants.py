import os
import sys

def organize_files(folder_path):
  """
  Scans a folder, moves files to corresponding variant folders,
  iterating for duplicates.
  """
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
    os.rename(source_path, destination_path)

  print(f"Finished organizing files in {folder_path}")

directory = sys.argv[1]
directories = [os.path.abspath(x[0]) for x in os.walk(directory)]
directories.remove(os.path.abspath(directory)) #
for i in directories:
    if 'variants' not in i:
      os.chdir(i)         
      print(i)
      organize_files(i)