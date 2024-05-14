from PySide6.QtCore import QPersistentModelIndex, QSize, Qt, QEvent, Signal, QModelIndex
from PySide6.QtWidgets import QStyleOptionViewItem, QStyledItemDelegate
from PySide6.QtGui import QMouseEvent, QFontMetrics

class TableItemDelegate(QStyledItemDelegate):
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

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> QSize:
        kaomoji = index.data(Qt.ItemDataRole.DisplayRole)
        opt = option
        self.initStyleOption(opt, index)
        
        font_metrics = QFontMetrics(opt.font)
        text_width = font_metrics.horizontalAdvance(kaomoji)
        column_width = option.rect.width()
        num_lines = text_width // column_width + 1
        font_height = font_metrics.height()
        height = num_lines * font_height
        return QSize(option.rect.width(), height)