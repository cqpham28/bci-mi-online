import os
import numpy as np
import random
import scipy.signal as signal



def fixSeed(seed: int):
    """ random seed """
    random.seed(seed)
    os.environ["PYTHONSEED"] = str(seed)
    np.random.seed(seed)


def butter_bandpass(data, fs, order, lowcut, highcut):
    """ butterworth bandpass filter """
    
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    y = signal.lfilter(b, a, data)
    return y


def func_softmax(Z):
    """ softmax values for each sets of scores """
    e_Z = np.exp(Z - np.max(Z, axis = 0, keepdims = True))
    A = e_Z / e_Z.sum(axis = 0)
    return A



def chunk(arr_in, win_sample, overlap_sample):
    """ segment data into chunk """

    len_arr = arr_in.shape[1]
    if win_sample >= len_arr:
        return [arr_in]

    else:
        sample_start = list(np.arange(0, len_arr - win_sample, overlap_sample))
        sample_end = [x + win_sample for x in sample_start]
        # print([(i,j) for i,j in zip(sample_start, sample_end)])

        list_arr_out = []
        for i in range(len(sample_start)):
            list_arr_out.append(arr_in[:, sample_start[i]: sample_end[i]])

        return list_arr_out