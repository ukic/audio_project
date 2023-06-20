from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QPushButton, QLabel, QDialogButtonBox, \
    QSpinBox, QMessageBox
from signal_generator.signal_generator import SignalType, generate_signal


class SignalGeneratorWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Signal Generator")

        self.layout = QVBoxLayout()

        # TRACK

        self.trackLayout = QHBoxLayout()
        self.trackLabel = QLabel("Select track: ")
        self.track = QComboBox()
        for i in range(1, 6):
            self.track.addItem(str(i))

        self.trackLayout.addWidget(self.trackLabel)
        self.trackLayout.addWidget(self.track)
        self.layout.addLayout(self.trackLayout)

        # SIGNAL TYPE

        self.signalTypeLayout = QHBoxLayout()
        self.signalTypeLabel = QLabel("Select signal type: ")
        self.signalType = QComboBox()
        for s in SignalType:
            self.signalType.addItem(str(s)[7:])

        self.signalTypeLayout.addWidget(self.signalTypeLabel)
        self.signalTypeLayout.addWidget(self.signalType)
        self.layout.addLayout(self.signalTypeLayout)

        # DURATION

        self.timeLayout = QHBoxLayout()
        self.timeLabel = QLabel("Enter duration: ")

        self.timeSpinBox = QSpinBox()
        self.timeSpinBox.setSingleStep(1)
        self.timeSpinBox.setMinimum(1)
        self.timeSpinBox.setMaximum(100000)
        self.timeSpinBox.setValue(1000)

        self.timeUnit = QComboBox()
        self.timeUnit.addItem("miliseconds")
        self.timeUnit.addItem("samples")

        self.timeLayout.addWidget(self.timeLabel)
        self.timeLayout.addWidget(self.timeSpinBox)
        self.timeLayout.addWidget(self.timeUnit)
        self.layout.addLayout(self.timeLayout)

        # SAMPLING RATE
        self.srLayout = QHBoxLayout()
        self.srLabel = QLabel("Enter sampling rate [Hz]: ")

        self.srSpinBox = QSpinBox()
        self.srSpinBox.setSingleStep(1)
        self.srSpinBox.setMinimum(10)
        self.srSpinBox.setMaximum(200000)
        self.srSpinBox.setValue(4000)

        self.srLayout.addWidget(self.srLabel)
        self.srLayout.addWidget(self.srSpinBox)
        self.layout.addLayout(self.srLayout)

        # FREQUENCY
        self.freqLayout = QHBoxLayout()
        self.freqLabel = QLabel("Enter frequency [Hz]: ")

        self.freqSpinBox = QSpinBox()
        self.freqSpinBox.setSingleStep(1)
        self.freqSpinBox.setMinimum(10)
        self.freqSpinBox.setMaximum(50000)
        self.freqSpinBox.setValue(1000)

        self.freqLayout.addWidget(self.freqLabel)
        self.freqLayout.addWidget(self.freqSpinBox)
        self.layout.addLayout(self.freqLayout)

        # AMPLITUDE

        self.amplLayout = QHBoxLayout()
        self.amplLabel = QLabel("Enter ampititude: ")

        self.amplSpinBox = QSpinBox()
        self.amplSpinBox.setSingleStep(1)
        self.amplSpinBox.setMinimum(-10000)
        self.amplSpinBox.setMaximum(10000)
        self.amplSpinBox.setValue(10)

        self.amplLayout.addWidget(self.amplLabel)
        self.amplLayout.addWidget(self.amplSpinBox)
        self.layout.addLayout(self.amplLayout)

        # PHASE SHIFT

        self.phasLayout = QHBoxLayout()
        self.phasLabel = QLabel("Enter phase shift: ")

        self.phasSpinBox = QSpinBox()
        self.phasSpinBox.setSingleStep(1)
        self.phasSpinBox.setMinimum(-360)
        self.phasSpinBox.setMaximum(360)
        self.phasSpinBox.setValue(0)

        self.phasLayout.addWidget(self.phasLabel)
        self.phasLayout.addWidget(self.phasSpinBox)
        self.layout.addLayout(self.phasLayout)

        # BUTTONS

        self.button = QPushButton("Generate")
        self.button.clicked.connect(self.generate_signal)
        self.layout.addWidget(self.button)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel)
        self.buttonBox.clicked.connect(self.close)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def generate_signal(self):
        i = int(self.track.currentText()) - 1
        try:
            self.parent.tracks[i] = generate_signal(self.signalType.currentText(),
                                                    self.timeSpinBox.value() / 1000,
                                                    self.srSpinBox.value(),
                                                    self.amplSpinBox.value(),
                                                    self.freqSpinBox.value(),
                                                    self.phasSpinBox.value())
            self.parent.draw_osc(self.parent.tracks[i], self.parent.parse_osc(i + 1))
        except ValueError:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Wrong parameters! Unable to generate signal!")
            dlg.setStandardButtons(QMessageBox.Ok)
            dlg.setIcon(QMessageBox.Critical)
            dlg.exec()

