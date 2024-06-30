from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from homeDisplay.scriptEntry import ScriptEntryWidget
from scriptWindow import ScriptWindow

import yaml
import os

class HomwWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("taskZen - Home")

        with open('src/gui/style.qss', 'r') as f:
            app.setStyleSheet(f.read())

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("src/gui/homeWindow.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        
        # Set the UI geometry
        self.setGeometry(self.ui.geometry())

        # Connect buttons
        self.ui.createScriptBtn.clicked.connect(self.createScript)

        self.loadScripts()

    def loadScripts(self) -> None:
        for filename in os.listdir(os.path.expanduser("~/.config/taskZen/scripts")):
            if filename.endswith(".yaml"):
                scriptData = yaml.safe_load(open(os.path.expanduser(f"~/.config/taskZen/scripts/{filename}")))
                scriptEntry = ScriptEntryWidget(scriptData)
                self.ui.scriptSideContent.layout().addWidget(scriptEntry)

    def createScript(self) -> None:
        scriptWindow = ScriptWindow()
        scriptWindow.openAsSecondaryWindow(self)

if __name__ == "__main__":
    app = QApplication([])
    homeWindow = HomwWindow()
    homeWindow.show()
    app.exec()
