from PySide6.QtWidgets import QMainWindow, QWidget, QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import os

class ScriptWindow(QMainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("taskZen - Script")
        self.filepath = None

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

        self.show()


    def saveScript(self) -> None:
        outputText = 'Saving script...\n'
        self.ui.sideText.setText(outputText)
        scriptData = self.ui.scriptInput.toPlainText()

        if self.filepath is None:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            self.filepath, _ = QFileDialog.getSaveFileName(self, "Save Script", os.path.expanduser("~/.config/taskZen/scripts"), "Yaml Files (*.yaml)", options=options)
            if self.filepath == '':
                return

        with open(self.filepath, 'w') as f:
            f.write(scriptData)

        outputText = 'Script saved\n'
        self.ui.sideText.setText(outputText)

    def runScript(self) -> None:
        print('run script')
