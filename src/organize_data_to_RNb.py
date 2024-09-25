import os
import shutil
import re

def natural_sort(l):
    """Sorts a list in human order."""
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key=alphanum_key)

def find_rti_folder(root_path):
    """Recursively searches for an 'rti' folder starting from root_path."""
    for dirpath, dirnames, filenames in os.walk(root_path):
        if 'rti' in dirnames:
            return os.path.join(dirpath, 'rti')
    return None

def main():
    # Set the input folder path
    input_folder = r'C:\Users\Deivid\Documents\rti-data\Palermo_3D\real acquisitions\head_cs'
    
    # Get the last folder name
    last_folder_name = os.path.basename(os.path.normpath(input_folder))
    
    # Create the output folder path
    parent_dir = os.path.dirname(os.path.normpath(input_folder))
    output_folder_name = last_folder_name + '_3D_in'
    output_folder = os.path.join(parent_dir, output_folder_name)
    
    # Create the output folder and subfolders
    os.makedirs(output_folder, exist_ok=True)
    albedo_folder = os.path.join(output_folder, 'albedo')
    mask_folder = os.path.join(output_folder, 'mask')
    normal_folder = os.path.join(output_folder, 'normal')
    
    os.makedirs(albedo_folder, exist_ok=True)
    os.makedirs(mask_folder, exist_ok=True)
    os.makedirs(normal_folder, exist_ok=True)
    
    # Get list of subfolders in the input folder
    subfolders = [f for f in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, f))]
    subfolders = natural_sort(subfolders)
    
    lp_copied = False  # Flag to copy the .lp file only once

    # Process each subfolder
    for idx, subfolder in enumerate(subfolders):
        subfolder_path = os.path.join(input_folder, subfolder)
        rti_folder = find_rti_folder(subfolder_path)
        if rti_folder is None:
            print(f"No 'rti' folder found in {subfolder_path}")
            continue
        # Now, get the required files
        albedo_src = os.path.join(rti_folder, 'albedo.png')
        mask_src = os.path.join(rti_folder, 'mask.png')
        normal_src = os.path.join(rti_folder, 'normal_map.png')
        # Prepare destination filenames
        idx_str = f"{idx:03d}.png"  # zero-padded index
        albedo_dst = os.path.join(albedo_folder, idx_str)
        mask_dst = os.path.join(mask_folder, idx_str)
        normal_dst = os.path.join(normal_folder, idx_str)
        # Copy the files
        try:
            shutil.copyfile(albedo_src, albedo_dst)
            print(f"Copied albedo.png to {albedo_dst}")
        except FileNotFoundError:
            print(f"albedo.png not found in {rti_folder}")
        try:
            shutil.copyfile(mask_src, mask_dst)
            print(f"Copied mask.png to {mask_dst}")
        except FileNotFoundError:
            print(f"mask.png not found in {rti_folder}")
        try:
            shutil.copyfile(normal_src, normal_dst)
            print(f"Copied normal_map.png to {normal_dst}")
        except FileNotFoundError:
            print(f"normal_map.png not found in {rti_folder}")
        # Copy the .lp file from the first folder
        if not lp_copied:
            # Find the .lp file in the rti folder
            lp_files = [f for f in os.listdir(rti_folder) if f.lower().endswith('.lp')]
            if lp_files:
                lp_src = os.path.join(rti_folder, lp_files[0])
                lp_dst = os.path.join(output_folder, lp_files[0])
                try:
                    shutil.copyfile(lp_src, lp_dst)
                    print(f"Copied {lp_files[0]} to {lp_dst}")
                    lp_copied = True  # Only copy once
                except Exception as e:
                    print(f"Failed to copy {lp_files[0]}: {e}")
            else:
                print(f"No .lp file found in {rti_folder}")
    if not lp_copied:
        print("No .lp file was copied since none was found in any 'rti' folder.")

if __name__ == '__main__':
    main()
