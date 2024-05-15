from PySide6.QtCore import QEvent, QObject

class ScrollEventFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Wheel:
            event.ignore()
            return True
        else:
            return super().eventFilter(obj, event)