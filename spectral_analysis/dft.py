import numpy as np
import matplotlib.pyplot as plt


FSIZE = (10, 10)


def dft(signal):
    n = len(signal)
    w = np.exp(-1j * 2 * np.pi / n)
    w = np.array([[w ** (i * k) for i in range(n)] for k in range(n)]) / n
    return w @ signal


def plot_dft(t, s, sd, fs, N):
    df = int(fs / (2 * N))
    f = np.linspace(0, N * df, 2 * N)
    fig, axs = plt.subplots(3, 1, figsize=FSIZE)
    axs[0].plot(t, s)
    axs[1].plot(f, abs(sd))
    axs[2].plot(f, np.array([np.angle(x) for x in sd]))
    plt.show()
