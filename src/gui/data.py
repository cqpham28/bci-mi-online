#===============================================#
#CUONG
import os
import numpy as np
import time
import mne
from mne.io import concatenate_raws
from mne.channels import make_standard_montage
from moabb.datasets.base import BaseDataset
from moabb.paradigms import MotorImagery

ROOT = r"C:\Users\cuong\bci\DATA"
LIST_SUBJECTS = list(range(12, 30))
SAMPLING_RATE = 128
EEG_CH_NAMES = [
    'Cz', 'Fz', 'Fp1', 'F7', 'F3', 
    'FC1', 'C3', 'FC5', 'FT9', 'T7', 
    'CP5', 'CP1', 'P3', 'P7', 'PO9', 
    'O1', 'Pz', 'Oz', 'O2', 'PO10', 
    'P8', 'P4', 'CP2', 'CP6', 'T8', 
    'FT10', 'FC6', 'C4', 'FC2', 'F4', 
    'F8', 'Fp2'
]
EVENTS_DICT = dict(right_hand=1, left_hand=2, right_foot=3, left_foot=4)


#--------------------#
class Flex2023_moabb(BaseDataset):
    """Motor Imagery moabb dataset"""

    def __init__(self):
        super().__init__(
            subjects=LIST_SUBJECTS,
            sessions_per_subject=1,
            events=EVENTS_DICT,
            code="Flex2023",
            interval=[4, 8], # events at 4s
            paradigm="imagery",
            doi="",
        )
        self.runs = "run1"
        

    def _flow(self, raw0, stim):
        ## get eeg (32,N)
        data = raw0.get_data(picks=EEG_CH_NAMES)
        # stack eeg (32,N) with stim (1,N) => (32, N)
        data = np.vstack([data, stim.reshape(1,-1)])

        ch_types = ["eeg"]*32 + ["stim"]
        ch_names = EEG_CH_NAMES + ["Stim"]
        info = mne.create_info(ch_names=ch_names, 
                            ch_types=ch_types, 
                            sfreq=SAMPLING_RATE)
        raw = mne.io.RawArray(data=data, 
                            info=info, 
                            verbose=False)
        montage = make_standard_montage("standard_1020")
        raw.set_montage(montage)
        # raw.set_eeg_reference(ref_channels="average")
        return raw


    def _get_single_subject_data(self, subject):
        """Return data for a single subject."""
    
        path_edf = self.data_path(subject)

        if self.runs != -1:
            list_edf = [i for i in path_edf if f"run{self.runs}" in i]
        else:
            list_edf = path_edf

        list_raw = []
        for _edf in list_edf:
            raw0 = mne.io.read_raw_edf(_edf, preload=False)
            stim = raw0.get_data(picks=["MarkerValueInt"], units='uV')[0]
            raw_run = self._flow(raw0, stim)
            list_raw.append(raw_run)
        raw = mne.concatenate_raws(list_raw)
        return {"0": {"0": raw}}


    def data_path(self, subject, path=None, 
        force_update=False, update_path=None, verbose=None):

        path_edf = []
        for root, dirs, files in os.walk(ROOT):
            for file in files:
                if file.endswith(".edf") and (f"F{subject}" in file):
                    path_edf.append(os.path.join(root, file))
        
        return path_edf



###############
def get_epochs(subject:int, run:int, event_ids=EVENTS_DICT):

    print(">>>GET EPOCHS")
        
    dataset = Flex2023_moabb()
    dataset.subject_list = [subject]
    dataset.runs = run

    ## 
    paradigm = MotorImagery(
            events = list(event_ids.keys()), 
            n_classes = len(event_ids.keys()),
            fmin = 0, 
            fmax = SAMPLING_RATE/2-0.001, 
            ) 
    X, labels, meta = paradigm.get_data(
        dataset=dataset, 
        subjects=[subject], 
        return_raws=True
        )
    raw = concatenate_raws([f for f in X])

    events, _ = mne.events_from_annotations(raw, event_id=event_ids)
    tmin, tmax = 0, 12
    epochs = mne.Epochs(
        raw,
        events,
        event_ids,
        tmin,
        tmax,
        picks=EEG_CH_NAMES,
        baseline=None,
        preload=True,
    )
    
    return epochs



###############
# epochs = get_epochs(subject=16, run=1, event_ids=EVENTS_DICT) 


# def wait(record_duration_s):
#     print('start recording -------------------------')
#     length = 0
#     while length < record_duration_s:
#         print('recording at {0} s'.format(length))
#         time.sleep(1)
#         length+=1
#     print('end recording -------------------------')






