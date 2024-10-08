import os
import re
import argparse
from natsort import natsorted
from pathlib import Path

def find_rti_folders(root_path):
    rti_folders = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        if 'rti' in dirnames:
            rti_folder = os.path.join(dirpath, 'rti')
            rti_folders.append(rti_folder)
            # Prevent descending into 'rti' subdirectories
            dirnames.remove('rti')
    return rti_folders

def natural_sort(l):
    """Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def process_lp_file(rti_folder):
    # Step 4: Get all .JPG images and sort them naturally
    jpg_images = [f for f in os.listdir(rti_folder) if f.lower().endswith('.jpg')]
    jpg_images = natural_sort(jpg_images)

    # Step 5: Find the .lp file
    lp_files = [f for f in os.listdir(rti_folder) if f.lower().endswith('.lp')]
    if not lp_files:
        print(f"No .lp file found in {rti_folder}")
        return
    if len(lp_files) > 1:
        print(f"Multiple .lp files found in {rti_folder}, using the first one.")
    lp_file = os.path.join(rti_folder, lp_files[0])

    # Read the .lp file
    with open(lp_file, 'r') as f:
        lines = f.readlines()

    # Ignore the first line
    first_line = lines[0]
    lines_to_process = lines[1:]

    # Process each line
    modified_lines = []
    for line in lines_to_process:
        # Split the line into columns
        columns = line.strip().split()
        if not columns:
            modified_lines.append(line)
            continue  # Skip empty lines
        image_name = columns[0]
        # Check if the image exists in jpg_images
        if image_name in jpg_images:
            # Image exists, keep the line as is
            modified_lines.append(line)
        else:
            # Image does not exist, find the closest image name
            # Extract numerical part from image_name
            num_in_name = re.findall(r'\d+', image_name)
            if num_in_name:
                num_in_name = num_in_name[0]
                # Try to find an image in jpg_images with the same number
                matching_images = [img for img in jpg_images if num_in_name in img]
                if matching_images:
                    # Use the first matching image
                    new_image_name = matching_images[0]
                    print(f"Replacing {image_name} with {new_image_name} in {lp_file}")
                    columns[0] = new_image_name
                    # Reconstruct the line
                    modified_line = ' '.join(columns) + '\n'
                    modified_lines.append(modified_line)
                else:
                    print(f"No matching image found for {image_name} in {rti_folder}")
                    modified_lines.append(line)
            else:
                print(f"No number found in {image_name}, cannot find a matching image.")
                modified_lines.append(line)

    # Write back the modified .lp file
    with open(lp_file, 'w') as f:
        f.write(first_line)
        f.writelines(modified_lines)

def main():
    print('================================================================')
    print('                     Running modify_lp_files.py                 ')
    print('================================================================') 

    # Step 1: Parse the argument for experiment path
    parser = argparse.ArgumentParser(description='Process RTI folders and modify .lp files.')
    parser.add_argument('--experiment_path', type=Path, required=True, help='Path to the experiment folder')
    args = parser.parse_args()

    experiment_path = args.experiment_path

    if not experiment_path.exists() or not experiment_path.is_dir():
        print(f"Error: The path {experiment_path} does not exist or is not a directory.")
        return

    # Step 2: Get the list of subdirectories and sort them naturally
    subfolders = [f for f in experiment_path.iterdir() if f.is_dir()]
    subfolders = natural_sort([str(f) for f in subfolders])

    # Step 7: Process each subfolder
    for subfolder in subfolders:
        # Step 3: Find 'rti' folders recursively
        rti_folders = find_rti_folders(subfolder)
        for rti_folder in rti_folders:
            print(f"Processing rti folder: {rti_folder}")
            process_lp_file(rti_folder)

if __name__ == "__main__":
    main()

# python src/modify_lp_files.py --experiment_path "C://Users//Deivid//Documents//rti-data//Palermo_3D//real acquisitions//head_cs"