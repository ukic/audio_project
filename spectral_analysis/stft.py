from scipy.signal import stft
from numpy import ndarray
import matplotlib.pyplot as plt


def get_stft(s: ndarray, fs: int, overlap: float = 0):
    return stft(s, fs, nperseg=round(fs*20/1000), noverlap=round(fs*overlap))


def plot_stft(x: ndarray, f: ndarray, t: ndarray, title: str = ""):
    plt.figure(1)
    im1 = plt.pcolormesh(t, f, abs(x))
    plt.title("|"+title+"|")
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    plt.colorbar(im1)
    plt.show()
