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
from tableItemDelegate import TableItemDelegate
from tabData import TabData

class MainWindow(QWidget):
    keyboardSignal = Signal(Keybinds) # signal for keybinds callbacks to be executed in main thread instead of keyboard monitoring thread

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Data
        self.searchData = TabData(Tabs.Search)
        self.recentlyUsedData = TabData(Tabs.RecentlyUsed)
        self.favoritesData = TabData(Tabs.Favorites)
        self.settingsData = TabData(Tabs.Settings)
        self.currentTab = TabData()

        # Initialization
        self.mainUI = Ui_Form()
        self.searchData.list = self.load()
        self.mainUI.setupUi(self)
        
        # Assign UI Labels to tabs
        self.searchData.label = self.mainUI.SearchStatusLabel
        self.recentlyUsedData.label = self.mainUI.RecentlyUsedStatusLabel
        self.favoritesData.label = self.mainUI.FavoritesStatusLabel
        
        # Assign table views to tabs
        self.searchData.tableView = self.mainUI.SearchTableView
        self.recentlyUsedData.tableView = self.mainUI.RecentlyUsedTableView
        self.favoritesData.tableView = self.mainUI.FavoritesTableView

        # For keyboard input and monitoring
        self.controller: keyboard.Controller = keyboard.Controller()
        self.listener: keyboard.Listener = keyboard.Listener(onRelease=self.onRelease)
        self.listener.start()

        self.keyboardSignal.connect(self.keybindsCallback)

        # Search model
        self.mainUI.SearchTableView.setModel(self.searchData.model)
        self.mainUI.SearchVerticalLayout.addWidget(self.mainUI.SearchTableView)
        self.mainUI.SearchTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.mainUI.RecentlyUsedTableView.setModel(self.recentlyUsedData.model)
        self.mainUI.RecentlyUsedTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.mainUI.FavoritesTableView.setModel(self.favoritesData.model)
        self.mainUI.FavoritesTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Delegate for table view actions
        self.tableItemDelegate = TableItemDelegate()
        self.mainUI.SearchTableView.verticalHeader().hide()
        self.mainUI.SearchTableView.setItemDelegateForColumn(0, self.tableItemDelegate)
        self.mainUI.RecentlyUsedTableView.verticalHeader().hide()
        self.mainUI.RecentlyUsedTableView.setItemDelegate(self.tableItemDelegate)
        self.mainUI.FavoritesTableView.verticalHeader().hide()
        self.mainUI.FavoritesTableView.setItemDelegate(self.tableItemDelegate)
        self.tableItemDelegate.kaomojiClicked.connect(self.insertKaomoji)

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

        self.currentTab = self.searchData
        self.updateTab(Tabs.Search)
        self.updateTab(Tabs.RecentlyUsed)
        self.updateTab(Tabs.Favorites)
        
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

    def insertKaomoji(self, index):
        kaomoji = self.currentTab.model.itemFromIndex(index).text()
    
        self.showMinimized()
        self.controller.type(kaomoji)
    
        recentKaomojis = self.recentlyUsedData.list
        if kaomoji not in recentKaomojis:
            recentKaomojis[kaomoji] = self.searchData.list.get(kaomoji, [])
    
        recentKaomojis = dict(list(recentKaomojis.items())[-self.recentlyUsedData.limit:])
        self.recentlyUsedData.list = recentKaomojis
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
        currentPage = self.currentTab.currentPage

        if currentPage > 1:
            self.currentTab.currentPage = currentPage - 1
            self.updateTab()

    def nextPage(self):
        results = self.currentTab.results
        resultsPerPage = self.currentTab.resultsPerPage
        currentPage = self.currentTab.currentPage

        totalPages = (len(results) + resultsPerPage - 1) // resultsPerPage
        if currentPage < totalPages:
            self.currentTab.currentPage = currentPage + 1
            self.updateTab()

    def firstPage(self):
        if self.currentTab.currentPage != 1:
            self.currentTab.currentPage = 1
            self.updateTab()

    def lastPage(self):
        results = self.currentTab.results
        resultsPerPage = self.currentTab.resultsPerPage
        currentPage = self.currentTab.currentPage

        totalResults = len(results)
        totalPages = (totalResults + resultsPerPage - 1) // resultsPerPage

        if currentPage != totalPages:
            self.currentTab.currentPage = totalPages
            self.updateTab()

    def searchChanged(self, text):
        self.search(text)

    def tabChanged(self, index):
        self.currentTab.searchQuery = self.mainUI.SearchLineEdit.text()
        currentTab = Tabs(index)
        
        if currentTab == Tabs.Search:
            self.currentTab = self.searchData
        if currentTab == Tabs.RecentlyUsed:
            self.currentTab = self.recentlyUsedData
        if currentTab == Tabs.Favorites:
            self.currentTab = self.favoritesData
        if currentTab == Tabs.Settings:
            self.currentTab = self.settingsData
        self.mainUI.SearchLineEdit.setText(self.currentTab.searchQuery)

    def search(self, query: str):
        self.currentTab.results.clear()
        for kaomoji, tags in self.currentTab.list.items():
            if query.lower() in ' '.join(tags).lower():
                self.currentTab.results.append((kaomoji, tags))
        self.currentTab.currentPage = 1
        self.updateTab()

    def updateSearch(self, data: TabData):
        data.model.clear()

        startIndex = (data.currentPage - 1) * data.resultsPerPage
        endIndex = startIndex + data.resultsPerPage

        if not self.mainUI.SearchLineEdit.text().strip():
            data.results.clear()
            data.results += data.list.items()
            displayedResults = data.results[startIndex:endIndex]
        else:
            if not data.results:
                displayedResults = []
            else:
                displayedResults = data.results[startIndex:endIndex]

        data.model.setHorizontalHeaderLabels(["Kaomoji", "Tags"])

        for kaomoji, tags in displayedResults:
            tagsJoined = ', '.join(tags)

            kaomojiItem = QStandardItem(kaomoji)
            tagsItem = QStandardItem(tagsJoined)
            kaomojiItem.setEditable(False)
            tagsItem.setEditable(False)

            data.model.appendRow([kaomojiItem, tagsItem])
        
        data.tableView.resizeRowsToContents()

    def updateStatus(self, data: TabData):
        results = data.results
        totalResults = len(results)

        if not results:
            data.label.setText('0-0 results | 0 (total)')
            return

        startIndex = (data.currentPage - 1) * data.resultsPerPage + 1
        endIndex = min(startIndex + data.resultsPerPage - 1, totalResults)
        data.label.setText(f'{startIndex}-{endIndex} results | {totalResults} (total)')
    
    def updateTab(self, tab=None):
        data: TabData

        if tab is None:
            tab = self.currentTab.tab
        if tab not in Tabs:
            return
        if tab == Tabs.Search:
            data = self.searchData
        if tab == Tabs.RecentlyUsed:
            data = self.recentlyUsedData
        if tab == Tabs.Favorites:
            data = self.favoritesData

        self.updateSearch(data)
        self.updateStatus(data)

    def center(self):
        frameGeometry = self.frameGeometry()
        screen = self.window().windowHandle().screen()
        centerLocation = screen.geometry().center()
        frameGeometry.moveCenter(centerLocation)
        self.move(frameGeometry.topLeft())

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()
    mainWindow.center()

if __name__ == '__main__':
    main()
