import numpy as np
from librosa import pyin, times_like, note_to_hz, stft, amplitude_to_db


def pitch_detection(y, fs):
    d = amplitude_to_db(abs(stft(y)), ref=np.max)
    f0_pyin, voiced_flag, voiced_probs = pyin(y, sr=fs, fmin=note_to_hz('C2'), fmax=note_to_hz('C7'))
    times = times_like(f0_pyin)
    return d, f0_pyin, times
