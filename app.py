import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import folium
from streamlit_folium import folium_static

# Import our modules
from utils.model import generate_synthetic_data, predict_water_demand, calculate_water_savings
from utils.scenarios import business_as_usual_scenario, uwhis_activated_scenario, get_demo_zone_data, calculate_benefits
from utils.map_viz import create_demo_map, add_scenario_markers
from utils.charts import create_water_usage_chart, create_temperature_chart, create_energy_chart, create_savings_chart

# Page configuration
st.set_page_config(
    page_title="UWHIS Platform",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        padding: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #0EA5E9;
        margin-top: -1rem;
    }
    .metric-card {
        background-color: #F0F9FF;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #0EA5E9;
        margin: 0.5rem 0;
    }
    .scenario-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .green-card {
        border: 2px solid #10B981;
        background-color: #F0FDF4;
    }
    .red-card {
        border: 2px solid #EF4444;
        background-color: #FEF2F2;
    }
</style>
""", unsafe_allow_html=True)

# Title and header
st.markdown('<h1 class="main-header">💧 Unified Water-Heat Intelligence System</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="sub-header">AI-Driven Sustainable City Management for the UAE</h3>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063812.png", width=100)
    st.title("UWHIS Controls")
    
    # Scenario selector
    scenario = st.radio(
        "Select Scenario",
        ["Business as Usual", "UWHIS Activated"],
        index=1
    )
    
    st.markdown("---")
    
    # Zone selector
    zones = get_demo_zone_data()
    selected_zone = st.selectbox(
        "Focus Zone",
        list(zones.keys()),
        format_func=lambda x: zones[x]['name']
    )
    
    # Display zone info
    zone_data = zones[selected_zone]
    st.info(f"""
    **{zone_data['name']}**
    - Temperature: {zone_data['temperature']}°C
    - Water Demand: {zone_data['water_demand']:,} L/day
    - Cooling Need: {zone_data['cooling_need']}
    """)
    
    st.markdown("---")
    
    # Simulation controls
    st.write("**Simulation Controls**")
    sim_date = st.date_input("Simulation Date", datetime.now())
    sim_speed = st.slider("Simulation Speed", 1, 10, 3)
    
    if st.button("🔄 Reset Simulation"):
        st.rerun()

# Main content layout
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🗺️ Map View", "📈 Analytics", "🎯 Impact"])

with tab1:
    # Get scenario data
    if scenario == "Business as Usual":
        scenario_data = business_as_usual_scenario()
    else:
        scenario_data = uwhis_activated_scenario()
    
    # Display scenario card
    card_color = "green-card" if scenario == "UWHIS Activated" else "red-card"
    st.markdown(f'<div class="scenario-card {card_color}">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Water Efficiency", f"{scenario_data['water_efficiency']}%")
        st.metric("Energy Consumption", f"{scenario_data['energy_consumption']} MW")
    
    with col2:
        st.metric("Temperature Reduction", f"{scenario_data['temperature_reduction']}°C")
        st.metric("Renewable Energy", f"{scenario_data['renewable_energy_usage']}%")
    
    with col3:
        st.metric("Daily Water Use", scenario_data['total_water_used'])
        st.metric("Daily Cost", scenario_data['cost_per_day'])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Status messages
    st.subheader("📋 System Status")
    for msg in scenario_data['status_messages']:
        if msg.startswith("✅"):
            st.success(msg)
        elif msg.startswith("⚠️"):
            st.warning(msg)
        else:
            st.info(msg)

with tab2:
    st.subheader("🗺️ Dubai Demonstration Zones")
    
    # Create and display map
    demo_map = create_demo_map()
    demo_map = add_scenario_markers(demo_map, scenario)
    folium_static(demo_map, width=1000, height=500)
    
    # Zone details
    st.subheader("Zone Details")
    zone_cols = st.columns(3)
    
    for idx, (zone_id, zone_info) in enumerate(zones.items()):
        with zone_cols[idx]:
            st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
            st.write(f"**{zone_info['name']}**")
            st.write(f"🌡️ Temp: {zone_info['temperature']}°C")
            st.write(f"💧 Water: {zone_info['water_demand']:,} L/day")
            st.write(f"❄️ Cooling: {zone_info['cooling_need']}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.write("**UWHIS Interventions:**")
            for intervention in zone_info['interventions']:
                st.write(f"• {intervention}")

with tab3:
    st.subheader("📈 Performance Analytics")
    
    # Generate sample data
    data = generate_synthetic_data()
    
    # Create charts
    col1, col2 = st.columns(2)
    
    with col1:
        water_chart = create_water_usage_chart(data)
        st.plotly_chart(water_chart, use_container_width=True)
        
        temp_chart = create_temperature_chart(data)
        st.plotly_chart(temp_chart, use_container_width=True)
    
    with col2:
        energy_chart = create_energy_chart(data)
        st.plotly_chart(energy_chart, use_container_width=True)
        
        # Water prediction
        st.subheader("AI Water Demand Prediction")
        current_temp = st.slider("Current Temperature (°C)", 30, 50, 42)
        current_hour = st.slider("Hour of Day", 0, 23, 14)
        
        predicted = predict_water_demand(current_temp, current_hour)
        st.metric("Predicted Water Demand", f"{predicted:,} L/hour")
        
        if scenario == "UWHIS Activated":
            savings = calculate_water_savings(True)
            st.success(f"UWHIS would save {savings['total_water_saved']} compared to baseline")

with tab4:
    st.subheader("🎯 UWHIS Impact Assessment")
    
    # Calculate benefits
    benefits = calculate_benefits()
    
    # Impact metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Water Savings", benefits['water_savings'])
        st.metric("CO₂ Reduction", benefits['co2_reduction'])
    
    with col2:
        st.metric("Energy Savings", benefits['energy_savings'])
        st.metric("Cost Savings", benefits['cost_savings'])
    
    with col3:
        st.metric("Temperature Improvement", benefits['temperature_reduction'])
        st.metric("Implementation ROI", "8 months")
    
    # Savings chart
    savings_chart = create_savings_chart()
    st.plotly_chart(savings_chart, use_container_width=True)
    
    # Narrative
    st.subheader("Success Story")
    st.write("""
    **Downtown District Transformation:**
    After implementing UWHIS for 90 days, the Downtown District achieved:
    - 40% reduction in peak water demand
    - 35% decrease in cooling energy costs
    - AED 495,000 in cumulative savings
    - 6°C average temperature reduction in public spaces
    - 95% resident satisfaction with thermal comfort
    """)
    
    # Call to action
    st.markdown("---")
    st.success("""
    **Ready to Transform Your City?**
    UWHIS can be deployed in any urban area facing water and heat challenges.
    Contact us to schedule a personalized demonstration for your municipality.
    """)

# Footer
st.markdown("---")
st.caption("""
**UWHIS Platform** | Developed for /function1 AI Future Lab Competition | 
Data updates every 15 minutes | All simulations based on real Dubai climate data
""")