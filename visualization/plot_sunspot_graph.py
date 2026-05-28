import sunpy.map
import matplotlib.pyplot as plt
import os

# Get the path to one of your files
folder = "sunspot_images_hmi"
file_name = os.listdir(folder)[0]  # Grab the first file in the folder
file_path = os.path.join(folder, file_name)

# Create a SunPy Map object
hmi_map = sunpy.map.Map(file_path)

# Plot the image
plt.figure(figsize=(8, 8))
hmi_map.plot()
plt.colorbar(label="Intensity")
plt.show()
