import plotly.graph_objects as go
import numpy as np
import pandas as pd

def plot_progress(time_points, conversions):
    """Create an interactive line+marker plot for conversion progression over time."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_points,
        y=conversions,
        mode='lines+markers',
        name='Conversion Progress',
        line=dict(color='#2ca02c', width=3)
    ))
    fig.update_layout(
        title='Bioreactor Conversion Over Time',
        xaxis_title='Time (hours)',
        yaxis_title='Conversion Ratio',
        template='plotly_white',
        height=500
    )
    return fig

def plot_3d_surface(model, substrate, enzyme, ph=6.5):
    """Generate a 3D surface plot of conversion as a function of temperature and time."""
    temps = np.linspace(25, 60, 30)
    times = np.linspace(1, 72, 30)
    T, Time = np.meshgrid(temps, times)
    
    # Prepare grid predictions
    Z = np.zeros_like(T)
    for i in range(T.shape[0]):
        for j in range(T.shape[1]):
            input_data = pd.DataFrame([{
                'substrate': substrate,
                'enzyme': enzyme,
                'temperature': T[i, j],
                'time': Time[i, j],
                'ph': ph
            }])
            Z[i, j] = model.predict(input_data)[0]
    
    fig = go.Figure(data=[go.Surface(z=Z, x=T, y=Time)])
    fig.update_layout(
        title=f'{substrate} Conversion Landscape',
        scene=dict(
            xaxis_title='Temperature (°C)',
            yaxis_title='Time (hours)',
            zaxis_title='Conversion Ratio',
            camera=dict(eye=dict(x=1.5, y=1.5, z=0.8))
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    return fig
