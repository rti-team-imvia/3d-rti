import os
import cv2
from rti import compute_normals
import matplotlib.pyplot as plt
import math
from utils import params, utils
import numpy as np

class Acq:
    def __init__(self, path, lp_file = None):
        self.path = path
        self.lp_file = lp_file
        self.lp_positions = []
        self.image_paths = []
        self.image_names = []
        self.image_width = None
        self.image_height = None
        self.image_channels = None
        self.lps_cartesian = []
        self.lps_spherical = []
        self.normals = None
        self.normal_map_img = None

        self.load_image_paths_from_acq_path()
        self.compute_pxl_wise_light_directions_and_distances()
        if params.COMPUTE_AND_SAVE_NORMALS:
            self.compute_and_save_normals()
        
    def load_image_paths_from_acq_path(self):
         
        if self.lp_file is None:
            # Check if the path has a lp file
            for root, dirs, files in os.walk(self.path):
                for f in files:
                    if f.endswith(".lp"):
                        self.lp_file = os.path.join(root, f)

            print("No .lp file found in the path: ", self.path)
            return
        
        with open(self.lp_file, 'r') as f:
            lines = f.readlines()
            try:
                num_lights = int(lines[0].strip())
            except ValueError:
                print(f"First line of {self.lp_file} is not an integer.")
                return

            if len(lines[1:]) != num_lights:
                print(f"Number of light positions in {self.lp_file} does not match the number indicated.")
                return

            current_lp_positions = set()
            acq_image_files = []  # List to store image files for this acquisition
            for line in lines[1:]:
                parts = line.split()
                if len(parts) != 4:
                    print(f"Line in {self.lp_file} does not contain exactly four parts: {line}")
                    return

                img_file, x, y, z = parts
                try:
                    x = float(x)
                    y = float(y)
                    z = float(z)
                    self.lps_cartesian.append((x, y, z))
                    self.lps_spherical.append(utils.Cartesian2spherical3D(x, y, z))
                except ValueError:
                    print(f"Coordinates in {self.lp_file} are not valid numbers: {line}")
                    return

                current_lp_positions.add((x, y, z))
                img_path = os.path.join(self.path, img_file)

                if not os.path.exists(img_path):
                    print(f"Image file {img_file} listed in {self.lp_file} does not exist.")
                    return 
                else:
                    self.image_paths.append(img_path)
                    self.image_names.append(img_file)

            self.image_width, self.image_height, self.image_channels = cv2.imread(self.image_paths[0]).shape
            self.lp_positions = list(current_lp_positions)

    # Compute and save the normal maps    
    def compute_and_save_normals(self):
        # Create PhotometricStereo instance
        ps = compute_normals.PhotometricStereo_traditional(self.image_paths, self.lps_cartesian)
        # Compute normals
        self.normals = ps.estimate_normals_and_albedo()
        print("Normals computed successfully.")
        # Get the directory of the first image
        img_dir = os.path.dirname(self.image_paths[0])
        # Save normal map image in the image directory
        ps.save_results(img_dir)
        print("Finished computing and saving normal maps.")

    def compute_pxl_wise_light_directions_and_distances(self):
        img_shape = (self.image_height, self.image_width)
        distance_matrices = []
        angles_matrices = []
        for i in range(len(self.image_paths)):
            center_distance = np.linalg.norm(np.array(self.lp_positions[i]))
            h, w = img_shape
            surface_width, surface_height = params.SURFACE_PHYSCIAL_SIZE
            x = np.linspace(-surface_width / 2, surface_width / 2, w)
            y = np.linspace(-surface_height / 2, surface_height / 2, h)
            X, Y = np.meshgrid(y, x)
            Z = np.zeros_like(X)        
            distances = np.sqrt((X - self.lp_positions[i][0])**2 + (Y - self.lp_positions[i][1])**2 + (Z - self.lp_positions[i][2])**2)
            # Ensure that the angle calculation is safe for arccos
            cos_theta = np.clip(-self.lp_positions[i][2] / distances, -1.0, 1.0)
            angles = np.arccos(cos_theta)
            distance_matrices.append(distances)
            angles_matrices.append(angles)
        
        np.save(os.path.join(self.path, "distance_matrices.npy"), np.array(distance_matrices))
        np.save(os.path.join(self.path, "angles_matrices.npy"), np.array(angles_matrices))

    # Plot and save 3D scatter plot of the light positions
    def plot_and_save_3d_scatter(self):
        x = [lp[0] for lp in self.lps_cartesian]
        y = [lp[1] for lp in self.lps_cartesian]
        z = [lp[2] for lp in self.lps_cartesian]
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.savefig(os.path.join(self.path, f"lps_3d_scatter.png"))
        plt.close()

    # Plot and save 2D projection of the light positions    
    def plot_and_save_2d_projection(self):
        x = [lp[0] for lp in self.lps_cartesian]
        y = [lp[1] for lp in self.lps_cartesian]
        
        plt.figure()
        plt.scatter(x, y)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.savefig(os.path.join(self.path, "lps_2d_projection.png"))
        plt.close()

    

    