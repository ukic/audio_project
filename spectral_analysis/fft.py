from numpy.fft import fft
from numpy import angle
import matplotlib.pyplot as plt


def get_fft(signal):
    return fft(signal)


def plot_fft(fft_values):
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(abs(fft_values))
    ax[1].plot(angle(fft_values))
    plt.show()
