import sys
import time
import downloader
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title  = 'XenTube'
        self.left   = 100
        self.top    = 100
        self.width  = 320
        self.height = 160
        self.step   = 0
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # Input path
        self.pathinput = QLineEdit(self)
        self.pathinput.setPlaceholderText("Download Path")
        # Input URL
        self.URLinput = QLineEdit(self)
        self.URLinput.setPlaceholderText("Youtube URL")
        
        # Progress Bar
        self.pbar = QProgressBar(self)
        self.timer = QBasicTimer()
        
        # Download button
        self.download_button = QPushButton("Download", self)
        self.download_button.clicked.connect(self.btn_download)
        
        # Layout
        self.createGridLayout()
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        
        self.show()

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.download_button.setEnabled(True)
            self.step = 0
            self.pbar.setValue(self.step)
            return
        
        self.step = self.step + 10
        self.pbar.setValue(self.step)

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        
        layout.addWidget(self.pathinput      , 0, 1)
        layout.addWidget(self.URLinput       , 1, 1)
        layout.addWidget(self.pbar           , 2, 1)
        layout.addWidget(self.download_button, 3, 1)
        
        self.horizontalGroupBox.setLayout(layout)

    @pyqtSlot()
    def btn_download(self):
        if len(self.pathinput.text()) is not 0 and len(self.URLinput.text()) is not 0:
            print("download")
            
            path: str = self.pathinput.text()
            url: str = self.URLinput.text()
            
            print(path)
            print(url)
            
            yt = downloader.ytDownloader(self.URLinput.text(), self.pathinput.text())
            yt.download()
            
            self.timer.start(100, self)
            self.download_button.setEnabled(False)
