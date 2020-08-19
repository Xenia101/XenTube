from typing import *
import guiWindow
import qtmodern.styles
import qtmodern.windows
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    # GUI
    app = QApplication(sys.argv)
    win = guiWindow.App()
    
    # Set Window re-Style
    qss_file = open('style.qss').read()
    win.setStyleSheet(qss_file)
    
    # Set theme..
    qtmodern.styles.dark(app)
    mw = qtmodern.windows.ModernWindow(win)    
    mw.show()
    
    sys.exit(app.exec_())
