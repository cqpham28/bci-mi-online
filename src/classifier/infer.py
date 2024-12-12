"""
Author: Cuong
"""

import os
import numpy as np
from scipy import stats
import onnxruntime

from classifier.utils import chunk, butter_bandpass, func_softmax



class Module_Prediction:
    def __init__(
        self, 
        path_onnx: str,
        fs: int = 128,
        window: float = 2.0,
        overlap: float = 0.5,

        ):
        """
        Args:
            array_input (np.array, float32): 2s window (1,32,256) 
            filepath (str): path to onnx model
        """
        self.path_onnx = path_onnx
        self.fs = fs
        self.win_sample = int(window*fs)
        self.overlap_sample = int(overlap*fs)


    def _onnx(self, x: np.array) -> None: 
        """ onnxruntime for a single input (e.g., window 1s within a trial) """
        
        ort_session = onnxruntime.InferenceSession(self.path_onnx,
                                    providers=["CPUExecutionProvider"])
        input_name = ort_session.get_inputs()[0].name
        ort_inputs = {input_name: x}
        ort_outs = ort_session.run(None, ort_inputs)
        return ort_outs


    def _preprocess(self, inp: np.array):
        """ preprocesing """

        inp = butter_bandpass(inp, fs=128, order=3, lowcut=8, highcut=30)
        inp = np.expand_dims(inp, 0).astype(np.float32) # (1,12,5000)
        # print(">>>> INPUT SHAPE", inp.shape)

        return inp


    # def predict(self, eeg_trial: np.array):
    #     """ Run prediction on the trial """

    #     # Chunk window segments
    #     list_arr = chunk(eeg_trial, self.win_sample, self.overlap_sample)
        
    #     # Pipeline predict
    #     y_preds = []
    #     for arr in list_arr:
    #         arr = self._preprocess(arr)
    #         out = self._onnx(arr)
    #         prob = func_softmax(out[0].reshape(-1,))
    #         y_preds.append(np.argmax(prob))
        
    #     # Vote
    #     y_preds = np.array(y_preds)
    #     y_vote = stats.mode(y_preds, keepdims=True)[0]

    #     return y_vote+1



    def predict(self, eeg_trial: np.array):
        """ Run prediction on the trial """

        # Chunk window segments
        list_arr = chunk(eeg_trial, self.win_sample, self.overlap_sample)
        
        # Pipeline predict
        y_preds = []
        for arr in list_arr:
            arr = self._preprocess(arr)
            out = self._onnx(arr)
            pred = np.argmax(out[0])
            y_preds.append(pred)
        
        
        # Vote
        y_preds = np.array(y_preds)
        y_vote = stats.mode(y_preds, keepdims=True)[0]

        return y_vote+1






