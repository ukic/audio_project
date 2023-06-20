from numpy import ndarray, concatenate, zeros


def add_2_tracks(y1: ndarray, y2: ndarray):
    n1 = len(y1)
    n2 = len(y2)
    dn = abs(n1 - n2)
    if n1 > n2:
        y = concatenate((y2, zeros(dn)))
        return y + y1
    else:
        y = concatenate((y1, zeros(dn)))
        return y + y2


def add_tracks(y1: ndarray, y2: ndarray, y3: ndarray = None, y4: ndarray = None, y5: ndarray = None):
    y = add_2_tracks(y1, y2)
    if y3 is None:
        return y
    y = add_2_tracks(y, y3)
    if y4 is None:
        return y
    y = add_2_tracks(y, y4)
    if y5 is None:
        return y
    return add_2_tracks(y, y5)


def insert_to_track(y: ndarray, ins: ndarray, n: int):
    if n < 0:
        raise ValueError
    return concatenate((y[:n], ins, y[n:]))


def insert_to_track_by_time(y: ndarray, ins: ndarray, t0: int, fs: int):
    n = int(t0 * fs)
    return concatenate((y[:n], ins, y[n:]))


def change_loudness(y: ndarray, db: float):
    a = 10 ** (db/20)
    return y * a


def trim(y: ndarray, n0: int, n1: int):
    return y[n0:n1]


def trim_by_time(y: ndarray, t0: float, t1: float, fs: int):
    n0 = int(t0 * fs)
    n1 = int(t1*fs)
    return y[n0:n1]


def delete(y: ndarray, n0: int, n1: int):
    return concatenate((y[:n0], y[n1:]))


def delete_by_time(y: ndarray, t0: float, t1: float, fs: int):
    n0 = int(t0 * fs)
    n1 = int(t1*fs)
    return concatenate((y[:n0], y[n1:]))
