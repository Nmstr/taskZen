from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from script.moduleEntry import ModuleWidget
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QScrollArea, QSpacerItem


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
        self.ui.addTap.clicked.connect(lambda: self.addModule('tap'))
        self.ui.addPress.clicked.connect(lambda: self.addModule('press'))
        self.ui.addRelease.clicked.connect(lambda: self.addModule('release'))
        self.ui.addWait.clicked.connect(lambda: self.addModule('wait'))
        self.ui.addMoveRelative.clicked.connect(lambda: self.addModule('move-relative'))
        self.ui.addMoveAbsolute.clicked.connect(lambda: self.addModule('move-absolute'))
        self.ui.addExec.clicked.connect(lambda: self.addModule('exec'))
        self.ui.addLoop.clicked.connect(lambda: self.addModule('loop'))
        self.ui.addIf.clicked.connect(lambda: self.addModule('if'))
        self.ui.addModifyVariable.clicked.connect(lambda: self.addModule('modify-variable'))

    def addModule(self, moduleType: str) -> None:
        widget = ModuleWidget(self, moduleType)
        container = self.ui.scriptAreaContent
        container.layout().addWidget(widget) # Add the widget
        container.setMinimumHeight(container.minimumHeight() + 110) # Increase the height of its container

    def openAsSecondaryWindow(self, parent: QWidget = None) -> None:
        window = ScriptWindow(parent)
        window.setWindowTitle(self.windowTitle())
        window.show()
