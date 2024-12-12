import numpy as np
import threading
import time
import os
from cortex.record import Record
from dotenv import load_dotenv
from utils import SharedData



# Load environment variables for client info
load_dotenv(".env")
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
r = Record(client_id, client_secret)

class LSL_STREAM:
    def __init__(self, sampling_rate):
        self.sampling_rate = sampling_rate
        self.lock = threading.Lock()
        self.prediction_data = None
        self.new_data_event = threading.Event()

    def accumulate_samples(self, trial_duration=12):
        """Simulated sample accumulation with debug logging."""
        dur1 = int(self.sampling_rate * 4.0)
        dur2 = int(self.sampling_rate * 8.0)

        while True:
            trial_samples = []  
            index = 0
            print("Starting new trial sample accumulation...")  # Debug log

            while index < int(self.sampling_rate * trial_duration):
                time.sleep(0.01)  # Simulate sample collection delay
                sample = np.random.rand(35)  # Simulated sample data

                if dur1 <= index < dur2:
                    trial_samples.append(sample[3:35])

                index += 1

            # Signal new data availability
            with self.lock:
                self.prediction_data = np.array(trial_samples)
                self.new_data_event.set()  # Signal new data availability
                print("New data segment ready for prediction.")  # Debug log

    def get_prediction_data(self):
        """ Return the 4s-8s window data for prediction. """
        with self.lock:
            return self.prediction_data


def start_predicted_result(lsl, ml_module):
    """ Continuously predict based on the latest 4s-8s data window when available. """
    print("Prediction thread started.")  # Debug log

    while True:
        # Wait until new data is available
        lsl.new_data_event.wait()

        # Retrieve and process the prediction data
        prediction_data = lsl.get_prediction_data()
        if prediction_data is not None:
            preds = ml_module.predict(prediction_data).item()
            SharedData.setCurrentResult(preds)
            print("Prediction:", preds)  # Debug log

        # Reset event to wait for the next data update
        lsl.new_data_event.clear()
        time.sleep(0.1)  # Optional delay to reduce CPU usage


# Mocking the prediction module
class Module_Prediction:
    def predict(self, data):
        return np.array([1])  # Mock prediction result for testing


# Example setup for threading
if __name__ == "__main__":
    lsl = LSL_STREAM(sampling_rate=128)
    ml_module = Module_Prediction()

    # Start the data accumulation thread
    accumulate_thread = threading.Thread(target=lsl.accumulate_samples, args=(12,))
    accumulate_thread.start()

    # Start the prediction thread
    prediction_thread = threading.Thread(target=start_predicted_result, args=(lsl, ml_module))
    prediction_thread.start()

    print("Both threads initialized and started.")
