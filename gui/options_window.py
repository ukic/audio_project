from PyQt5.QtWidgets import QDialog, QComboBox, QLabel, QDialogButtonBox, QVBoxLayout


class OptionsWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.value = 2

        self.setWindowTitle("Choose track")

        self.cbox = QComboBox()
        for i in range(1, 6):
            self.cbox.addItem(str(i))

        q_btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(q_btn)
        self.buttonBox.accepted.connect(self.accept_func)
        self.buttonBox.rejected.connect(self.reject_func)

        self.layout = QVBoxLayout()
        message = QLabel("Choose track: ")
        self.layout.addWidget(message)
        self.layout.addWidget(self.cbox)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept_func(self):
        self.value = self.cbox.currentText()
        self.accept()

    def reject_func(self):
        self.value = self.cbox.currentText()
        self.reject()
