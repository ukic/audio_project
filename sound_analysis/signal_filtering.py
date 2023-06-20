from scipy.signal import butter, cheby1, cheby2, ellip, sosfilt, sosfreqz
from numpy import ndarray
from enum import Enum, auto


class FilteringType(Enum):
    HPF = 'highpass'
    LPF = 'lowpass'
    BPF = 'band'


class FilterType(Enum):
    BUTTERWORTH = auto()
    CHEBYSHEW1 = auto()
    CHEBYSHEW2 = auto()
    ELLIPTIC = auto()


def parse_filtering(filt: str) -> FilteringType:
    if filt == 'HPF':
        return FilteringType.HPF
    if filt == 'LPF':
        return FilteringType.LPF
    if filt == 'BPF':
        return FilteringType.BPF


def parse_type(filt: str) -> FilterType:
    if filt == 'BUTTERWORTH':
        return FilterType.BUTTERWORTH
    if filt == 'CHEBYSHEW1':
        return FilterType.CHEBYSHEW1
    if filt == 'CHEBYSHEW2':
        return FilterType.CHEBYSHEW2
    if filt == 'ELLIPTIC':
        return FilterType.ELLIPTIC


def design_filter(ftype: FilterType, filt: FilteringType, fs: int, f: [int, list], order: int = 10, rp: float = 5,
                  rs: float = 40, output='sos'):
    if ftype == FilterType.BUTTERWORTH:
        return butter(order, f, str(filt.value), fs=fs, output=output)
    elif ftype == FilterType.CHEBYSHEW1:
        return cheby1(order, rp, f, str(filt.value), fs=fs, output=output)
    elif ftype == FilterType.CHEBYSHEW2:
        return cheby2(order, rs, f, str(filt.value), fs=fs, output=output)
    elif ftype == FilterType.ELLIPTIC:
        return ellip(order, rp, rs, f, str(filt.value), fs=fs, output=output)


def filter_signal(signal: [ndarray, list], fs, f: [int, list], ftype: str, filt: str, order=10, rp=5, rs: float = 40):
    ftype = parse_type(ftype)
    filt = parse_filtering(filt)
    sos = design_filter(ftype, filt, fs, f, order, rp=rp, rs=rs)
    w, h = sosfreqz(sos)
    return sosfilt(sos, signal), w, h
