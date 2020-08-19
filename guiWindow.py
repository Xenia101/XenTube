import sys
import time
import requests
import checkpath
from pytube import YouTube
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

def restore(settings):
    finfo = QFileInfo(settings.fileName())
    
    if finfo.exists() and finfo.isFile():
        for w in qApp.allWidgets():
            mo = w.metaObject()
            if w.objectName() != "":
                for i in range(mo.propertyCount()):
                    name = mo.property(i).name()
                    val = settings.value("{}/{}".format(w.objectName(), name), w.property(name))
                    w.setProperty(name, val)

def save(settings):
    for w in qApp.allWidgets():
        mo = w.metaObject()
        if w.objectName() != "":
            for i in range(mo.propertyCount()):
                name = mo.property(i).name()
                settings.setValue("{}/{}".format(w.objectName(), name), w.property(name))

class App(QWidget):  
    settings = QSettings("gui.ini", QSettings.IniFormat)
    
    def __init__(self):
        super().__init__()
        self.title  = 'XenTube'
        self.left   = 100
        self.top    = 100
        self.width  = 320
        self.height = 160
        self.step   = 0
        self.filesize = 0
        self.initUI()
        
        restore(self.settings)
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # Input path
        self.pathinput = QLineEdit(self)
        self.pathinput.setPlaceholderText("Download Path")
        self.pathinput.setObjectName("pathinput")
        
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
        windowLayout.setContentsMargins(5, -1, 5, 5)
        
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        
        self.show()

    def closeEvent(self, event):
        save(self.settings)

    def progress_function(self, stream, chunk, bytes_remaining):
        if self.step >= 100:
            self.timer.stop()
            self.download_button.setEnabled(True)
            self.step = 0
            self.pbar.setValue(self.step)
            return
        
        self.step = round((1-bytes_remaining/stream.filesize)*100, 3)
        self.pbar.setValue(self.step)
        
        
    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QGridLayout()
        #layout.setColumnStretch(1, 4)
        
        layout.addWidget(self.pathinput      , 0, 1)
        layout.addWidget(self.URLinput       , 1, 1)
        layout.addWidget(self.pbar           , 2, 1)
        layout.addWidget(self.download_button, 3, 1)
        
        self.horizontalGroupBox.setLayout(layout)

    @pyqtSlot()
    def btn_download(self):
        if len(self.pathinput.text()) is not 0 and len(self.URLinput.text()) is not 0:
            path: str = self.pathinput.text()
            url: str = self.URLinput.text()
            
            c = checkpath.Checking(url, path)
            if c.check():
                try:
                    yt = YouTube(url, on_progress_callback=self.progress_function)
                except: pass
                
                video = yt.streams.first()
                video.download(output_path=path)
                
                #self.timer.start(100, self)
                #self.download_button.setEnabled(False)
            else:
                c.dircreate()
            self.URLinput.clear()