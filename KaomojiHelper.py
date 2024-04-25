import sys
import json
from pynput import keyboard
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QFrame,
    QGraphicsEffect,
    QHeaderView
)
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QStandardItemModel, QStandardItem
from ui import Ui_Form
from keybinds import Keybinds
from tabs import Tabs
from tableViewDelegate import TableViewDelegate

class KaomojiHelper(QObject):
    def __init__(self):
        super().__init__()
        # Data
        self.kaomojis = {}
        self.recentKaomojis = {}
        self.favorites = {}
        self.resultsPerPage: int = 10
        self.maxRecentKaomojis: int = 100

    def load(self):
        kaomojis = {}
        with open('kaomojis.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for kaomoji, info in data.items():
                tags = info.get('tags')
                if isinstance(kaomoji, str) and isinstance(tags, list) and all(isinstance(tag, str) for tag in tags):
                    kaomojis[kaomoji] = tags
                else:
                    raise ValueError("Invalid structure in JSON data.")
        return kaomojis

class MainWindow(QWidget):
    keyboardSignal = Signal(Keybinds) # signal for keybinds callbacks to be executed in main thread instead of keyboard monitoring thread

    def __init__(self, kaomojiHelper: KaomojiHelper, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mainUI = Ui_Form()
        kaomojiHelper.kaomojis = kaomojiHelper.load()
        self.mainUI.setupUi(self)

        # Data
        self.kaomojiHelper = kaomojiHelper
        self.currentTab: Tabs = Tabs.Search
        self.searchCurrentPage: int = 1
        self.recentlyUsedCurrentPage: int = 1
        self.favoritesCurrentPage: int = 1
        self.searchResults: list[tuple[str, list[str]]] = []
        self.recentlyUsedResults: list[tuple[str, list[str]]] = []
        self.favoritesResults: list[tuple[str, list[str]]] = []

        # For keyboard input and monitoring
        self.controller: keyboard.Controller = keyboard.Controller()
        self.listener: keyboard.Listener = keyboard.Listener(onRelease=self.onRelease)
        self.listener.start()

        self.keyboardSignal.connect(self.keybindsCallback)

        # Search model
        self.searchModel = QStandardItemModel()
        self.recentlyUsedModel = QStandardItemModel()
        self.favoritesModel = QStandardItemModel()
        self.mainUI.SearchTableView.setModel(self.searchModel)
        self.mainUI.SearchTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.mainUI.RecentlyUsedTableView.setModel(self.recentlyUsedModel)
        self.mainUI.RecentlyUsedTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.mainUI.FavoritesTableView.setModel(self.favoritesModel)
        self.mainUI.FavoritesTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Delegate for table view actions
        self.tableViewDelegate = TableViewDelegate()
        self.mainUI.SearchTableView.verticalHeader().hide()
        self.mainUI.SearchTableView.setItemDelegate(self.tableViewDelegate)
        self.mainUI.RecentlyUsedTableView.verticalHeader().hide()
        self.mainUI.RecentlyUsedTableView.setItemDelegate(self.tableViewDelegate)
        self.mainUI.FavoritesTableView.verticalHeader().hide()
        self.mainUI.FavoritesTableView.setItemDelegate(self.tableViewDelegate)
        self.tableViewDelegate.kaomojiClicked.connect(self.insertKaomoji)

        # Connect UI
        self.mainUI.SearchLineEdit.textChanged.connect(self.searchChanged)
        self.mainUI.TabsWidget.currentChanged.connect(self.tabChanged)

        self.mainUI.SearchFirstButton.clicked.connect(self.firstPage)
        self.mainUI.SearchPreviousButton.clicked.connect(self.previousPage)
        self.mainUI.SearchNextButton.clicked.connect(self.nextPage)
        self.mainUI.SearchLastButton.clicked.connect(self.lastPage)

        self.mainUI.RecentlyUsedFirstButton.clicked.connect(self.firstPage)
        self.mainUI.RecentlyUsedPreviousButton.clicked.connect(self.previousPage)
        self.mainUI.RecentlyUsedNextButton.clicked.connect(self.nextPage)
        self.mainUI.RecentlyUsedLastButton.clicked.connect(self.lastPage)

        self.mainUI.FavoritesFirstButton.clicked.connect(self.firstPage)
        self.mainUI.FavoritesPreviousButton.clicked.connect(self.previousPage)
        self.mainUI.FavoritesNextButton.clicked.connect(self.nextPage)
        self.mainUI.FavoritesLastButton.clicked.connect(self.lastPage)

        self.updateTab()

    def insertKaomoji(self, index):
        model = self.getModel()
    
        kaomoji = model.itemFromIndex(index).text()
    
        self.showMinimized()
        self.controller.type(kaomoji)
    
        recentKaomojis = self.kaomojiHelper.recentKaomojis
        if kaomoji not in recentKaomojis:
            recentKaomojis[kaomoji] = self.kaomojiHelper.kaomojis.get(kaomoji, [])
    
        recentKaomojis = dict(list(recentKaomojis.items())[-self.kaomojiHelper.maxRecentKaomojis:])
        self.kaomojiHelper.recentKaomojis = recentKaomojis
        self.updateTab(Tabs.RecentlyUsed)

    def onRelease(self, key: keyboard.Key):
        if hasattr(key, 'char'):
            if (key.char == 'k'):
                self.keyboardSignal.emit(Keybinds.Show)
        if key == keyboard.Key.esc:
            self.keyboardSignal.emit(Keybinds.Hide)
        if key == keyboard.Key.left:
            self.keyboardSignal.emit(Keybinds.Prev)
        if key == keyboard.Key.right:
            self.keyboardSignal.emit(Keybinds.Next)

    def keybindsCallback(self, key: Keybinds):
        if key == Keybinds.Show:
            self.show()
        if key == Keybinds.Hide:
            self.hide()
        if key == Keybinds.Prev:
            self.previousPage()
        if key == Keybinds.Next:
            self.nextPage()

    def previousPage(self):
        currentPage = self.getCurrentPage()

        if currentPage > 1:
            self.setCurrentPage(currentPage - 1)
            self.updateTab()

    def nextPage(self):
        results = self.getResults()
        totalPages = (len(results) + self.kaomojiHelper.resultsPerPage - 1) // self.kaomojiHelper.resultsPerPage
        currentPage = self.getCurrentPage()

        if currentPage < totalPages:
            self.setCurrentPage(currentPage + 1)
            self.updateTab()

    def firstPage(self):
        currentPage = self.getCurrentPage()

        if currentPage != 1:
            self.setCurrentPage(1)
            self.updateTab()

    def lastPage(self):
        results = self.getResults()
        totalResults = len(results)
        totalPages = (totalResults + self.kaomojiHelper.resultsPerPage - 1) // self.kaomojiHelper.resultsPerPage
        currentPage = self.getCurrentPage()

        if currentPage != totalPages:
            self.setCurrentPage(totalPages)
            self.updateTab()

    def searchChanged(self, text):
        self.search(text)

    def tabChanged(self, index):
        self.currentTab = Tabs(index)

    def search(self, query: str):
        searchList = self.getSearchList()
        results = self.getResults()

        results.clear()
        for kaomoji, tags in searchList.items():
            if query.lower() in ' '.join(tags).lower():
                results.append((kaomoji, tags))
        self.setCurrentPage(1)
        self.updateTab()

    def updateSearch(self, currentPage: int, tab=None):
        results = self.getResults(tab)
        model = self.getModel(tab)
        model.clear()

        searchList = self.getSearchList(tab)
        startIndex = (currentPage - 1) * self.kaomojiHelper.resultsPerPage
        endIndex = startIndex + self.kaomojiHelper.resultsPerPage

        if not self.mainUI.SearchLineEdit.text().strip():
            results.clear()
            results += searchList.items()
            displayedResults = results[startIndex:endIndex]
        else:
            if not results:
                displayedResults = []
            else:
                displayedResults = results[startIndex:endIndex]

        model.setHorizontalHeaderLabels(["Kaomoji", "Tags"])

        for kaomoji, tags in displayedResults:
            tagsJoined = ', '.join(tags)

            kaomojiItem = QStandardItem(kaomoji)
            tagsItem = QStandardItem(tagsJoined)
            kaomojiItem.setEditable(False)
            tagsItem.setEditable(False)

            model.appendRow([kaomojiItem, tagsItem])

    def updateStatus(self, label: QLabel, currentPage: int, tab=None):
        results = self.getResults(tab)
        totalResults = len(results)

        if not results:
            label.setText('0-0 results | 0 (total)')
            return

        startIndex = (currentPage - 1) * self.kaomojiHelper.resultsPerPage + 1
        endIndex = min(startIndex + self.kaomojiHelper.resultsPerPage - 1, totalResults)
        label.setText(f'{startIndex}-{endIndex} results | {totalResults} (total)')
    
    def updateTab(self, tab=None):
        label: QLabel
        currentPage: int

        if tab is None:
            tab = self.currentTab
        if tab not in Tabs:
            return
        if tab == Tabs.Search:
            label = self.mainUI.SearchStatusLabel
            currentPage = self.searchCurrentPage
        if tab == Tabs.RecentlyUsed:
            label = self.mainUI.RecentlyUsedStatusLabel
            currentPage = self.recentlyUsedCurrentPage
        if tab == Tabs.Favorites:
            label = self.mainUI.FavoritesStatusLabel
            currentPage = self.favoritesCurrentPage

        self.updateSearch(currentPage, tab)
        self.updateStatus(label, currentPage, tab)

    def setCurrentPage(self, page: int, tab=None):
        if tab is None:
            tab = self.currentTab
        if tab == Tabs.Search:
            self.searchCurrentPage = page
        if tab == Tabs.RecentlyUsed:
            self.recentlyUsedCurrentPage = page
        if tab == Tabs.Favorites:
            self.favoritesCurrentPage = page

    def getCurrentPage(self, tab=None) -> int:
        if tab is None:
            tab = self.currentTab
        currentPage: int
        if tab == Tabs.Search:
            currentPage = self.searchCurrentPage
        if tab == Tabs.RecentlyUsed:
            currentPage = self.recentlyUsedCurrentPage
        if tab == Tabs.Favorites:
           currentPage = self.favoritesCurrentPage
        return currentPage

    def getResults(self, tab=None) -> list[str]:
        if tab is None:
            tab = self.currentTab
        results: list[str]
        if tab == Tabs.Search:
            results = self.searchResults
        if tab == Tabs.RecentlyUsed:
            results = self.recentlyUsedResults
        if tab == Tabs.Favorites:
           results = self.favoritesResults
        return results

    def getModel(self, tab=None) -> QStandardItemModel:
        if tab is None:
            tab = self.currentTab
        model: QStandardItemModel
        if tab == Tabs.Search:
            model = self.searchModel
        if tab == Tabs.RecentlyUsed:
            model = self.recentlyUsedModel
        if tab == Tabs.Favorites:
           model = self.favoritesModel
        return model

    def getSearchList(self, tab=None) -> dict:
        if tab is None:
            tab = self.currentTab
        if tab == Tabs.Search:
            searchList = self.kaomojiHelper.kaomojis
        if tab == Tabs.RecentlyUsed:
            searchList = self.kaomojiHelper.recentKaomojis
        if tab == Tabs.Favorites:
            searchList = self.kaomojiHelper.favorites
        return searchList

    def center(self):
        frameGeometry = self.frameGeometry()
        screen = self.window().windowHandle().screen()
        centerLocation = screen.geometry().center()
        frameGeometry.moveCenter(centerLocation)
        self.move(frameGeometry.topLeft())

def main():
    kaomojiHelper = KaomojiHelper()
    app = QApplication(sys.argv)
    mainWindow = MainWindow(kaomojiHelper)
    mainWindow.show()
    app.exec()
    mainWindow.center()

if __name__ == '__main__':
    main()
