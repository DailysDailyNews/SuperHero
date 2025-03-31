import os
import time
import logging
import joblib # For saving/loading models
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class SelfLearning:
    def __init__(self, log_file="self_learning.log", model_file="anomaly_model.joblib"):
        self.log_file = log_file
        self.model_file = model_file
        self.logger = self._setup_logger()
        self.anomaly_model = self._load_or_train_model()
        self.scaler = StandardScaler()
        self.data_buffer = [] #buffer for training data.

    def _setup_logger(self):
        logger = logging.getLogger("SelfLearning")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def _load_or_train_model(self):
        """Loads a pre-trained model or trains a new one."""
        if os.path.exists(self.model_file):
            return joblib.load(self.model_file)
        else:
            return IsolationForest(contamination=0.05) # Adjust contamination as needed

    def _save_model(self):
        """Saves the trained anomaly detection model."""
        joblib.dump(self.anomaly_model, self.model_file)

    def monitor_system(self, system_data):
        """Monitors system data for anomalies."""
        try:
            scaled_data = self.scaler.fit_transform([system_data])
            anomaly_score = self.anomaly_model.decision_function(scaled_data)

            if anomaly_score < 0: # Negative scores indicate anomalies
                self.logger.warning(f"Anomaly detected: {system_data}, score: {anomaly_score}")
                # Take appropriate action (e.g., alert, block)
                return True #anomaly found
            else:
                self.logger.info(f"System data normal: {system_data}, score: {anomaly_score}")
                return False #no anomaly found

        except Exception as e:
            self.logger.error(f"Error monitoring system: {e}")
            return False

    def learn_from_user_actions(self, user_action_data):
        """Learns from user actions to improve anomaly detection."""
        self.data_buffer.append(user_action_data)
        if len(self.data_buffer) > 100: #train every 100 actions.
            self.train_model(self.data_buffer)
            self.data_buffer = []

    def train_model(self, training_data):
        """Trains the anomaly detection model with new data."""
        try:
            scaled_data = self.scaler.fit_transform(training_data)
            self.anomaly_model.fit(scaled_data)
            self._save_model()
            self.logger.info("Anomaly detection model trained.")
        except Exception as e:
            self.logger.error(f"Error training model: {e}")

# Example Usage (Integration with SuperHero):

if __name__ == "__main__":
    self_learning = SelfLearning()

    # Example system data (replace with actual system metrics)
    system_data = [10, 5, 20, 100] # CPU usage, memory usage, network traffic, etc.
    self_learning.monitor_system(system_data)

    # Example user action data (replace with actual user actions)
    user_action_data = [1, 0, 10, 5] # Action type, success/failure, time taken, resources used.
    self_learning.learn_from_user_actions(user_action_data)

    # Simulate more system data and user actions...
