import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_water_usage_chart(data):
    """Create interactive water usage chart"""
    # Prepare data for sector comparison
    sector_data = pd.DataFrame({
        'Sector': ['Residential', 'Agricultural', 'Industrial'],
        'Water Usage (L/hour)': [
            data['residential_water'].mean(),
            data['agricultural_water'].mean(),
            data['industrial_water'].mean()
        ]
    })
    
    fig = px.bar(
        sector_data,
        x='Sector',
        y='Water Usage (L/hour)',
        title='Average Water Usage by Sector',
        color='Sector',
        color_discrete_map={
            'Residential': '#3B82F6',
            'Agricultural': '#10B981',
            'Industrial': '#8B5CF6'
        },
        text='Water Usage (L/hour)'
    )
    
    fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    fig.update_layout(
        yaxis_title='Liters per Hour',
        showlegend=False,
        plot_bgcolor='rgba(240, 249, 255, 0.8)'
    )
    
    return fig

def create_temperature_chart(data):
    """Create temperature trend chart"""
    # Sample last 24 hours
    recent_data = data.tail(24).copy()
    
    fig = px.line(
        recent_data,
        x='timestamp',
        y='temperature',
        title='Temperature Trend (Last 24 Hours)',
        markers=True
    )
    
    # Add threshold lines
    fig.add_hline(y=40, line_dash="dash", line_color="red", 
                  annotation_text="Heat Alert Threshold", 
                  annotation_position="bottom right")
    fig.add_hline(y=35, line_dash="dot", line_color="orange",
                  annotation_text="Comfort Threshold",
                  annotation_position="top right")
    
    fig.update_layout(
        yaxis_title='Temperature (°C)',
        xaxis_title='Time',
        hovermode='x unified'
    )
    
    return fig

def create_energy_chart(data):
    """Create energy usage vs solar power chart"""
    # Sample data
    sample_data = data.tail(12).copy()
    
    fig = go.Figure()
    
    # Add energy consumption bars
    fig.add_trace(go.Bar(
        x=sample_data['timestamp'],
        y=sample_data['energy_consumption'],
        name='Energy Consumption',
        marker_color='#EF4444',
        opacity=0.7
    ))
    
    # Add solar power line
    fig.add_trace(go.Scatter(
        x=sample_data['timestamp'],
        y=sample_data['solar_power'],
        name='Solar Power Available',
        line=dict(color='#F59E0B', width=3),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title='Energy Consumption vs Solar Availability',
        yaxis=dict(title='Energy Consumption (MW)'),
        yaxis2=dict(
            title='Solar Power (MW)',
            overlaying='y',
            side='right'
        ),
        barmode='group',
        hovermode='x unified'
    )
    
    return fig

def create_savings_chart():
    """Create savings comparison chart"""
    savings_data = pd.DataFrame({
        'Metric': ['Water Efficiency', 'Energy Savings', 'Cost Reduction', 'CO₂ Reduction'],
        'Business as Usual': [65, 0, 0, 0],
        'UWHIS Activated': [88, 27, 37, 45]
    })
    
    fig = go.Figure()
    
    # Add traces for both scenarios
    fig.add_trace(go.Bar(
        name='Business as Usual',
        x=savings_data['Metric'],
        y=savings_data['Business as Usual'],
        marker_color='#EF4444',
        text=savings_data['Business as Usual'],
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        name='UWHIS Activated',
        x=savings_data['Metric'],
        y=savings_data['UWHIS Activated'],
        marker_color='#10B981',
        text=savings_data['UWHIS Activated'],
        textposition='auto'
    ))
    
    fig.update_layout(
        title='Performance Comparison: UWHIS vs Baseline',
        yaxis_title='Percentage/Value',
        barmode='group',
        plot_bgcolor='rgba(240, 249, 255, 0.8)'
    )
    
    return fig

def create_demand_prediction_chart():
    """Create water demand prediction chart"""
    # Simulate prediction data
    hours = list(range(24))
    predicted = [800 + 50 * np.sin(h/24 * 2*np.pi) + np.random.normal(0, 20) for h in hours]
    actual = [p + np.random.normal(0, 30) for p in predicted]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=hours,
        y=predicted,
        mode='lines+markers',
        name='AI Prediction',
        line=dict(color='#3B82F6', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=hours,
        y=actual,
        mode='lines',
        name='Actual Demand',
        line=dict(color='#10B981', width=2, dash='dot')
    ))
    
    # Fill between lines
    fig.add_trace(go.Scatter(
        x=hours + hours[::-1],
        y=predicted + actual[::-1],
        fill='toself',
        fillcolor='rgba(59, 130, 246, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Prediction Range'
    ))
    
    fig.update_layout(
        title='24-Hour Water Demand Forecast',
        xaxis_title='Hour of Day',
        yaxis_title='Water Demand (L/hour)',
        hovermode='x unified'
    )
    
    return fig

# Test the functions
if __name__ == "__main__":
    print("📊 Testing chart creation...")
    
    # Create test data
    test_data = pd.DataFrame({
        'timestamp': pd.date_range('2024-01-15', periods=100, freq='H'),
        'residential_water': np.random.normal(500, 50, 100),
        'agricultural_water': np.random.normal(800, 100, 100),
        'industrial_water': np.random.normal(300, 30, 100),
        'temperature': np.random.normal(38, 3, 100),
        'energy_consumption': np.random.normal(700, 50, 100),
        'solar_power': np.random.normal(400, 100, 100)
    })
    
    # Test each chart
    water_chart = create_water_usage_chart(test_data)
    temp_chart = create_temperature_chart(test_data)
    energy_chart = create_energy_chart(test_data)
    savings_chart = create_savings_chart()
    
    print("✅ All charts created successfully!")
    print(f"Water chart type: {type(water_chart)}")
    print(f"Temperature chart type: {type(temp_chart)}")