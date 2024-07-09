from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtCore import QFile, QTimer
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QTextCursor

import os

import sys
from pathlib import Path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))
from functions.server import startServer, stopServer

class ServerWindow(QMainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setObjectName("ServerWindow")
        self.setWindowTitle("taskZen - Server")

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("src/gui/serverWindow.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Set the UI geometry
        self.setGeometry(self.ui.geometry())

        # Connect buttons
        self.ui.runBtn.clicked.connect(self.runServer)
        self.ui.stopBtn.clicked.connect(self.stopServer)

        # Create a QTimer object for updating the server output
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateOutput)
        self.timer.start(1000)
        self.updateOutput()

        self.show()

    def runServer(self):
        print(startServer())

    def stopServer(self):
        print(stopServer())

    def updateOutput(self) -> None:
        logFile = os.getenv('XDG_CACHE_HOME', default=os.path.expanduser('~/.cache')) + '/taskZen/server.log'
        with open(logFile, 'r') as f:
            # Calculate new scroll bar position
            scrollbar = self.ui.serverOutput.verticalScrollBar()
            currentPos = scrollbar.value()
            maxPos = scrollbar.maximum()
            threshold = scrollbar.pageStep() / 4
            closeToBottom = (maxPos - currentPos) <= threshold

            # Update the text
            logContent = f.read()
            self.ui.serverOutput.setPlainText(logContent)

            # Set scroll bar position
            if closeToBottom:
                self.ui.serverOutput.moveCursor(QTextCursor.End)
            else:
                scrollbar.setValue(currentPos)
