from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFrame
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from scriptWindow import ScriptWindow

class ScriptEntryWidget(QFrame):
    def __init__(self, parent, scriptData: dict, filepath: str) -> None:
        super().__init__()
        self.setObjectName("scriptEntryWidget")

        self.homeWindow = parent
        self.scriptData = scriptData
        self.filepath = filepath

        # Load the UI file
        ui_file = QFile("src/gui/homeDisplay/scriptEntry.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()


        # Add the loaded widget to the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.ui)

        # Set the labels
        self.ui.scriptNameLabel.setText(scriptData['name'])

    def mousePressEvent(self, event):
        scriptWindow = ScriptWindow(self, self.filepath)
