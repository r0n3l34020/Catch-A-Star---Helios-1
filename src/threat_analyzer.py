import pandas as pd
import json
import os
from datetime import datetime

INPUT_CSV = "output/sunspot_measurements.csv"
OUTPUT_JSON = "output/current_threat.json"
EARTH_AREA = 1.27e8 

def get_trend(df):
    if len(df) < 2: return "STABLE"
    last = df.iloc[-1]['total_area_km2_approx']
    prev = df.iloc[-2]['total_area_km2_approx']
    change = (last - prev) / prev
    if change > 0.15: return "📈 INCREASING"
    if change < -0.15: return "📉 DECREASING"
    return "➡️ STABLE"

def calculate_threat_level(area_km2, spot_count, trend):
    area_in_earths = area_km2 / EARTH_AREA
    intensity_score = min(100, (area_in_earths * 18) + (spot_count * 2.5))
    if trend == "📈 INCREASING": intensity_score += 10
    
    if intensity_score > 75:
        return {"level": "CRITICAL", "action": "RED ALERT: Shielding required.", "color": "red"}
    elif intensity_score > 40:
        return {"level": "ELEVATED", "action": "CAUTION: Monitor radio flux.", "color": "orange"}
    return {"level": "NOMINAL", "action": "STATUS GREEN: No orbital action.", "color": "green"}

def generate_report():
    print("🛡️ Analyzing Solar Flux Data...")
    df = pd.read_csv(INPUT_CSV).sort_values('date')
    latest = df.iloc[-1]
    trend = get_trend(df)
    assessment = calculate_threat_level(latest['total_area_km2_approx'], latest['sunspot_count'], trend)
    
    report = {
        "timestamp": datetime.now().strftime("%H:%M IST"),
        "metrics": {
            "area_earths": round(latest['total_area_km2_approx'] / EARTH_AREA, 2),
            "spots": int(latest['sunspot_count']),
            "trend": trend
        },
        "assessment": assessment
    }
    
    with open(OUTPUT_JSON, "w") as f:
        json.dump(report, f, indent=4)
    print(f"✅ Threat Level: {assessment['level']} ({trend})")

if __name__ == "__main__": generate_report()
