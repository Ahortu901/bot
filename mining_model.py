import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import joblib

# Data preprocessing and model training
class MiningProfitabilityModel:
    def __init__(self, data_file='mining_data.csv'):
        self.data_file = data_file
        self.model = None

    def load_data(self):
        """
        Load historical mining data (e.g., mining difficulty, price, hash rate, power cost)
        """
        # Load dataset (adjust path if necessary)
        df = pd.read_csv(self.data_file)
        df.dropna(inplace=True)  # Remove missing values
        return df

    def train_model(self):
        """
        Train a model to predict mining profitability based on features such as
        difficulty, hash rate, price, and energy cost.
        """
        # Load data
        df = self.load_data()
        
        # Features (mining difficulty, hash rate, energy cost, crypto price, etc.)
        X = df[['difficulty', 'hash_rate', 'energy_cost', 'crypto_price', 'power_usage']]
        
        # Target variable (profitability)
        y = df['profitability']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a Random Forest Regressor model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        # Predict on the test set and evaluate
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f'Mean Squared Error: {mse}')

        # Save the model for future use
        joblib.dump(self.model, 'mining_profitability_model.pkl')
    
    def predict_profitability(self, difficulty, hash_rate, energy_cost, crypto_price, power_usage):
        """
        Predict mining profitability for given parameters
        """
        # Ensure model is loaded
        if self.model is None:
            self.model = joblib.load('mining_profitability_model.pkl')
        
        # Prepare input data
        input_data = np.array([[difficulty, hash_rate, energy_cost, crypto_price, power_usage]])
        
        # Make prediction
        profitability = self.model.predict(input_data)
        return profitability[0]

    def plot_feature_importance(self):
        """
        Plot feature importance based on trained model
        """
        if self.model is None:
            self.model = joblib.load('mining_profitability_model.pkl')
        
        # Feature importance
        feature_importance = self.model.feature_importances_

        # Plot
        features = ['difficulty', 'hash_rate', 'energy_cost', 'crypto_price', 'power_usage']
        plt.bar(features, feature_importance)
        plt.title("Feature Importance")
        plt.xlabel('Features')
        plt.ylabel('Importance')
        plt.show()
