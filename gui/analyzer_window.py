from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QMessageBox, QWidget, QLabel
from PyQt5 import uic
from gui.mpl_canvas import MplCanvas
import pywhisper
import numpy as np
from librosa.display import specshow

from spectral_analysis.dft import dft
from spectral_analysis.fft import get_fft
from spectral_analysis.mfcc import get_mfcc
from spectral_analysis.stft import get_stft
from sound_analysis.signal_filtering import filter_signal
from sound_analysis.pitch_detection import pitch_detection
from sound_analysis.asr import transcribe
from sound_analysis.feature_matching import verify, GaussianModel
from basic.track import Track


class FilterWindow(QWidget):
    def __init__(self, w, h):
        super().__init__()
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.draw(w, h)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.setWindowTitle("Filter characteristics")
        self.show()

    def draw(self, w, h):
        self.canvas.fig.clf()
        db = 20 * np.log10(np.maximum(np.abs(h), 1e-5))
        w = w / np.pi
        ax = self.canvas.fig.add_subplot(2, 1, 1)
        ax.plot(w, db)
        ax = self.canvas.fig.add_subplot(2, 1, 2)
        ax.plot(w, np.angle(h))
        self.canvas.draw()


class TranscriptionWindow(QWidget):
    def __init__(self, text):
        super().__init__()
        self.textarea = QLabel()
        self.textarea.setText(text)
        layout = QVBoxLayout()
        layout.addWidget(self.textarea)
        self.setLayout(layout)
        self.setWindowTitle("Transcription")
        self.show()


class AnalyzerWindow(QMainWindow):
    def __init__(self, parent, y, fs, i):
        super().__init__()

        uic.loadUi('GUI/analyzerWindow.ui', self)

        self.parent = parent
        self.y = y
        self.fs = fs
        self.i = i

        self.n = len(self.y)
        self.t = [t / fs for t in range(self.n)]

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        self.analysisBox.setLayout(layout)

        self.analyseButton.clicked.connect(self.analyze)
        self.closingButton.clicked.connect(self.close_func)
        self.applyButton.clicked.connect(lambda: self.close_func(True))
        self.filterButton.clicked.connect(self.filter_signal)
        self.transcribeButton.clicked.connect(self.transcribe)
        self.pitchButton.clicked.connect(self.detect_pitch)
        self.recognitionButton.clicked.connect(self.speaker_matching)
        self.digitButton.clicked.connect(self.digit_recognition)

        self.filt_win = None
        self.txt = None

        self.model = pywhisper.load_model("small")

    def analyze(self):
        self.clear_figure()
        if self.analysisType.currentText() == "DFT":
            self.draw_ft('DFT')
        elif self.analysisType.currentText() == "FFT":
            self.draw_ft('FFT')
        elif self.analysisType.currentText() == "MFCC":
            nmfcc = int(self.nMFCCSpin.value() * self.fftSpin.value() / 100)
            winhop = int(self.winHopSpin.value() * self.fftSpin.value() / 100)
            winlen = int(self.winlenSpin.value() * self.fftSpin.value() / 100)
            self.draw_mfcc(nmfcc, lifter=self.lifterSpin.value() * nmfcc, dct_type=self.dctSpin.value(),
                           n_fft=self.fftSpin.value(), hop_length=winhop,
                           win_length=winlen, center=True, window=self.windowType.currentText())
        elif self.analysisType.currentText() == "STFT":
            self.draw_stft(int(self.fftSpin.value() * self.winHopSpin.value() / 100))

    def draw_ft(self, transform_type):
        try:
            if transform_type == 'DFT':
                if self.n > 1000:
                    msg = QMessageBox.warning(self, 'DFT warning',
                                              "DFT is a time-consuming method and you have more than 1000 samples. "
                                              "Try FFT instead. Do you want to continue?",
                                              QMessageBox.Yes | QMessageBox.No)
                    if msg != QMessageBox.Yes:
                        return None, -1
                ft = dft(self.y)
            else:
                ft = get_fft(self.y)
            df = int(self.fs / (2 * self.n))
            f = np.linspace(0, self.n * df, 2 * self.n)[:len(ft)]

            ax = self.canvas.fig.add_subplot(3, 1, 1)
            ax.plot(self.t, self.y)
            ax = self.canvas.fig.add_subplot(3, 1, 2)
            ax.plot(f, abs(ft))
            ax = self.canvas.fig.add_subplot(3, 1, 3)
            ax.plot(f, np.array([np.angle(x) for x in ft]))
            self.canvas.draw()
        except ValueError:
            self.error_window("Wrong ft parameters!")

    def error_window(self, text):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Error")
        dlg.setText(text)
        dlg.setStandardButtons(QMessageBox.Ok)
        dlg.setIcon(QMessageBox.Critical)
        dlg.exec()

    def draw_mfcc(self, n_mfcc, **kwargs):
        try:
            n = len(self.y)
            mfcc_values = get_mfcc(self.y, self.fs, **kwargs)
            tt = np.arange(1, np.shape(mfcc_values)[1] - 1)

            x = np.linspace(0, n / self.fs, n)
            y = np.array(range(1, n_mfcc))
            z = mfcc_values[1:n_mfcc, tt]

            x_min, x_max = min(x), max(x)
            y_min, y_max = min(y), max(y)
            ax = self.canvas.fig.add_subplot(1, 1, 1)
            ax.imshow(z, extent=[x_min, x_max, y_min, y_max],
                      aspect='auto', origin='lower', interpolation='none')
            self.canvas.draw()
        except ValueError:
            self.error_window("Wrong mfcc parameters!")

    def draw_stft(self, overlap):
        try:
            f, t, x = get_stft(self.y, self.fs, overlap)
            ax = self.canvas.fig.add_subplot(1, 1, 1)
            ax.pcolormesh(t, f, abs(x))
            self.canvas.draw()
        except ValueError:
            self.error_window("Wrong stft parameters!")

    def filter_signal(self):
        filtering_type = self.filteringTypeBox.currentText()
        if filtering_type == 'HPF' or filtering_type == 'LPF':
            self.y, w, h = filter_signal(self.y, self.fs, self.f0SpinBox.value(), self.filterTypeBox.currentText(),
                                         filtering_type, order=self.orderSpinBox.value(), rp=self.rpSpinBox.value())
        else:
            self.y, w, h = filter_signal(self.y, self.fs, [self.f0SpinBox.value(), self.f1SpinBox.value()],
                                         self.filterTypeBox.currentText(), filtering_type,
                                         order=self.orderSpinBox.value(), rp=self.rpSpinBox.value())
        if self.filtResponse.isChecked():
            if self.filt_win is None:
                self.filt_win = FilterWindow(w, h)
            else:
                self.filt_win.draw(w, h)
        self.clear_figure()
        ax = self.canvas.fig.add_subplot(1, 1, 1)
        ax.plot(self.y)
        self.canvas.draw()

    def transcribe(self):
        data = transcribe(self.y, self.model)
        self.txt = TranscriptionWindow(data)
        self.txt.show()

    def detect_pitch(self):
        self.clear_figure()
        d, f0, times = pitch_detection(self.y[:10000], self.fs)
        ax = self.canvas.fig.add_subplot(111)
        img = specshow(d, x_axis='time', y_axis='log', ax=ax)
        self.canvas.fig.colorbar(img, ax=ax, format="%+2.f dB")
        ax.plot(times, f0, label='f0', color='cyan', linewidth=3)
        ax.legend(loc='upper right')
        self.canvas.draw()

    def digit_recognition(self):
        result = verify(self.y, self.fs, 1)
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Recognized digit")
        dlg.setText("Our GMM model recognized in your recording digit with highest probability: " + str(result))
        dlg.setStandardButtons(QMessageBox.Ok)
        dlg.setIcon(QMessageBox.Information)
        dlg.exec()

    def speaker_matching(self):
        result = verify(self.y, self.fs, 0)
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Matched speaker")
        dlg.setText("The voice in your recording with highest probability belongs to: " + str(result))
        dlg.setStandardButtons(QMessageBox.Ok)
        dlg.setIcon(QMessageBox.Information)
        dlg.exec()

    def clear_figure(self):
        self.canvas.fig.clf()
        self.canvas.draw()

    def close_func(self, save=False):
        if save:
            t = Track(self.y, self.fs)
            self.parent.tracks[self.i] = t
            self.parent.draw_osc(t, self.parent.parse_osc(self.i + 1))
        self.close()
