from numpy import linspace


class Track:
    def __init__(self, y, fs):
        self.y = y
        self.fs = fs
        self.n = len(y)
        if self.n == 0:
            self.time = None
        else:
            self.time = linspace(0, self.n/fs, self.n)
