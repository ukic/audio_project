from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QMessageBox
from PyQt5 import uic
from gui.mpl_canvas import MplCanvas

from basic.track import Track
from basic.audio_loading import import_wav
from basic.basic_audio_modifications import change_loudness, delete, delete_by_time, insert_to_track, \
    insert_to_track_by_time, trim, trim_by_time


class ModificationWindow(QMainWindow):
    def __init__(self, parent, y, fs, i):
        super().__init__()

        uic.loadUi('gui/modificationWindow.ui', self)

        self.parent = parent
        self.y = y
        self.fs = fs
        self.i = i

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.axes = self.canvas.fig.add_subplot(111)
        self.axes.plot(self.y)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.trackBox.setLayout(layout)

        self.trimButton.clicked.connect(self.trim)
        self.insertButton.clicked.connect(self.insert)
        self.removeButton.clicked.connect(self.delete)

        self.volumeButton.clicked.connect(self.change_volume)
        self.closeButton.clicked.connect(self.close_func)
        self.applyButton.clicked.connect(lambda: self.close_func(True))

    def redraw(self):
        self.axes.cla()
        self.axes.plot(self.y)
        self.canvas.draw()

    def change_volume(self):
        self.y = change_loudness(self.y, self.volumeSlider.value())
        self.redraw()

    def trim(self):
        v0 = self.fromSpinBox.value()
        v1 = self.toSpinBox.value()
        if self.unitComboBox == "samples":
            self.y = trim(self.y, v0, v1)
        else:
            self.y = trim_by_time(self.y, v0, v1, self.fs)
        self.redraw()

    def choose_signal(self):
        path = self.parent.choose_read_wav_file()
        t = import_wav(path)
        if t.fs != self.fs:
            msg = QMessageBox.warning(self, 'MessageBox', "Your sampling rate differs from the file you want to insert."
                                                          "Do you want to continue?", QMessageBox.Yes | QMessageBox.No)
            if msg == QMessageBox.Yes:
                return t.y, t.fs
            return None, -1
        return t.y, t.fs

    def insert(self):
        sig, fs = self.choose_signal()
        if fs == -1:
            return
        v0 = self.fromSpinBox.value()
        if self.unitComboBox == "samples":
            self.y = insert_to_track(self.y, sig, v0)
        else:
            self.y = insert_to_track_by_time(self.y, sig, v0, self.fs)
        self.redraw()

    def delete(self):
        v0 = self.fromSpinBox.value()
        v1 = self.toSpinBox.value()
        if self.unitComboBox == "samples":
            self.y = delete(self.y, v0, v1)
        else:
            self.y = delete_by_time(self.y, v0, v1, self.fs)
        self.redraw()

    def close_func(self, save=False):
        if save:
            t = Track(self.y, self.fs)
            self.parent.tracks[self.i] = t
            self.parent.draw_osc(t, self.parent.parse_osc(self.i+1))
        self.close()
