import sunpy.map
import matplotlib.pyplot as plt
import os

folder = "sunspot_images_hmi"
file_name = os.listdir(folder)[0]
file_path = os.path.join(folder, file_name)

hmi_map = sunpy.map.Map(file_path)

plt.figure(figsize=(8, 8))
hmi_map.plot()
plt.colorbar(label="Intensity")
plt.show()
