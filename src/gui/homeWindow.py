from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from scriptWindow import ScriptWindow

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

    def createScript(self) -> None:
        scriptWindow = ScriptWindow()
        scriptWindow.openAsSecondaryWindow(self)

if __name__ == "__main__":
    app = QApplication([])
    homeWindow = HomwWindow()
    homeWindow.show()
    app.exec()
