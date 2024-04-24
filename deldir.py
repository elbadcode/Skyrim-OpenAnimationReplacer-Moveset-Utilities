import os

import os

import os

def delete_dirs(path):
    for dirpath, dirnames, files in os.walk(path, topdown=False):
        hkx_files = [f for f in files if f.endswith('.hkx')]
        files = [f for f in files]

        # Check if there are no .hkx files and only config.json is present or not
        if not dirnames and not hkx_files and (not files or files == ['_conditions.txt']):
            # Deleting config.json file from directory before deleting directory
            if '_conditions.txt' in files:
                print(f'Removing file: {dirpath}\\_conditions.txt')
                os.remove(os.path.join(dirpath, '_conditions.txt'))

            # Trying to delete directory
            try:
                print(f'Removing directory: {dirpath}')
                os.rmdir(dirpath)
            except:
                print(f'Failed to remove directory: {dirpath}. Possibly not empty.')

directory = os.getcwd()
delete_dirs(directory)