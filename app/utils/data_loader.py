import pandas as pd
import numpy as np
import os

class BioReactorData:
    """
    Class to load raw kinetic and thermal data, and to generate synthetic
    bioreactor reaction samples.
    """
    def __init__(self):
        # Load kinetic data with error handling
        try:
            self.kinetic_data = pd.read_csv('data/raw/enzyme_kinetics.csv')
        except FileNotFoundError:
            raise FileNotFoundError("enzyme_kinetics.csv not found in data/raw. Please process raw data first.")
        
        try:
            self.thermal_data = pd.read_json('data/raw/thermal_profiles.json')
        except FileNotFoundError:
            raise FileNotFoundError("thermal_profiles.json not found in data/raw. Please ensure the file exists.")
    
    def generate_samples(self, n=10000):
        """
        Generate synthetic bioreactor samples with realistic parameters based on
        Michaelis-Menten kinetics and temperature adjustments.
        """
        samples = []
        for _ in range(n):
            # Randomly choose a substrate from the kinetics data
            substrate = np.random.choice(self.kinetic_data.Substrate)
            # Get the corresponding enzyme and kinetic parameters
            row = self.kinetic_data[self.kinetic_data.Substrate == substrate].iloc[0]
            enzyme = row['Enzyme']
            km = row['Km(mM)']
            vmax = row['Vmax(μmol/min)']
            
            # Simulate reaction conditions
            temp = np.random.normal(loc=35, scale=5)
            time_val = np.random.uniform(1, 72)
            ph = np.random.normal(loc=6.0, scale=0.5)
            
            # Michaelis-Menten kinetics adjusted by temperature deviation from 37°C
            conversion = (vmax * time_val) / (km + time_val) * np.exp(-0.05 * abs(temp - 37))
            conversion = np.clip(conversion + np.random.normal(0, 0.05), 0, 1)
            
            samples.append({
                'substrate': substrate,
                'enzyme': enzyme,
                'temperature': temp,
                'time': time_val,
                'ph': ph,
                'conversion': conversion
            })
            
        return pd.DataFrame(samples)

def process_raw_data():
    """
    Process raw data files into a training-ready format.
    If the kinetic data is missing, generate sample data.
    """
    print("Processing raw data...")
    
    loader = BioReactorData()
    
    # If raw data does not exist, generate a small sample for demonstration.
    if not os.path.exists('data/raw/enzyme_kinetics.csv'):
        print("Raw enzyme kinetics data not found. Generating sample data...")
        sample_data = loader.generate_samples(1000)
        os.makedirs('data/raw', exist_ok=True)
        sample_data.to_csv('data/raw/enzyme_kinetics.csv', index=False)
    
    # Process and save a larger synthetic dataset
    processed = loader.generate_samples(10000)
    os.makedirs('data/processed', exist_ok=True)
    processed.to_csv('data/processed/training_data.csv', index=False)
    print("Data processing complete!")
