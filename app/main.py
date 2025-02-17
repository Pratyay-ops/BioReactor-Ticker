!pip install --upgrade pip
import streamlit as st
import pandas as pd
import numpy as np
from model import BioReactorModel
from utils.visualizations import plot_progress, plot_3d_surface
import plotly.io as pio  # Needed for exporting the figure as an image

# Load kinetics data to get valid substrate-enzyme mappings
@st.cache_data
def load_kinetics_data():
    return pd.read_csv('data/raw/enzyme_kinetics.csv')

kinetics_data = load_kinetics_data()
substrate_options = kinetics_data['Substrate'].unique().tolist()

st.sidebar.title("Bioreactor Parameters")
st.sidebar.write('________________________________________________')
# Select substrate and automatically determine enzyme from kinetics data
selected_substrate = st.sidebar.selectbox("Select Substrate", substrate_options)
enzyme_for_substrate = kinetics_data[kinetics_data['Substrate'] == selected_substrate]['Enzyme'].iloc[0]
st.sidebar.markdown(f"**Enzyme:** {enzyme_for_substrate}")

# Choose other reaction parameters
temperature = st.sidebar.slider("Temperature (°C)", 25, 60, 35)
time_duration = st.sidebar.slider("Reaction Time (hours)", 1, 72, 10)
ph = st.sidebar.slider("pH", 4.0, 8.0, 6.0, 0.1)

st.title("Bioreactor Conversion Predictor")
st.write('______________________________________________________________________')
st.write('This system allows users to select substrates, adjust reaction conditions such as temperature,')
st.write('time, and pH, and view detailed visualizations of reaction progress.')

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
st.success(f"### Predicted Conversion(α): {predicted_conversion:.2f}")
st.write('______________________________________________________________________')

# Create and display a progression vs. time graph
st.write("### Conversion Progression Over Time")
st.info(f"The reaction progress is shown for {selected_substrate} with {enzyme_for_substrate} at {temperature}°C, {ph} pH, and {time_duration} hours.") 

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

# Option 1: Download the underlying progression data as CSV
progress_df = pd.DataFrame({
    'Time (hours)': time_points,
    'Conversion Ratio': conversions
})
csv_data = progress_df.to_csv(index=False)
st.download_button(
    label="Download Conversion Data as CSV",
    data=csv_data,
    file_name='conversion_progress_data.csv',
    mime='text/csv'
)

# Option 2: Download the interactive graph as an HTML file
graph_html = fig_progress.to_html(include_plotlyjs='cdn')
st.download_button(
    label="Download Interactive Graph as HTML",
    data=graph_html,
    file_name='conversion_progress_graph.html',
    mime='text/html'
)

# Option 3: Download the graph as a PNG image
# Make sure you have installed the 'kaleido' package for this to work.
image_bytes = fig_progress.to_image(format="png")
st.download_button(
    label="Download Graph as PNG",
    data=image_bytes,
    file_name='conversion_progress_graph.png',
    mime='image/png'
)

st.write('______________________________________________________________________')

# Optionally, display a 3D conversion landscape graph
if st.sidebar.checkbox("Show 3D Conversion Landscape"):
    st.write("### 3D Conversion Landscape")
    fig_3d = plot_3d_surface(model_instance, selected_substrate, enzyme_for_substrate, ph)
    st.plotly_chart(fig_3d, use_container_width=True)
