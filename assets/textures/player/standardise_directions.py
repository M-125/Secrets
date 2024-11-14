import os

# little renaming thingy because my autism ass brain cant realise what "front" and "back" means 💀

current_directory = os.getcwd()

for filename in os.listdir(current_directory):
    old_file_path = os.path.join(current_directory, filename)
    
    if os.path.isfile(old_file_path):
        new_filename = filename.replace('front', 'down').replace('back', 'up')
        
        new_file_path = os.path.join(current_directory, new_filename)
        
        os.rename(old_file_path, new_file_path)
        print(f'Renamed: {filename} -> {new_filename}')
