import time
import threading
import numpy as np
from pylsl import StreamInfo, StreamOutlet
from pylsl import StreamInlet, resolve_stream, resolve_bypred
import utils


class LSL_STREAM:
    def __init__(self):

        self.info = StreamInfo(
            name='BCI_online', 
            type='Markers', 
            channel_count=3,
            channel_format='float32', 
            source_id='BCI_online'
            )
        chns = self.info.desc().append_child("channels")

        # streams = resolve_stream('type', 'EEG')
        # self.inlet = StreamInlet(streams[0])

        for label in ["MarkerTime", "MarkerValue", "CurrentTime"]:
            ch = chns.append_child("channel")
            ch.append_child_value("label", label)
            ch.append_child_value("type", "Marker")
        self.info.desc().append_child_value("manufacturer", "PsychoPy")

        self.outlet = StreamOutlet(self.info)  # Broadcast the stream

        ###
        self.sampling_rate = 128
        self.trial_data = []  # Buffer to store the current trial's EEG data
        self.inlet = None  # Initialize inlet as None
        # self.lock = threading.Lock()  # To prevent data corruption in multi-threaded access
        self.new_data_event = threading.Event()  # Event to signal new data availability


    def push_marker(self, id_trial, label):
        self.outlet.push_sample([id_trial, label, time.time()])


    def initialize_inlet(self, timeout=5):
        """Initialize the LSL stream inlet with a timeout."""

        print("Attempting to connect to LSL stream...")
        while True:
            try:
                # Try to resolve the EEG stream with a specified timeout
                streams = resolve_bypred("type='EEG'", timeout=timeout)
                if streams:
                    # If a stream is found, initialize the inlet and break the loop
                    self.inlet = StreamInlet(streams[0])
                    print(">>>[SUCCESS] LSL stream is connected!.")
                    break

                else:
                    # If no streams found, display a warning and wait for user action
                    print(f">>>[ERROR] No EEG stream detected!")
                    input("Please connect your EEG device and press [ENTER] to retry...")

            except Exception as e:
                print(f"Error while connecting to LSL stream: {e}")
                time.sleep(2)  # Optional: wait briefly before retrying


    # def accumulate_samples(self):
    
    #     dur1 = int(self.sampling_rate * 4.0)  # Start index for 4s (e.g., at 128 Hz, it's 512 samples)
    #     dur2 = int(self.sampling_rate * 8.0)  # End index for 8s (e.g., 1024 samples)

    #     accumulated_samples = []
    #     index = 0

    #     while index <= dur2:
        
    #         sample, timestamp = self.inlet.pull_sample() # sample contains 37 points

    #         if timestamp is not None:
    #             if index > dur1:
    #                 accumulated_samples.append(sample[3:35])  # Only take the EEG channels
    #                 # print(f"[accumulated_samples] index = {index}")   
    #             index += 1
    
    #     accumulated_samples = np.array(accumulated_samples).T # 32,512
    #     return accumulated_samples


    def accumulate_samples(self):
    
        dur1 = int(self.sampling_rate * 4.0)  # Start index for 4s (e.g., at 128 Hz, it's 512 samples)
        dur2 = int(self.sampling_rate * 8.0)  # End index for 8s (e.g., 1024 samples)

        accumulated_samples = []
        index = 0
        while index < 512:
            
            try:
                current_experiment_time = int(utils.SharedDataTimer.getCurrentResult().toString('ss'))
                current_trial_time = current_experiment_time % 12 
            except:
                continue


            sample, timestamp = self.inlet.pull_sample() # sample contains 37 points
            
            if timestamp is not None:
                if 8 >= current_trial_time >= 4:
                    accumulated_samples.append(sample[3:35])  # EEG channels
                    
                    if index == 0:
                        print(f"time: {current_trial_time} ({current_experiment_time}), START ACCUMULATE, index: {index}")
                    elif index == 511:
                        print(f"time: {current_trial_time} ({current_experiment_time}), END ACCUMULATE, index: {index}")
                    index += 1
    
        accumulated_samples = np.array(accumulated_samples).T # 32,512
         
        return accumulated_samples

        

def start_predicted_result(lsl, ml_module):

    print(f"\n>>>[predict_thread] --> start_predicted_result()")

    while True:

        # # # Wait for the new data signal
        # lsl.new_data_event.wait()   
        
        # # Get and process the prediction data
        prediction_data = lsl.accumulate_samples()

        if prediction_data is not None :
            
            # Predict on the accumulated 4s-8s data
            preds = ml_module.predict(prediction_data).item()
            utils.SharedDataLabel.setCurrentResult(preds)

            # Logs
            print("DATA: ", prediction_data)
            print("PREDICTION RESULT: ", preds)

        # # Clear the event to wait for the next new data signal
        # lsl.new_data_event.clear()
        time.sleep(0.1)  # Optional sleep to reduce CPU usage






# # #--------------------#
# def start_record_offline(**kwargs):

#     ##
#     num_samples = 512
#     trial_idx = 0
#     while trial_idx < kwargs["n_trials"]:
#         data = epochs[trial_idx].crop(4,8).get_data() # (1,chan,513)
#         array_sample = data[0,:,:num_samples] # (chan,512)

#         wait(12)
#         trial_idx += 1
#     return array_sample


class OFFLINE_STREAM:
    def __init__(self):
        # data = start_record_offline()
        # self.epochs = get_epochs(subject=20, run=1)  
        # self.data = self.epochs[index-1].crop(4, 8).get_data() # (1,3,513)

        self.data = np.random.random_sample((32, 512))

    def accumulate_samples(self, index:int=1):
        # return np.array(self.data[0, :, :512])
        return self.data






# # s = Offline_Stream()
# # print(s.accumulate_samples().shape)
    

# #--------------------#
# def start_predicted_result(lsl, ml_module, index=1):

#     # Accumulate samples for 4 seconds
#     accumulated_samples = lsl.accumulate_samples(index)
#     print("okkkkkkkkk", accumulated_samples[0, :5])

#     # Process the accumulated samples and predict
#     return SharedData.setCurrentResult(
#         ml_module.predict(accumulated_samples).item())