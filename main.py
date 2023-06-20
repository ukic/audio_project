from PyQt5.QtWidgets import QApplication
import sys
from gui.app import MainWindow
from sound_analysis.feature_matching import GaussianModel


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
