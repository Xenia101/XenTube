import os
import sys
import time
import requests
import checkpath
from pytube import YouTube
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets  import *

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
        
        self.nowplaying = ""
        self.playbtnenable = False
        
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
        
        # Grid Layout
        self.createGridLayout()
        
        # video list
        self.initpath = self.settings.value("pathinput")
        
        # Video
        videoWidget = QVideoWidget()
        
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        #self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.initpath + "/" + self.nowplaying)))
        #self.mediaPlayer.setVolume(30)
        
        # Controler Btns
        self.playButton = QPushButton()
        self.playButton.setEnabled(self.playbtnenable)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        
        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        
        # volume
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setValue(30)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.sliderMoved.connect(self.volumeControl)
        
        # control Layout
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.volumeSlider)
        
        # video Layout
        videolayout = QVBoxLayout()
        videolayout.addWidget(videoWidget)
        videolayout.addLayout(controlLayout)
        videolayout.addWidget(self.errorLabel)
        
        # File list view
        self.listView = QListView(self)
        self.listView.setFixedHeight(200)
        
        self.model = QStandardItemModel()
        self.listView.setModel(self.model)
        for x in os.listdir(self.initpath):
            item = QStandardItem(x)
            self.model.appendRow(item)
        
        self.listView.clicked[QModelIndex].connect(self.onclicked_item)
        
        listLayout = QHBoxLayout()        
        listLayout.addWidget(self.listView)
        
        # main Frame
        windowLayout = QVBoxLayout()
        windowLayout.setContentsMargins(5, -1, 5, 5)
        windowLayout.addWidget(self.horizontalGroupBox)
        
        windowLayout.addLayout(listLayout ) # List  View
        windowLayout.addLayout(videolayout) # Video View
        
        self.setLayout(windowLayout)
        
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect( self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        
        self.show()
    
    def onclicked_item(self, index):
        item = self.model.itemFromIndex(index)
        self.playbtnenable = True
        self.playButton.setEnabled(self.playbtnenable)
        self.nowplaying = item.text()
    
    def exitCall(self):
        sys.exit(app.exec_())
        
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.initpath + "/" + self.nowplaying)))
            self.mediaPlayer.setVolume(30)
            self.mediaPlayer.play()
            
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            
    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        
    def volumeControl(self, volume):
        self.mediaPlayer.setVolume(volume)
        
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
        
    def handleError(self):
        self.playButton.setEnabled(self.playbtnenable)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())
        
    # Downloader
    def closeEvent(self, event):
        self.settings.setValue("pathinput", self.pathinput.text())
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