from PySide6.QtGui import QPainter, QIcon
from PySide6.QtWidgets import QWidget

class iconDisplay(QWidget):
    def __init__(self, parent=None, *, iconName, iconSize=64):
        super().__init__(parent)
        self.icon = QIcon.fromTheme(iconName)
        self.iconSize = iconSize

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = self.icon.pixmap(self.iconSize, self.iconSize)
        painter.drawPixmap(self.rect(), pixmap)
