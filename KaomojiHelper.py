import sys
import json
from pynput import keyboard
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QStyleFactory,
    QHeaderView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QFont, QKeySequence
from ui.ui import Ui_Form
from ui.tableItemDelegate import TableItemDelegate
from ui.tabData import TabData
from ui.scrollEventFilter import ScrollEventFilter
from enums.keybinds import Keybinds
from enums.tabs import Tabs
from config import Config
from keyboardListener import KeyboardListener

class MainWindow(QWidget):
    def __init__(self, config: Config, parent=None):
        super(MainWindow, self).__init__(parent)

        # Data
        self.config = config
        self.searchData = TabData(Tabs.Search)
        self.recentlyUsedData = TabData(Tabs.RecentlyUsed)
        self.favoritesData = TabData(Tabs.Favorites)
        self.settingsData = TabData(Tabs.Settings)
        self.currentTab = TabData()

        # Initialization
        self.mainUI = Ui_Form()
        self.searchData.list = self.load()
        self.mainUI.setupUi(self)
        default_tab = self.config.config.getint('GENERAL', 'default_tab')
        self.mainUI.TabsWidget.setCurrentIndex(default_tab)
        self.tabChanged(default_tab)
        
        # Populate theme combobox
        styles = QStyleFactory.keys()
        for style in styles:
            self.mainUI.ThemeComboBox.addItem(style)
            
        # Ignore scroll event on combobox
        self.scrollEventFilter = ScrollEventFilter()
        self.mainUI.FontComboBox.installEventFilter(self.scrollEventFilter)
        self.mainUI.ThemeComboBox.installEventFilter(self.scrollEventFilter)
        self.mainUI.DefaultTabComboBox.installEventFilter(self.scrollEventFilter)
        
        # Assign UI Labels to tabs
        self.searchData.label = self.mainUI.SearchStatusLabel
        self.recentlyUsedData.label = self.mainUI.RecentlyUsedStatusLabel
        self.favoritesData.label = self.mainUI.FavoritesStatusLabel
        
        # Assign table views to tabs
        self.searchData.tableView = self.mainUI.SearchTableView
        self.recentlyUsedData.tableView = self.mainUI.RecentlyUsedTableView
        self.favoritesData.tableView = self.mainUI.FavoritesTableView

        # For keyboard input and monitoring
        self.controller = keyboard.Controller()
        self.keyboardListener = KeyboardListener()
        self.keyboardListener.keyboardSignal.connect(self.keybindsCallback)
        self.keyboardListener.start()

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
        
        #self.mainUI.KaomojiSetButton.clicked.connect(self.updateEmojiSet)
        self.mainUI.DefaultTabComboBox.currentIndexChanged.connect(self.updateDefaultTab)
        self.mainUI.LaunchAtStartupCheckbox.clicked.connect(self.updateLaunchAtStartup)
        self.mainUI.ClearSearchEntryCheckbox.clicked.connect(self.updateClearSearchEntry)
        self.mainUI.ThemeComboBox.currentIndexChanged.connect(self.updateTheme)
        self.mainUI.FontComboBox.currentFontChanged.connect(self.updateFont)
        #self.mainUI.FontColorButton.clicked.connect(self.updateFontColor)
        ##self.mainUI.ShowSoundButton.clicked.connect(self.updateShowSound)
        ##self.mainUI.HideSoundButton.clicked.connect(self.updateHideSound)
        self.mainUI.ShowWindowKeySequence.keySequenceChanged.connect(self.updateShowWindow)
        self.mainUI.HideWindowKeySequence.keySequenceChanged.connect(self.updateHideWindow)
        self.mainUI.PreviousPageKeySequence.keySequenceChanged.connect(self.updatePreviousPage)
        self.mainUI.NextPageKeySequence.keySequenceChanged.connect(self.updateNextPage)
                
        self.updateTab(Tabs.Search)
        self.updateTab(Tabs.RecentlyUsed)
        self.updateTab(Tabs.Favorites)
        self.updateSettings()
        
    def load(self):
        kaomojis = {}

        with open(self.config.config.get('GENERAL', 'kaomoji_set'), 'r', encoding='utf-8') as file:
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
        if self.config.config.getboolean('GENERAL', 'clear_search_entry_upon_inserting') == True:
            self.currentTab.searchQuery = ''
            self.mainUI.SearchLineEdit.setText('')
    
        self.showMinimized()
        self.controller.type(kaomoji)
    
        recentKaomojis = self.recentlyUsedData.list
        if kaomoji not in recentKaomojis:
            recentKaomojis[kaomoji] = self.searchData.list.get(kaomoji, [])
    
        recentKaomojis = dict(list(recentKaomojis.items())[-self.recentlyUsedData.limit:])
        self.recentlyUsedData.list = recentKaomojis
        self.updateTab(Tabs.RecentlyUsed)

    # def onRelease(self, key: keyboard.Key):
    #     if hasattr(key, 'char'):
    #         if (key.char == 'k'):
    #             self.keyboardSignal.emit(Keybinds.Show)
    #     if key == keyboard.Key.esc:
    #         self.keyboardSignal.emit(Keybinds.Hide)
    #     if key == keyboard.Key.left:
    #         self.keyboardSignal.emit(Keybinds.Prev)
    #     if key == keyboard.Key.right:
    #         self.keyboardSignal.emit(Keybinds.Next)

    def keybindsCallback(self, keysPressed: list[int]):
        for keycode in keysPressed:
            print(keycode)
            qtkey = Qt.Key(keycode)
            qtkeysequence = QKeySequence(qtkey)
            print(qtkey)
            print(qtkeysequence.toString())
        # if key == Keybinds.Show:
        #     self.show()
        # if key == Keybinds.Hide:
        #     self.hide()
        # if key == Keybinds.Prev:
        #     self.previousPage()
        # if key == Keybinds.Next:
        #     self.nextPage()
        # if key == Keybinds.Debug:
        #     print(self.config.config.get('KEYBINDS', 'show_window'))
        #     print(self.config.config.get('KEYBINDS', 'hide_window'))
        #     print(keyboard.HotKey.parse(self.config.config.get('KEYBINDS', 'show_window')))
        #     print(keyboard.HotKey.parse(self.config.config.get('KEYBINDS', 'hide_window')))

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
            self.mainUI.SearchLineEdit.setEnabled(False)
        else:
            self.mainUI.SearchLineEdit.setEnabled(True)
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

        data.model.setHorizontalHeaderLabels(["Kaomoji"])
        font = QFont(self.config.config.get('APPEARANCE', 'font'), 12)

        for kaomoji, tags in displayedResults:
            tagsJoined = ', '.join(tags)

            kaomojiItem = QStandardItem(kaomoji)
            kaomojiItem.setFont(font)
            kaomojiItem.setEditable(False)

            data.model.appendRow([kaomojiItem])
            kaomojiItem.setToolTip(tagsJoined)
        
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
        elif tab == Tabs.RecentlyUsed:
            data = self.recentlyUsedData
        elif tab == Tabs.Favorites:
            data = self.favoritesData
        else:
            return

        self.updateSearch(data)
        self.updateStatus(data)
    
    def updateSettings(self):
        # General
        self.mainUI.KaomojiSetLineEdit.setText(self.config.config.get('GENERAL', 'kaomoji_set'))
        self.mainUI.DefaultTabComboBox.setCurrentIndex(self.config.config.getint('GENERAL', 'default_tab'))
        self.mainUI.LaunchAtStartupCheckbox.setChecked(self.config.config.getboolean('GENERAL', 'launch_at_startup'))
        self.mainUI.ClearSearchEntryCheckbox.setChecked(self.config.config.getboolean('GENERAL', 'clear_search_entry_upon_inserting'))
        
        # Appearance
        self.mainUI.ThemeComboBox.setCurrentIndex(self.config.config.getint('APPEARANCE', 'theme'))
        self.mainUI.FontComboBox.setCurrentFont(self.config.config.get('APPEARANCE', 'font'))
        
        # Miscellaneous
        self.mainUI.ShowSoundLineEdit.setText(self.config.config.get('MISCELLANEOUS', 'show_sound'))
        self.mainUI.HideSoundLineEdit.setText(self.config.config.get('MISCELLANEOUS', 'hide_sound'))

        # Keybinds
        self.mainUI.ShowWindowKeySequence.setKeySequence(self.config.config.get('KEYBINDS', 'show_window'))
        self.mainUI.HideWindowKeySequence.setKeySequence(self.config.config.get('KEYBINDS', 'hide_window'))
        self.mainUI.PreviousPageKeySequence.setKeySequence(self.config.config.get('KEYBINDS', 'previous_page'))
        self.mainUI.NextPageKeySequence.setKeySequence(self.config.config.get('KEYBINDS', 'next_page'))

    def updateDefaultTab(self, index):
        self.config.setValue('GENERAL', 'default_tab', index)

    def updateLaunchAtStartup(self, state):
        self.config.setValue('GENERAL', 'launch_at_startup', state)
    
    def updateClearSearchEntry(self, state):
        self.config.setValue('GENERAL', 'clear_search_entry_upon_inserting', state)

    def updateTheme(self, index):
        self.config.setValue('APPEARANCE', 'theme', index)
    
    def updateFont(self, font: QFont):
        self.config.setValue('APPEARANCE', 'font', font.family())

    def updateShowWindow(self, keybind: QKeySequence):
        self.config.setValue('KEYBINDS', 'show_window', keybind.toString())

    def updateHideWindow(self, keybind: QKeySequence):
        self.config.setValue('KEYBINDS', 'hide_window', keybind.toString())

    def updatePreviousPage(self, keybind: QKeySequence):
        self.config.setValue('KEYBINDS', 'previous_page', keybind.toString())

    def updateNextPage(self, keybind: QKeySequence):
        self.config.setValue('KEYBINDS', 'next_page', keybind.toString())

    def center(self):
        frameGeometry = self.frameGeometry()
        screen = self.window().windowHandle().screen()
        centerLocation = screen.geometry().center()
        frameGeometry.moveCenter(centerLocation)
        self.move(frameGeometry.topLeft())

def main():
    config = Config()
    app = QApplication(sys.argv)

    styles = QStyleFactory.keys()
    selectedStyle = int(config.config.get('APPEARANCE', 'theme'))
    if selectedStyle < len(styles):
        app.setStyle(styles[selectedStyle])

    mainWindow = MainWindow(config)
    mainWindow.show()
    app.exec()
    mainWindow.center()

if __name__ == '__main__':
    main()
