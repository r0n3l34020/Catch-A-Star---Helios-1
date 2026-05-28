import streamlit as st
import pandas as pd
import json
import plotly.express as px
from datetime import datetime

# --- UI Configuration ---
st.set_page_config(
    page_title="Helios-1 Orbital Defense",
    page_icon="🛰️",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #374151; }
    </style>
    """, unsafe_allow_html=True)

# --- Data Loaders ---
def load_data():
    try:
        with open("output/current_threat.json", "r") as f:
            threat = json.load(f)
        df = pd.read_csv("output/sunspot_measurements.csv")
        return threat, df
    except Exception as e:
        st.error(f"Error loading system data: {e}")
        return None, None

threat_data, history_df = load_data()

# --- Dashboard Header ---
st.title("🛰️ Helios-1 | Space Weather Monitoring & Satellite Defense")
st.write(f"**System Status:** Operational | **Last Sync:** {threat_data['timestamp'] if threat_data else 'N/A'}")

if threat_data and history_df is not None:
    
    assessment = threat_data['assessment']
    if assessment['level'] == "CRITICAL":
        st.error(f"🚨 **{assessment['level']} ALERT:** {assessment['action']}")
    elif assessment['level'] == "ELEVATED":
        st.warning(f"⚠️ **{assessment['level']} ALERT:** {assessment['action']}")
    else:
        st.success(f"✅ **SYSTEM NOMINAL:** {assessment['level']}")

    st.markdown("---")

    
    m = threat_data['metrics']
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Effective Area", f"{m['area_earths']} Earths", delta=m['trend'])
    with col2:
        st.metric("Observed Sunspots", m['spots'])
    with col3:
        
        intensity = min(100, (m['area_earths'] * 18) + (m['spots'] * 2.5))
        st.metric("Magnetic Flux Intensity", f"{round(intensity, 1)}%")

    st.markdown("---")

    
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        st.subheader("📈 Historical Photospheric Activity")
        
        fig = px.line(history_df, x='date', y='total_area_km2_approx', 
                      title="Sunspot Area Expansion (km²)",
                      template="plotly_dark",
                      color_discrete_sequence=['#ff4b4b'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with right_col:
        st.subheader("📋 Satellite Telemetry Logs")
        
        st.dataframe(history_df.tail(10)[['date', 'sunspot_count', 'total_area_km2_approx']], 
                     hide_index=True, use_container_width=True)

    
    with st.expander("🛠️ Recommended Preventative Measures"):
        if assessment['level'] == "CRITICAL":
            st.write("- **Satellite Operations:** Deploy magnetic shielding; initiate 'Safe Mode' for LEO assets.")
            st.write("- **Grid Infrastructure:** Monitor GIC (Geomagnetically Induced Currents) in high-latitude transformers.")
            st.write("- **Communications:** Expect HF radio blackouts on the sunlit side of Earth.")
        else:
            st.write("All systems within safety parameters. Continue routine monitoring.")

else:
    st.info("Awaiting system input. Please ensure your analyzer has run successfully.")
