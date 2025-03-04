import streamlit as st
import plotly.express as px
from datetime import datetime

# Conversion formulas
def convert_units(value, from_unit, to_unit, category):
    conversions = {
        'Area': {'m²': 1, 'km²': 0.000001, 'cm²': 10000, 'mm²': 1000000, 'ft²': 10.7639, 'in²': 1550, 'acre': 0.000247105, 'hectare': 0.0001},
        'Data Transfer Rate': {'bps': 1, 'Kbps': 0.001, 'Mbps': 0.000001, 'Gbps': 0.000000001, 'Tbps': 0.000000000001},
        'Digital Storage': {'B': 1, 'KB': 0.001, 'MB': 0.000001, 'GB': 0.000000001, 'TB': 0.000000000001, 'PB': 0.000000000000001},
        'Energy': {'J': 1, 'kJ': 0.001, 'cal': 0.239006, 'kcal': 0.000239006, 'Wh': 0.000277778, 'BTU': 0.000947817},
        'Frequency': {'Hz': 1, 'kHz': 0.001, 'MHz': 0.000001, 'GHz': 0.000000001, 'THz': 0.000000000001},
        'Fuel Economy': {'km/L': 1, 'mpg': 2.35215, 'L/100km': 100},
        'Length': {'m': 1, 'cm': 100, 'mm': 1000, 'km': 0.001, 'inch': 39.3701, 'ft': 3.28084, 'yard': 1.09361, 'mile': 0.000621371},
        'Mass': {'kg': 1, 'g': 1000, 'mg': 1000000, 'lb': 2.20462, 'oz': 35.274, 'ton': 0.001, 'metric_ton': 0.001},
        'Plane Angle': {'degree': 1, 'radian': 0.0174533, 'grad': 1.11111},
        'Pressure': {'Pa': 1, 'kPa': 0.001, 'bar': 0.00001, 'psi': 0.000145038, 'atm': 0.00000986923},
        'Speed': {'m/s': 1, 'km/h': 3.6, 'mph': 2.23694, 'knot': 1.94384},
        'Temperature': {'C': lambda x: x, 'F': lambda x: (x * 9/5) + 32, 'K': lambda x: x + 273.15},
        'Time': {'s': 1, 'min': 1/60, 'h': 1/3600, 'day': 1/86400, 'week': 1/604800, 'month': 1/2592000, 'year': 1/31536000},
        'Volume': {'L': 1, 'mL': 1000, 'cm³': 1000, 'm³': 0.001, 'ft³': 0.0353147, 'gal': 0.264172, 'qt': 1.05669},
    }

    units = conversions.get(category, {})
    if from_unit in units and to_unit in units:
        if callable(units[from_unit]):
            value_in_base = units[from_unit](value)
        else:
            value_in_base = value / units[from_unit]
        
        if callable(units[to_unit]):
            return units[to_unit](value_in_base)
        return value_in_base * units[to_unit]
    return None

# Streamlit UI with enhanced styling
st.set_page_config(page_title="Enhanced Unit Converter", layout="wide")
st.title('📐 Unit Converter')
st.write('Convert units instantly with enhanced visualization!')

# Category selection with improved UI
st.header('🔄 Select a Conversion Category')
categories = [
    'Area', 'Data Transfer Rate', 'Digital Storage', 'Energy', 'Frequency',
    'Fuel Economy', 'Length', 'Mass', 'Plane Angle', 'Pressure', 'Speed',
    'Temperature', 'Time', 'Volume'
]
category = st.selectbox('Category:', categories)

# Enhanced units based on selected category
units = {
    'Area': ['m²', 'km²', 'cm²', 'mm²', 'ft²', 'in²', 'acre', 'hectare'],
    'Data Transfer Rate': ['bps', 'Kbps', 'Mbps', 'Gbps', 'Tbps'],
    'Digital Storage': ['B', 'KB', 'MB', 'GB', 'TB', 'PB'],
    'Energy': ['J', 'kJ', 'cal', 'kcal', 'Wh', 'BTU'],
    'Frequency': ['Hz', 'kHz', 'MHz', 'GHz', 'THz'],
    'Fuel Economy': ['km/L', 'mpg', 'L/100km'],
    'Length': ['m', 'cm', 'mm', 'km', 'inch', 'ft', 'yard', 'mile'],
    'Mass': ['kg', 'g', 'mg', 'lb', 'oz', 'ton', 'metric_ton'],
    'Plane Angle': ['degree', 'radian', 'grad'],
    'Pressure': ['Pa', 'kPa', 'bar', 'psi', 'atm'],
    'Speed': ['m/s', 'km/h', 'mph', 'knot'],
    'Temperature': ['C', 'F', 'K'],
    'Time': ['s', 'min', 'h', 'day', 'week', 'month', 'year'],
    'Volume': ['L', 'mL', 'cm³', 'm³', 'ft³', 'gal', 'qt'],
}

col1, col2 = st.columns(2)
with col1:
    st.subheader('From')
    from_unit = st.selectbox('Source Unit:', units[category])
    value = st.number_input('Enter Value:', min_value=0.0, format="%.8f")

with col2:
    st.subheader('To')
    to_unit = st.selectbox('Target Unit:', units[category])

# Convert and show result with enhanced visualization
if st.button('Convert 🔄'):
    result = convert_units(value, from_unit, to_unit, category)
    if result is not None:
        st.success(f"🎯 {value} {from_unit} = {result:.8f} {to_unit}")

        # Enhanced visualization
        data = {'Units': [from_unit, to_unit], 'Values': [value, result]}
        fig = px.bar(data, x='Units', y='Values', color='Units', 
                    title='Conversion Comparison',
                    template='plotly_dark',
                    labels={'Values': 'Value', 'Units': 'Unit Type'})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        # Store history with timestamp
        if 'history' not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append((datetime.now().strftime('%Y-%m-%d %H:%M:%S'), value, from_unit, result, to_unit))

# Show enhanced history
if 'history' in st.session_state and st.session_state.history:
    st.header('📜 Recent Conversions')
    for record in reversed(st.session_state.history[-5:]):
        st.write(f"🕒 {record[0]}: {record[1]} {record[2]} ➡️ {record[3]:.8f} {record[4]}")