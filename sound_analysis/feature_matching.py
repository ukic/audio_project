import numpy as np
from collections import defaultdict
from sklearn.mixture import GaussianMixture
from basic.audio_loading import import_wav
from spectral_analysis.mfcc import get_mfcc
from os import listdir
import pickle

N_FFT = 512
WIN_LEN = 320
WIN_HOP = 160
N_MFCC = 10
WINDOW = 'hamming'
LIFTER = 2 * N_MFCC


class GaussianModel:
    def __init__(self, training_set, sample_rate):
        self.models = {}

        for key in training_set.keys():
            self.models[key] = GaussianMixture(n_components=7, covariance_type="diag")
            self.models[key].fit(
                get_mfcc(training_set[key], sample_rate, S=None, n_mfcc=N_MFCC, lifter=LIFTER, n_fft=N_FFT,
                         hop_length=WIN_HOP, win_length=WIN_LEN, center=True, window=WINDOW).T)

    def score(self, signal, sample_rate):
        sig_mfcc = get_mfcc(signal, sample_rate, S=None, n_mfcc=N_MFCC, lifter=LIFTER, n_fft=N_FFT, hop_length=WIN_HOP,
                            win_length=WIN_LEN, center=True, window=WINDOW).T
        max_score = None
        prediction = None
        for key in self.models.keys():
            score = self.models[key].score(sig_mfcc)
            if max_score is None or score > max_score:
                max_score = score
                prediction = key
        return prediction

    def save(self, name):
        with open(name, 'wb') as filename:
            pickle.dump(self, filename)


def prepare_training_data(folder_path, label_value):
    training_set = defaultdict(lambda: np.array([]))
    sample_rate = 0
    for filename in listdir(folder_path):
        if filename.endswith(".wav"):
            track = import_wav(folder_path + "\\" + filename)
            label = "Speaker " + str(filename[label_value])
            if len(training_set[label]) == 0:
                training_set[label] = track.y
            else:
                training_set[label] = np.concatenate([training_set[label], track.y])
            sample_rate = track.fs
    return training_set, sample_rate


def verify(y, fs, feature):
    if feature == 0:
        name = "D:\AGH\Python\\audio_project\\sound_analysis\\speaker_model.pkl"
    elif feature == 1:
        name = "D:\AGH\Python\\audio_project\\sound_analysis\\digit_model.pkl"
    else:
        return -1
    with open(name, 'rb') as file:
        model = pickle.load(file)
    return model.score(y, fs)
