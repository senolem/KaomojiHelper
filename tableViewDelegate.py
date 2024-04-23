from PySide6.QtCore import Qt, QEvent, Signal, QModelIndex
from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtGui import QMouseEvent

class TableViewDelegate(QStyledItemDelegate):
    kaomojiClicked = Signal(QModelIndex)
    
    def __init__(self, parent=None):
        super().__init__(parent)

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.Type.MouseButtonRelease:
            mouseEvent = QMouseEvent(event)
            if mouseEvent.button() == Qt.MouseButton.LeftButton:
                if index.column() == 0:
                    self.kaomojiClicked.emit(index)
                    return True
        return super().editorEvent(event, model, option, index)