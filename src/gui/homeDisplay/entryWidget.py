from PySide6.QtWidgets import QVBoxLayout, QFrame
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from scriptWindow import ScriptWindow
from deviceWindow import DeviceWindow

class EntryWidget(QFrame):
    def __init__(self, parent, target: str, name: str, filepath: str) -> None:
        super().__init__()
        self.setObjectName("EntryWidget")

        self.homeWindow = parent
        self.target = target
        self.name = name
        self.filepath = filepath

        # Load the UI file
        ui_file = QFile("src/gui/homeDisplay/entryWidget.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()


        # Add the loaded widget to the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.ui)

        # Set the labels
        self.ui.entryNameLabel.setText(name)

    def mousePressEvent(self, event):
        if self.target == 'scripts':
            scriptWindow = ScriptWindow(self, self.filepath)
        elif self.target == 'devices':
            deviceWindow = DeviceWindow(self, self.filepath)
