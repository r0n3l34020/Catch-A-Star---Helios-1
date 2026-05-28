from sunpy.net import Fido, attrs as a
from astropy import units as u

# --- CONFIGURATION ---
START_DATE = "2024-10-01"
END_DATE = "2024-11-01" 

print(f"🚀 Initializing download for Solar Maximum Peak: {START_DATE} to {END_DATE}")

results = Fido.search(
    a.Time(START_DATE, END_DATE),
    a.Instrument.hmi,
    a.Physobs.intensity, 
    a.Sample(24 * u.h)                 
)

print(f"🔍 Found {len(results)} high-activity images.")

if results:
    files = Fido.fetch(results[0:35], path="sunspot_images_hmi/{file}.fits")
    print("✅ Success! This dataset has been officially beefed up.")
else:
    print("❌ No images found for this period. Check your internet connection!")
