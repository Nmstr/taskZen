from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from homeDisplay.scriptEntry import ScriptEntryWidget
from scriptWindow import ScriptWindow

import yaml
import os

class HomeWindow(QMainWindow):
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
                filepath = os.path.expanduser(f"~/.config/taskZen/scripts/{filename}")
                scriptData = yaml.safe_load(open(filepath))
                scriptEntry = ScriptEntryWidget(self, scriptData, filepath)
                self.ui.scriptSideContent.layout().addWidget(scriptEntry)
                self.ui.scriptSideContent.setMinimumHeight(self.ui.scriptSideContent.height() + 75)

    def createScript(self) -> None:
        scriptWindow = ScriptWindow(self)

if __name__ == "__main__":
    app = QApplication([])
    homeWindow = HomeWindow()
    homeWindow.show()
    app.exec()
