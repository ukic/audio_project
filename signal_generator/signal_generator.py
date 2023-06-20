from enum import Enum, auto
import numpy as np
from basic.track import Track


class SignalType(Enum):
    SINE = auto()
    SQUARE = auto()
    SAWTOOTH = auto()
    TRIANGLE = auto()
    SINC = auto()
    CHIRP = auto()


def calc_sin(x):
    return np.sin(x)


def calc_saw(t, f, amplitude):
    return 2 * amplitude * f * (t % (1 / f)) - amplitude


def calc_tr(t, f, amplitude):
    return 4 * amplitude * f * abs(((t - 0.5 / f) % (1 / f)) - 0.5 / f) - amplitude


def calc_sq(t, f, amplitude):
    return 2 * amplitude * (2 * np.floor(f * t) - np.floor(2 * f * t)) + amplitude


def sinc(x):
    if x == 0:
        return 1
    return np.sin(np.pi * x) / (np.pi * x)


def calc_sinc(samples):
    return np.array([sinc(t) for t in samples])


def get_chirp(phi, f0, c, t):
    return np.sin(phi + 2 * np.pi * (c * t * t / 2 + f0 * t))


def parse_signal_type(sig_type: str) -> SignalType:
    for s in SignalType:
        if sig_type == str(s)[7:]:
            return s
    raise ValueError


def generate_samples(a, b, fs):
    return np.linspace(a, b, int((b - a) * fs))


def generate_signal(sig_type: str, t, sample_rate, amplitude, f: int, phi) -> Track:
    sig_type = parse_signal_type(sig_type)
    samples = generate_samples(0, t, sample_rate)
    if sig_type == SignalType.SINE:
        return Track(amplitude * calc_sin((2 * np.pi * f * samples) + phi), sample_rate)
    if sig_type == SignalType.SQUARE:
        return Track(calc_sq(samples, f, amplitude), sample_rate)
    if sig_type == SignalType.SAWTOOTH:
        return Track(calc_saw(samples, f, amplitude), sample_rate)
    if sig_type == SignalType.TRIANGLE:
        return Track(calc_tr(samples, f, amplitude), sample_rate)
    if sig_type == SignalType.SINC:
        return Track(calc_sinc(samples), sample_rate)
    raise ValueError
