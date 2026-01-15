import folium
from folium import plugins
import numpy as np

def create_demo_map():
    """Create an interactive map of Dubai demonstration zones"""
    # Dubai coordinates
    dubai_center = [25.2048, 55.2708]
    
    # Create base map
    demo_map = folium.Map(
        location=dubai_center,
        zoom_start=12,
        tiles='cartodbpositron',
        width='100%',
        height='100%'
    )
    
    # Add scale
    folium.plugins.MeasureControl().add_to(demo_map)
    
    # Add fullscreen button
    folium.plugins.Fullscreen().add_to(demo_map)
    
    return demo_map

def add_scenario_markers(base_map, scenario="UWHIS Activated"):
    """Add markers based on scenario"""
    
    # Define zones with their data
    zones = {
        'downtown': {
            'coords': [25.1972, 55.2744],
            'name': 'Downtown District',
            'temp': 42.5 if scenario == "Business as Usual" else 36.5,
            'water_usage': 450000,
            'color': 'red' if scenario == "Business as Usual" else 'green'
        },
        'agricultural': {
            'coords': [25.1150, 55.3800],
            'name': 'Agricultural Zone A',
            'temp': 38.0,
            'water_usage': 800000,
            'color': 'orange' if scenario == "Business as Usual" else 'blue'
        },
        'residential': {
            'coords': [25.2350, 55.2900],
            'name': 'Residential Complex',
            'temp': 40.0 if scenario == "Business as Usual" else 34.0,
            'water_usage': 350000,
            'color': 'red' if scenario == "Business as Usual" else 'green'
        },
        'industrial': {
            'coords': [25.1500, 55.2500],
            'name': 'Industrial Park',
            'temp': 41.0,
            'water_usage': 300000,
            'color': 'orange'
        }
    }
    
    # Add zone markers
    for zone_id, zone_data in zones.items():
        # Create popup content
        popup_html = f"""
        <div style="width: 250px">
            <h4>{zone_data['name']}</h4>
            <hr>
            <p><b>Temperature:</b> {zone_data['temp']}°C</p>
            <p><b>Water Usage:</b> {zone_data['water_usage']:,} L/day</p>
            <p><b>Scenario:</b> {scenario}</p>
            <p><b>Status:</b> {'Optimized' if zone_data['color'] in ['green', 'blue'] else 'Needs Attention'}</p>
        </div>
        """
        
        # Add marker
        folium.Marker(
            location=zone_data['coords'],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{zone_data['name']} - Click for details",
            icon=folium.Icon(
                color=zone_data['color'],
                icon='tint' if 'water' in zone_id else 'building' if 'downtown' in zone_id else 'home' if 'residential' in zone_id else 'industry',
                prefix='fa'
            )
        ).add_to(base_map)
        
        # Add circle for temperature visualization
        folium.Circle(
            location=zone_data['coords'],
            radius=zone_data['water_usage'] / 100,  # Scale for visibility
            color=zone_data['color'],
            fill=True,
            fill_opacity=0.2,
            popup=f"Water footprint: {zone_data['water_usage']:,} L/day"
        ).add_to(base_map)
    
    # Add heatmap layer for temperature
    heat_data = [[zone['coords'][0], zone['coords'][1], zone['temp']] for zone in zones.values()]
    plugins.HeatMap(heat_data, radius=25, blur=15, max_zoom=1).add_to(base_map)
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 180px; height: 150px; 
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color:white;
                padding: 10px;
                border-radius: 5px;">
    <p><strong>Map Legend</strong></p>
    <p><i class="fa fa-circle" style="color:green"></i> Optimized Zone</p>
    <p><i class="fa fa-circle" style="color:blue"></i> Agricultural Zone</p>
    <p><i class="fa fa-circle" style="color:orange"></i> Monitoring Zone</p>
    <p><i class="fa fa-circle" style="color:red"></i> Attention Needed</p>
    <p>Circle size = Water usage</p>
    </div>
    '''
    
    base_map.get_root().html.add_child(folium.Element(legend_html))
    
    return base_map

def create_temperature_heatmap():
    """Create a dedicated temperature heatmap"""
    # This could be enhanced with real temperature data
    dubai_map = folium.Map([25.2048, 55.2708], zoom_start=11)
    
    # Simulate temperature grid
    temperature_points = []
    for lat in np.linspace(25.10, 25.30, 10):
        for lon in np.linspace(55.20, 55.40, 10):
            # Simulate urban heat island effect (hotter in center)
            center_dist = np.sqrt((lat-25.2048)**2 + (lon-55.2708)**2)
            temp = 42 - center_dist * 100  # Hotter in center
            temperature_points.append([lat, lon, temp])
    
    plugins.HeatMap(temperature_points, radius=20, blur=15).add_to(dubai_map)
    
    return dubai_map

# Test the functions
if __name__ == "__main__":
    print("🗺️ Testing map visualization...")
    test_map = create_demo_map()
    test_map = add_scenario_markers(test_map, "UWHIS Activated")
    test_map.save('test_map.html')
    print("✅ Map created successfully! Saved as test_map.html")