from librosa.feature import mfcc
from numpy import arange, shape, array, linspace
from matplotlib.pyplot import figure, imshow, xlabel, ylabel, title, show

N_FFT = 512
WIN_LEN = 320
WIN_HOP = 160
N_MFCC = 10
WINDOW = 'hamming'
LIFTER = 2 * N_MFCC


def normalise(signal):
    return signal/max(abs(signal))


def get_mfcc(signal, fs, **kwargs):
    signal = normalise(signal)
    return mfcc(y=signal, sr=fs, **kwargs)


def plot_mfcc(mfcc_values, n, fs):
    t = arange(1, shape(mfcc_values)[1] - 1)

    x = linspace(0, n/fs, n)
    y = array(range(1, N_MFCC))
    z = mfcc_values[1:N_MFCC, t]
    tt = "Librosa MFCC"
    y_label = "Coefficients"

    fig = figure(figsize=(12, 3))
    x_min, x_max = min(x), max(x)
    y_min, y_max = min(y), max(y)
    im1 = imshow(z, extent=[x_min, x_max, y_min, y_max], aspect='auto', origin='lower', interpolation='none')
    xlabel("Time [sec]")
    title(tt)
    ylabel(y_label)
    fig.colorbar(im1)
    show()
