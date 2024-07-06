from PySide6.QtWidgets import QMainWindow, QWidget, QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

import os

class DeviceWindow(QMainWindow):
    def __init__(self, parent: QWidget = None, filepath: str = None) -> None:
        super().__init__(parent)
        self.setObjectName("DeviceWindow")
        self.setWindowTitle("taskZen - Device")
        self.filepath = filepath

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("src/gui/deviceWindow.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Set the UI geometry
        self.setGeometry(self.ui.geometry())

        # Connect buttons
        self.ui.saveBtn.clicked.connect(self.saveScript)

        self.show()

        # Fill with text
        if self.filepath is not None:
            with open(self.filepath, 'r') as f:
                self.ui.deviceInput.setPlainText(f.read())

    def saveScript(self) -> None:
        self.outputText = 'Saving Device...\n'
        self.ui.sideText.setText(self.outputText)
        scriptData = self.ui.deviceInput.toPlainText()

        if self.filepath is None:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            self.filepath, _ = QFileDialog.getSaveFileName(self, "Save Device", os.path.expanduser("~/.config/taskZen/devices"), "Yaml Files (*.yaml)", options=options)
            if self.filepath == '':
                return

        with open(self.filepath, 'w') as f:
            f.write(scriptData)

        self.outputText = 'Device saved\n'
        self.ui.sideText.setText(self.outputText)
