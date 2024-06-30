from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class ScriptWindow(QMainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("taskZen - Script")

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("src/gui/scriptWindow.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Set the UI geometry
        self.setGeometry(self.ui.geometry())

        # Connect buttons
        self.ui.saveBtn.clicked.connect(self.saveScript)
        self.ui.runBtn.clicked.connect(self.runScript)

    def saveScript(self) -> None:
        scriptData = self.ui.scriptInput.toPlainText()
        print(scriptData)
        with open('script.txt', 'w') as f:
            f.write(scriptData)

    def runScript(self) -> None:
        print('run script')

    def openAsSecondaryWindow(self, parent: QWidget = None) -> None:
        window = ScriptWindow(parent)
        window.setWindowTitle(self.windowTitle())
        window.show()
