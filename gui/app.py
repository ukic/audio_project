from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGroupBox, \
    QMessageBox, QFileDialog
from PyQt5 import uic
from copy import copy
from playsound import playsound

from basic.track import Track
from basic.audio_loading import import_wav, export_wav, AudioRecorder
from basic.basic_audio_modifications import add_2_tracks
from gui.options_window import OptionsWindow
from gui.signal_generator_window import SignalGeneratorWindow
from gui.modification_window import ModificationWindow
from gui.analyzer_window import AnalyzerWindow
from gui.mpl_canvas import MplCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui/mainWindow.ui', self)

        self.tracks = [Track([], -1) for _ in range(5)]

        self.actionExport.triggered.connect(self.export)
        self.actionAudioFile.triggered.connect(self.add_track)
        self.actionGenerateSignal.triggered.connect(self.generate_signal)

        self.soloButtons = [self.soloButton1, self.soloButton2, self.soloButton3, self.soloButton4, self.soloButton5]
        self.muteButtons = [self.muteButton1, self.muteButton2, self.muteButton3, self.muteButton4, self.muteButton5]

        for b in self.soloButtons:
            b.setCheckable(True)

        self.soloButton1.clicked.connect(lambda: self.solo_track(0))
        self.soloButton2.clicked.connect(lambda: self.solo_track(1))
        self.soloButton3.clicked.connect(lambda: self.solo_track(2))
        self.soloButton4.clicked.connect(lambda: self.solo_track(3))
        self.soloButton5.clicked.connect(lambda: self.solo_track(4))

        for b in self.muteButtons:
            b.setCheckable(True)

        self.recButton.clicked.connect(self.start_recording)
        self.playButton.clicked.connect(self.play)
        self.stopRecButton.clicked.connect(self.end_recording)

        self.modButton1.clicked.connect(lambda: self.modify(0))
        self.modButton2.clicked.connect(lambda: self.modify(1))
        self.modButton3.clicked.connect(lambda: self.modify(2))
        self.modButton4.clicked.connect(lambda: self.modify(3))
        self.modButton5.clicked.connect(lambda: self.modify(4))

        self.expButton1.clicked.connect(lambda: self.export_track(0))
        self.expButton2.clicked.connect(lambda: self.export_track(1))
        self.expButton3.clicked.connect(lambda: self.export_track(2))
        self.expButton4.clicked.connect(lambda: self.export_track(3))
        self.expButton5.clicked.connect(lambda: self.export_track(4))

        self.anButton1.clicked.connect(lambda: self.analyse(0))
        self.anButton2.clicked.connect(lambda: self.analyse(1))
        self.anButton3.clicked.connect(lambda: self.analyse(2))
        self.anButton4.clicked.connect(lambda: self.analyse(3))
        self.anButton5.clicked.connect(lambda: self.analyse(4))

        self.clButton1.clicked.connect(lambda: self.clear_track(0))
        self.clButton2.clicked.connect(lambda: self.clear_track(1))
        self.clButton3.clicked.connect(lambda: self.clear_track(2))
        self.clButton4.clicked.connect(lambda: self.clear_track(3))
        self.clButton5.clicked.connect(lambda: self.clear_track(4))

        # Windows
        self.analyzer = None
        self.modification = None
        self.options = None

        # Tools
        self.recorder = AudioRecorder()
        self.sg = None

        self.i = 1

    def add_track(self):
        opt = OptionsWindow(self)
        if opt.exec():
            i = int(opt.value)
            path = self.choose_read_wav_file()
            if path != '':
                self.tracks[i - 1] = import_wav(path)
                self.draw_osc(self.tracks[i - 1], self.parse_osc(i))
            else:
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Error")
                dlg.setText("No file chosen")
                dlg.setStandardButtons(QMessageBox.Ok)
                dlg.setIcon(QMessageBox.Critical)
                dlg.exec()

    def clear_track(self, idx: int):
        if -1 < idx < 5:
            self.tracks[idx] = Track([], None)
            gb = self.parse_osc(idx + 1)
            sg = gb.findChild(MplCanvas)
            if sg is not None:
                sg.setParent(None)
                del sg

    def choose_read_wav_file(self) -> str:
        path = QFileDialog.getOpenFileName(self, 'Open file',
                                               'c:\\', "(*.wav)")
        return path[0]

    def choose_write_wav_file(self) -> str:
        path = QFileDialog.getSaveFileName(self, directory='c:\\', filter="(*.wav)")
        return path[0]

    def parse_osc(self, i):
        if i == 1:
            return self.osc1
        elif i == 2:
            return self.osc2
        elif i == 3:
            return self.osc3
        elif i == 4:
            return self.osc4
        elif i == 5:
            return self.osc5
        else:
            raise ValueError

    def generate_signal(self):
        if self.sg is None:
            self.sg = SignalGeneratorWindow(self)
        self.sg.show()

    def solo_track(self, i):
        val = self.soloButtons[i].isChecked()

        for k in range(5):
            if k != i:
                self.muteButtons[k].setChecked(val)
                if val:
                    self.soloButtons[k].setChecked(not val)
            else:
                if val:
                    self.muteButtons[k].setChecked(not val)

    def export(self, path_choice=True):
        exp, fs = self.combine_tracks()
        if exp is not None:
            if path_choice:
                path = self.choose_write_wav_file()
            else:
                path = "tmp.wav"
            if path != '':
                export_wav(Track(exp, fs), path)
            else:
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Error")
                dlg.setText("No file chosen")
                dlg.setStandardButtons(QMessageBox.Ok)
                dlg.setIcon(QMessageBox.Critical)
                dlg.exec()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("No audio data on your tracks")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.setIcon(QMessageBox.Critical)
            dlg.exec()

    def export_track(self, i):
        path = self.choose_write_wav_file()
        export_wav(self.tracks[i], path)

    def modify(self, i):
        self.modification = ModificationWindow(self, copy(self.tracks[i].y), self.tracks[i].fs, i)
        self.modification.show()

    def analyse(self, i):
        self.analyzer = AnalyzerWindow(self, copy(self.tracks[i].y), self.tracks[i].fs, i)
        self.analyzer.show()

    def start_recording(self):
        opt = OptionsWindow(self)
        if opt.exec():
            self.i = int(opt.value)
            self.recorder.start_recording()

    def end_recording(self):
        self.tracks[self.i - 1] = self.recorder.stop_recording()
        self.draw_osc(self.tracks[self.i - 1], self.parse_osc(self.i))

    def combine_tracks(self):
        i = 0
        for b in self.soloButtons:
            if b.isChecked():
                return self.tracks[i].y, self.tracks[i].fs
            i += 1

        fs = -1
        for i in range(5):
            if self.tracks[i].n > 0:
                if fs == -1:
                    fs = self.tracks[i].fs
                elif fs != -1 and self.tracks[i].fs != fs:
                    dlg = QMessageBox(self)
                    dlg.setWindowTitle("Different sampling rate")
                    dlg.setText(
                        "Audio files on your tracks have different sampling rate. Are you sure you want to continue?")
                    dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    dlg.setIcon(QMessageBox.Warning)
                    button = dlg.exec()

                    if button == QMessageBox.No:
                        return [], -1

        exp = None
        for i in range(5):
            if self.tracks[i].n > 0 and not self.muteButtons[i].isChecked():
                if exp is None:
                    exp = self.tracks[i].y
                else:
                    exp = add_2_tracks(exp, self.tracks[i].y)
        return exp, fs

    def play(self):
        self.export(path_choice=False)
        playsound("tmp.wav")

    def draw_osc(self, t: Track, gb: QGroupBox):
        sg = gb.findChild(MplCanvas)
        if sg is not None:
            sg.setParent(None)
            del sg
            sl = gb.findChild(QVBoxLayout)
        else:
            sl = QVBoxLayout()
            gb.setLayout(sl)
        sc = MplCanvas(self, width=1300, height=100, dpi=100)
        ax = sc.fig.add_subplot(111)
        ax.plot(t.time, t.y)
        sc.setFixedSize(1300, 100)
        sl.addWidget(sc)
