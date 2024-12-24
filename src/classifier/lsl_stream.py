import utils
import time
import threading
import numpy as np
from pylsl import (
    StreamInfo, 
    StreamOutlet, 
    StreamInlet,
    resolve_stream,
    resolve_bypred,
    local_clock,
)

class LSL_STREAM:
    def __init__(self):
        """
        
        """
        self.info = StreamInfo(
            name='BCI_online', 
            type='Markers', 
            channel_count= 3, # 3,
            channel_format='float32', 
            source_id='BCI_online',
            # nominal_srate = 128, # add
            )
        
        chns = self.info.desc().append_child("channels")

        for label in ["MarkerTime", "MarkerValue", "CurrentTime"]:
            ch = chns.append_child("channel")
            ch.append_child_value("label", label)
            ch.append_child_value("type", "Marker")
        self.info.desc().append_child_value("manufacturer", "PsychoPy")

        # inits
        self.outlet = StreamOutlet(self.info)  # Broadcast the stream
        self.inlet = None  # Initialize inlet as None
        self.sampling_rate = 128


    #-------------------------#
    def push_marker(self, id_trial, label):
        """push marker outlet"""
        self.outlet.push_sample([id_trial, label, time.time()])


    #-------------------------#
    def initialize_inlet(self, timeout=5):
        """Initialize the LSL stream inlet
        Check pylsl time_correction() and local_clock() for offset
        """
        print("Attempting to connect to LSL stream...")
        while True:
            try:
                # Try to resolve the EEG stream with a specified timeout
                streams = resolve_bypred("type='EEG'", timeout=0)
                # streams = resolve_stream('type', 'EEG')

                # If a stream is found, initialize the inlet and break the loop
                if len(streams) > 0:
                    self.inlet = StreamInlet(streams[0])
                    print(">>>[SUCCESS] LSL stream is connected!.")
                    break

                # If no streams found, display a warning and wait for user action
                else:
                    print(f">>>[ERROR] No EEG stream detected!")
                    input("Please connect your EEG device and press [ENTER] to retry...")

            except Exception as e:
                print(f"Error while connecting to LSL stream: {e}")
                time.sleep(2)  # Optional: wait briefly before retrying



    #-------------------------#
    def accumulate_samples(self):
        """start accumulate prediction samples."""
    
        accumulated_samples = []
        idx = 0
        idx_accumulated = 0
        while True:       
            # pull sample (37 data points) +  timestamp (internal time_clock)
            sample, timestamp = self.inlet.pull_sample()

            flag = utils.SharedStartAccumulate.getCurrentResult()
            if sample is not None and flag:
                print(f"[ACCUMULATED {idx_accumulated}/{idx}] {sample[:5]}")
                accumulated_samples.append(sample)  # EEG channels
                idx_accumulated += 1
            
            if idx_accumulated == 512:
                utils.SharedStartAccumulate.setCurrentResult(False)
                break
            
            idx += 1

        accumulated_samples = np.array(accumulated_samples).T # 37,512        
        return accumulated_samples




#=====================#
def start_predicted_result(lsl, ml_module):
    """ function to infer prediction to accumulated data"""

    print(f"\n>>>[predict_thread] --> start_predicted_result()")

    while True:
        # Get and process the prediction data
        accumulated_samples = lsl.accumulate_samples()
        
        if accumulated_samples is not None :
            
            # Predict on the accumulated 4s-8s data
            prediction_data = accumulated_samples[3:35,:]
            preds = ml_module.predict(prediction_data).item()
            utils.SharedDataLabel.setCurrentResult(preds)

            # Logs
            print("DATA: ", prediction_data)
            print("PREDICTION RESULT: ", preds)
        
        # Optional sleep to reduce CPU usage
        time.sleep(0.1)  



#=====================#
class OFFLINE_STREAM:
    """
    debug offline stream
    """
    def __init__(self):
        self.data = np.random.random_sample((32, 512))

    def accumulate_samples(self, index:int=1):
        return self.data

