# Bioreactor Conversion Predictor [![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)

An innovative machine learning application that predicts bioreactor conversion efficiency by leveraging modern technology and experimental data. This system allows users to select substrates and automatically determine the corresponding enzyme (sourced from the BRENDA Enzyme Database), adjust reaction conditions such as temperature, time, and pH, and view detailed visualizations of reaction progress.

![image](https://github.com/user-attachments/assets/15453073-10cf-47b5-b5e2-10740493a756)


## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
  - [Data Processing](#data-processing)
  - [Model Training](#model-training)
  - [Running the Frontend](#running-the-frontend)
- [Contributing](#contributing)
- [License](#license)

## Overview

The **Bioreactor Conversion Predictor** utilizes experimental enzyme kinetics and thermal profile data, primarily sourced from the [BRENDA Enzyme Database](https://www.brenda-enzymes.org/), to simulate realistic bioreactor reactions. The application uses a machine learning model to predict conversion efficiency and generates interactive visualizations to help researchers optimize reaction conditions.

## Features

- **ML-Based Prediction:** Uses a Gradient Boosting Regressor model to predict bioreactor conversion based on substrate, enzyme, temperature, time, and pH.
- **Dynamic Visualizations:** Interactive progression vs. time graph and 3D conversion landscape using Plotly.
  ![image](https://github.com/user-attachments/assets/c2e0a8c7-2cb7-45d2-9464-116d725321db)

- **User-Friendly Frontend:** Built with Streamlit to allow easy selection of reaction parameters.
- **Data Integration:** Incorporates experimental kinetic data from the BRENDA Enzyme Database for realistic modeling.

## Project Structure

```plaintext
bioreactor-system/
├── app/
│   ├── main.py              # Streamlit frontend entry point
│   ├── model.py             # ML model class for bioreactor conversion prediction
│   └── utils/
│       ├── data_loader.py   # Data generation and loading utilities
│       ├── optimizers.py    # Parameter optimization functions
│       └── visualizations.py # Plotting functions for conversion graphs
├── notebooks/
│   └── exploration.ipynb    # Jupyter Notebook for data exploration and prototyping
├── data/
│   ├── raw/                 # Raw data files (enzyme kinetics & thermal profiles)
│   └── processed/           # Processed dataset ready for model training
├── models/                  # Trained model binaries
├── requirements.txt         # List of project dependencies
└── README.md                # Project documentation
```

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/bioreactor-system.git
   cd bioreactor-system
   ```

2. **Set Up a Virtual Environment (Recommended):**
   * Windows:
    ```bash
    python -m venv env
    .\env\Scripts\activate
    ```
   * MacOS/Linux:
    ```bash
    python -m venv env
    source env/bin/activate
    ```  
3. **Install Dependencies:**
   ```py
   pip install -r requirements.txt
   ```
## Usage

# Data Processing
Before training the model, ensure the raw data is processed. If raw files (enzyme_kinetics.csv and thermal_profiles.json) are missing, run the data processing script:
```py
python -m app.utils.data_loader
```
Alternatively, in a Python shell:
```py
from app.utils.data_loader import process_raw_data
process_raw_data()
```

#Model Training
Train the machine learning model using the processed dataset:
```py
python app/model.py
```
This script loads the generated synthetic data, trains the ML model, and saves the trained model to [models/conversion_model.pkl](#models)

#Running the Frontend
Launch the Streamlit web application to interact with the predictor:
```py
streamlit run app/main.py
```
A new browser window should open (or navigate to http://localhost:8501) where you can select a substrate (with the enzyme auto-populated), adjust reaction conditions, and view the predicted conversion along with detailed visualizations.

## License
This project is licensed under the GPL-3.0 License. See the [LICENSE](#license) file for details.