from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from homeDisplay.entryWidget import EntryWidget
from scriptWindow import ScriptWindow
from deviceWindow import DeviceWindow

import yaml
import os

class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("HomeWindow")
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
        self.ui.createScriptBtn.clicked.connect(lambda: ScriptWindow(self))
        self.ui.createDeviceBtn.clicked.connect(lambda: DeviceWindow(self))
        self.ui.refreshBtn.clicked.connect(self.refreshEntries)

        self.refreshEntries()

    def refreshEntries(self) -> None:
        layout = self.ui.scriptSideContent.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            self.ui.scriptSideContent.setFixedHeight(self.ui.scriptSideContent.height() - 75)

        layout = self.ui.deviceSideContent.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            self.ui.deviceSideContent.setFixedHeight(self.ui.deviceSideContent.height() - 75)

        self.loadEntries('scripts', '~/.config/taskZen/scripts')
        self.loadEntries('devices', '~/.config/taskZen/devices')

    def loadEntries(self, target, directory) -> None:
        for filename in os.listdir(os.path.expanduser(directory)):
            if filename.endswith(".yaml"):
                filepath = os.path.expanduser(f"{directory}/{filename}")
                entryData = yaml.safe_load(open(filepath))
                if type(entryData) == dict:
                    entryName = entryData.get('name', 'Unnamed')
                else:
                    entryName = 'Unnamed'

                scriptEntry = EntryWidget(self, target, entryName, filepath)
                if target == 'scripts':
                    self.ui.scriptSideContent.layout().addWidget(scriptEntry)
                    self.ui.scriptSideContent.setFixedHeight(self.ui.scriptSideContent.height() + 75)
                elif target == 'devices':
                    self.ui.deviceSideContent.layout().addWidget(scriptEntry)
                    self.ui.deviceSideContent.setFixedHeight(self.ui.deviceSideContent.height() + 75)

if __name__ == "__main__":
    app = QApplication([])
    homeWindow = HomeWindow()
    homeWindow.show()
    app.exec()
