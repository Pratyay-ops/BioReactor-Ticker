import joblib
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

class BioReactorModel:
    """
    Machine learning model to predict bioreactor conversion based on
    substrate, enzyme, temperature, time, and pH.
    """
    def __init__(self):
        self.pipeline = None
        self.features = ['substrate', 'enzyme', 'temperature', 'time', 'ph']
        
    def train(self, data):
        """
        Train the ML pipeline using a ColumnTransformer to handle categorical
        and numerical features.
        """
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore'), ['substrate', 'enzyme']),
                ('num', StandardScaler(), ['temperature', 'time', 'ph'])
            ])
        
        self.pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('regressor', GradientBoostingRegressor(n_estimators=100))
        ])
        
        self.pipeline.fit(data[self.features], data['conversion'])
        
    def predict(self, X):
        """Return conversion predictions for the input DataFrame X."""
        return self.pipeline.predict(X)
    
    def save(self, path):
        """Save the trained pipeline to a file."""
        joblib.dump(self.pipeline, path)
        
    @classmethod
    def load(cls, path):
        """Load a trained pipeline from a file and return a BioReactorModel instance."""
        model = cls()
        model.pipeline = joblib.load(path)
        return model

if __name__ == "__main__":
    from utils.data_loader import BioReactorData
    
    print("Training bioreactor conversion model...")
    
    # Initialize data loader and model
    data_loader = BioReactorData()
    model = BioReactorModel()
    
    # Generate synthetic data samples
    try:
        df = data_loader.generate_samples(50000)
    except FileNotFoundError:
        print("Error: Missing raw data files. Run data processing first!")
        print("Execute: python3 -m app.utils.data_loader")
        exit(1)
    
    # Train and save the model
    model.train(df)
    model.save("models/conversion_model.pkl")
    print("Model training completed successfully!")
