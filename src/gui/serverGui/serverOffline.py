from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from customWidgets.iconDisplay import iconDisplay

class ServerOffline(QFrame):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("src/gui/serverGui/serverOffline.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Set the UI geometry
        self.setGeometry(self.ui.geometry())

        self.iconWidget = iconDisplay(iconName = 'network-offline', iconSize = 512)
        self.ui.iconContainer.layout().addWidget(self.iconWidget)

        self.show()
