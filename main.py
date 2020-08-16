from typing import *
import downloader
import guiWindow
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = guiWindow.App()
    sys.exit(app.exec_())
    URL: str = "https://www.youtube.com/watch?v=LJOP9AF9ImM&list=RDLJOP9AF9ImM&start_radio=1&t=1"
    outpath: str = "storage"
    downloader.download(URL, outpath)
    