from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtCore import QFile, QTimer
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QTextCursor
from PySide6.QtCore import QPoint

from serverGui.serverOffline import ServerOffline

import os

import sys
from pathlib import Path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))
from functions.server import startServer, stopServer, pingServer

class ServerWindow(QMainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setObjectName("ServerWindow")
        self.setWindowTitle("taskZen - Server")
        
        self.serverOfflinePopover = None

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

        self.show()

        # Create a QTimer object for updating the server output
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateOutput)
        self.timer.start(1000)
        self.updateOutput()

        self.createServerOffline()
        if pingServer()[0]:
            self.removeServerOffline()

    def runServer(self):
        print(startServer())
        self.removeServerOffline()

    def stopServer(self):
        print(stopServer())
        self.showServerOffline()

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

    def createServerOffline(self) -> None:
        """
        Shows the server offline popover.
        """
        self.serverOfflinePopover = ServerOffline(self)

        # Calculate the position of the popover
        outputPos = self.ui.serverOutput.mapToGlobal(self.ui.serverOutput.pos())
        print(self.ui.serverOutput.pos())
        print(outputPos)
        popoverPosX = outputPos.x() - (500 / 2) + (self.ui.serverOutput.width() / 2)
        popoverPosY = outputPos.y() - (300 / 2) + (self.ui.serverOutput.height() / 2)
        
        # Set the position and size of the popover
        self.serverOfflinePopover.setGeometry(int(popoverPosX), int(popoverPosY), 500, 300)
        self.serverOfflinePopover.show()

    def showServerOffline(self) -> None:
        """
        Shows the server offline popover.
        """
        self.serverOfflinePopover.setVisible(True)

    def removeServerOffline(self) -> None:
        """
        Removes the server offline popover.
        """
        self.serverOfflinePopover.setVisible(False)
