from PySide6.QtWidgets import QFrame, QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

"""class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.iconWidget = IconWidget('your-icon-name')
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.iconWidget)
        self.resize(200, 200)  # Adjust size as needed"""

class ServerOffline(QFrame):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setObjectName("ServerWindow")

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("src/gui/serverGui/serverOffline.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Set the UI geometry
        self.setGeometry(self.ui.geometry())

        self.show()
