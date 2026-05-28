import os
import glob
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt

import astropy.units as u
from sunpy.map import Map

INPUT_FOLDER = "sunspot_images_hmi"
OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

rows = []
fits_files = sorted(glob.glob(os.path.join(INPUT_FOLDER, "*.fits")))

for file in fits_files:
    m = Map(file)
    img = np.nan_to_num(m.data.astype(float))

    cx = m.reference_pixel.x.value
    cy = m.reference_pixel.y.value
    radius_px = (m.rsun_obs / m.scale[0]).value

    yy, xx = np.indices(img.shape)
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    disk_mask = dist <= (0.95 * radius_px)   

    disk_values = img[disk_mask]
    median_val = np.median(disk_values)

    spot_threshold = 0.65 * median_val
    mask = (img < spot_threshold) & disk_mask
    mask_u8 = (mask * 255).astype(np.uint8)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask_u8 = cv2.morphologyEx(mask_u8, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(mask_u8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    km_per_arcsec = (m.dsun * np.tan(1 * u.arcsec)).to(u.km).value
    km_per_pixel = (abs(m.scale[0].value) * km_per_arcsec)

    total_area_km2 = 0
    kept_spots = 0

    norm_display = np.clip((img - np.percentile(disk_values, 1)) / (median_val - np.percentile(disk_values, 1)), 0, 1)
    overlay = cv2.cvtColor((255 * norm_display).astype(np.uint8), cv2.COLOR_GRAY2RGB)

    for c in contours:
        area_px = cv2.contourArea(c)
        if area_px < 5:
            continue

        M = cv2.moments(c)
        if M["m00"] == 0: continue
        
        scx, scy = M["m10"]/M["m00"], M["m01"]/M["m00"]

        spot_dist = np.sqrt((scx - cx)**2 + (scy - cy)**2)
        mu = np.sqrt(max(0.1, 1 - (spot_dist / radius_px)**2))
        
        area_km2 = (area_px * (km_per_pixel**2)) / mu
        total_area_km2 += area_km2
        kept_spots += 1

        cv2.drawContours(overlay, [c], -1, (0, 255, 0), 2)

    rows.append({
        "file": os.path.basename(file),
        "date": m.date.isot,
        "sunspot_count": kept_spots,
        "total_area_km2_approx": f"{total_area_km2:.2e}"
    })

    out_name = os.path.splitext(os.path.basename(file))[0] + "_fixed.png"
    plt.imsave(os.path.join(OUTPUT_FOLDER, out_name), overlay)

df = pd.DataFrame(rows)
df.to_csv(os.path.join(OUTPUT_FOLDER, "sunspot_measurements.csv"), index=False)
print(df)
