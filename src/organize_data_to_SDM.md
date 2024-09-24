# Organize_data_to_SDM

## Introduction:

The purpose of this script is to automate the process of selecting and renaming images from RTI (Reflectance Transformation Imaging) acquisitions, which is necessary for creating normal maps and reflectance maps. These maps are required to use the repository [RNb-NeuS](https://github.com/bbrument/RNb-NeuS/).

In order to generate these normal and reflectance maps, we use another repository called [SDM-UniPS-CVPR2023](https://github.com/rti-team-imvia/SDM-UniPS-CVPR2023-fork/tree/main). This repository requires exactly 10 input images from each RTI acquisition, and the images need to be renamed in a specific format. The current script facilitates this by selecting 10 equally spaced images from the RTI acquisitions, renaming them appropriately, and organizing them in the required format.

This script simplifies the preprocessing step by ensuring the correct image selection and renaming before using the SDM-UniPS-CVPR2023 repository for creating the maps.

## How the Script Works:

1. **Input Folder**: 
   - Takes a main input folder containing subfolders representing different RTI experiments. 
   - Example: `C:\Users\Deivid\Documents\rti-data\Palermo_3D\real acquisitions\head_cs`

2. **Processing Each Subfolder**:
   - For each experiment subfolder (e.g., `2024_07_02_HEAD_CS_00`):
     - **Step 2.1**: Recursively searches for a subfolder named `rti`, where the necessary images are stored.
     - **Step 2.2**: Within the `rti` folder, identifies all the images with the extension `.JPG` and sorts them in ascending order based on their file names.
     - **Step 2.3**: Selects 10 equally spaced images from the sorted list. For example, if there are 40 images, it selects every 4th image (`40/10 = 4`), resulting in a total of 10 images.
     - **Step 2.4**: The selected images are copied into a new folder named `SDM_in` that is created at the same level as the `rti` folder (i.e., inside the same parent folder). These images are renamed in order as: 
       - `L (1).JPG`
       - `L (2).JPG`
       - ...
       - `L (10).JPG`

3. **Repeat for All Subfolders**:
   - The script repeats this process for every experiment subfolder it encounters in the main input folder.

## Input:

- The main input folder containing RTI acquisition subfolders (e.g., `C:\Users\Deivid\Documents\rti-data\Palermo_3D\real acquisitions\head_cs`).

## Output:

- For each experiment, a new folder named `SDM_in` is created inside the parent folder of the `rti` folder. 
- This `SDM_in` folder contains 10 selected images renamed as `L (1).JPG`, `L (2).JPG`, ..., `L (10).JPG`.

