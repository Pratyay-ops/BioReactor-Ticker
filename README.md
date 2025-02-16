# Bioreactor Conversion Predictor

An innovative machine learning application that predicts bioreactor conversion efficiency by leveraging modern technology and experimental data. This system allows users to select substrates and automatically determine the corresponding enzyme (sourced from the BRENDA Enzyme Database), adjust reaction conditions such as temperature, time, and pH, and view detailed visualizations of reaction progress.

![Bioreactor Conversion Predictor](![image](https://github.com/user-attachments/assets/c616566a-ad82-4d4a-a93d-4414e7b76ded)
)

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
  ```bash
      
3. 
4. 
5. 
