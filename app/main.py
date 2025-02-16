import streamlit as st
import pandas as pd
import numpy as np
from model import BioReactorModel
from utils.visualizations import plot_progress, plot_3d_surface

# Load kinetics data to get valid substrate-enzyme mappings
@st.cache_data
def load_kinetics_data():
    return pd.read_csv('data/raw/enzyme_kinetics.csv')

kinetics_data = load_kinetics_data()
substrate_options = kinetics_data['Substrate'].unique().tolist()

st.sidebar.title("Bioreactor Parameters")

# Select substrate and automatically determine enzyme from kinetics data
selected_substrate = st.sidebar.selectbox("Select Substrate", substrate_options)
enzyme_for_substrate = kinetics_data[kinetics_data['Substrate'] == selected_substrate]['Enzyme'].iloc[0]
st.sidebar.markdown(f"**Enzyme:** {enzyme_for_substrate}")

# Choose other reaction parameters
temperature = st.sidebar.slider("Temperature (°C)", 25, 60, 35)
time_duration = st.sidebar.slider("Reaction Time (hours)", 1, 72, 10)
ph = st.sidebar.slider("pH", 4.0, 8.0, 6.0, 0.1)

st.title("Bioreactor Conversion Predictor")

# Load the trained ML model (cached for performance)
@st.cache_resource
def load_model():
    try:
        model = BioReactorModel.load("models/conversion_model.pkl")
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        st.stop()
    return model

model_instance = load_model()

# Prepare input for prediction
input_df = pd.DataFrame([{
    'substrate': selected_substrate,
    'enzyme': enzyme_for_substrate,
    'temperature': temperature,
    'time': time_duration,
    'ph': ph
}])

# Predict conversion for the given reaction conditions
predicted_conversion = model_instance.predict(input_df)[0]
st.write(f"### Predicted Conversion: {predicted_conversion:.2f}")

# Create and display a progression vs. time graph
st.write("### Conversion Progression Over Time")
# Generate time points from 1 hour to the selected reaction time
time_points = np.linspace(1, time_duration, num=50)
conversions = []
for t in time_points:
    temp_df = pd.DataFrame([{
        'substrate': selected_substrate,
        'enzyme': enzyme_for_substrate,
        'temperature': temperature,
        'time': t,
        'ph': ph
    }])
    conv = model_instance.predict(temp_df)[0]
    conversions.append(conv)
    
fig_progress = plot_progress(time_points, conversions)
st.plotly_chart(fig_progress, use_container_width=True)

# Optionally, display a 3D conversion landscape graph
if st.sidebar.checkbox("Show 3D Conversion Landscape"):
    st.write("### 3D Conversion Landscape")
    fig_3d = plot_3d_surface(model_instance, selected_substrate, enzyme_for_substrate, ph)
    st.plotly_chart(fig_3d, use_container_width=True)
