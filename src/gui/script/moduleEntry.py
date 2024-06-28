from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QFrame

class ModuleWidget(QFrame):
    def __init__(self, parent = None, moduleName: str = None) -> None:
        super().__init__(parent)

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("src/gui/script/moduleEntry.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Set the UI geometry
        self.setGeometry(self.ui.geometry())

        # Set labels
        self.ui.moduleLabel.setText(moduleName)

    def enterEvent(self, event) -> None:
        self.ui.setStyleSheet("background-color: #282C32;")

    def leaveEvent(self, event) -> None:
        self.ui.setStyleSheet("")
