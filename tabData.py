from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import (
    QLabel
)
from tabs import Tabs

class TabData():
    def __init__(self, tab=None):
        self.list = {}
        self.results: list[tuple[str, list[str]]] = []
        self.model = QStandardItemModel()
        self.currentPage: int = 1
        self.resultsPerPage: int = 10
        self.limit: int = 100
        self.tab = tab
        self.label: QLabel = QLabel()
        self.searchQuery = str()