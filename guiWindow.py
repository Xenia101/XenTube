import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'XenTube'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 320
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Download button
        self.download_button = QPushButton("Download", self)
        self.download_button.clicked.connect(self.btn_download)
        
        # Input text
        self.URLinput = QLineEdit(self)

        # Progress Bar
        self.pbar = QProgressBar(self)
        self.timer = QBasicTimer()
        self.step = 0

        # Layout
        self.createGridLayout()
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        
        self.show()

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.download_button.setText("Finished")
            return
        
        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QGridLayout()
        layout.setColumnStretch(1, 3)

        layout.addWidget(self.URLinput, 0, 1)
        layout.addWidget(self.pbar, 1, 1)
        layout.addWidget(self.download_button, 2, 1)

        self.horizontalGroupBox.setLayout(layout)

    @pyqtSlot()
    def btn_download(self):
        print("hello")
        if self.timer.isActive():
            self.timer.stop()
            self.download_button.setText("Start")
        else:
            self.timer.start(100, self)
            self.download_button.setText("Stop")