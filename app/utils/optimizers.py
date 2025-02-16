import numpy as np
from scipy.optimize import minimize
import pandas as pd

def optimize_parameters(model, input_data, target=0.9):
    """
    Optimize temperature and time to achieve at least the target conversion.
    
    Parameters:
      - model: Trained ML model instance with a predict() method.
      - input_data: Dictionary containing 'substrate', 'enzyme', and 'ph'. 
                    Temperature and time will be optimized.
      - target: Desired conversion value (default 0.9).
    
    Returns:
      A dictionary with optimal temperature, optimal time, and the achievable conversion.
    """
    def objective(x):
        # Update input data with the current optimization values
        modified = input_data.copy()
        modified['temperature'] = x[0]
        modified['time'] = x[1]
        # Negative conversion for maximization (since we minimize)
        return -model.predict(pd.DataFrame([modified]))[0]
    
    def constraint_fun(x):
        # Constraint: predicted conversion must be at least the target
        modified = input_data.copy()
        modified['temperature'] = x[0]
        modified['time'] = x[1]
        return model.predict(pd.DataFrame([modified]))[0] - target
    
    bounds = [(25, 60), (1, 72)]
    constraints = [{'type': 'ineq', 'fun': constraint_fun}]
    
    # Use current temperature and time from input_data as initial guess, if available
    x0 = [input_data.get('temperature', 35), input_data.get('time', 10)]
    
    result = minimize(objective, x0=x0, bounds=bounds, constraints=constraints, method='SLSQP')
    
    if not result.success:
        raise ValueError("Optimization failed: " + result.message)
    
    return {
        'optimal_temp': result.x[0],
        'optimal_time': result.x[1],
        'achievable_conversion': -result.fun
    }
