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
)
from PySide6.QtCore import Qt, Signal, QObject
from ui import Ui_Form
from keybinds import Keybinds
from tabs import Tabs

class KaomojiHelper(QObject):
	def __init__(self):
		super().__init__()
		# Data
		self.recentKaomojis: list[str] = []
		self.resultsPerPage: int = 10
		self.maxRecentKaomojis: int = 100
		self.kaomojis = self.load()

	def load(self):
		with open('kaomojis.json', 'r', encoding='utf-8') as file:
			return json.load(file)

class MainWindow(QWidget):
	keyboardSignal = Signal(Keybinds) # signal for keybinds callbacks to be executed in main thread instead of keyboard monitoring thread

	def __init__(self, kaomojiHelper: KaomojiHelper, parent=None):
		super(MainWindow, self).__init__(parent)
		self.mainUI = Ui_Form()
		self.mainUI.setupUi(self)

		# Data
		self.kaomojiHelper = kaomojiHelper
		self.currentTab: Tabs = Tabs.Search
		self.searchCurrentPage: int = 1
		self.recentlyUsedCurrentPage: int = 1
		self.favoritesCurrentPage: int = 1
		self.searchResults: list[str] = []

		# For keyboard input and monitoring
		self.controller: keyboard.Controller = keyboard.Controller()
		self.listener: keyboard.Listener = keyboard.Listener(onRelease=self.onRelease)
		self.listener.start()

		self.keyboardSignal.connect(self.keybindsCallback)

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

		if self.currentTab == Tabs.Search:
			self.updateSearch()
			self.updateStatus()

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
		if self.currentTab == Tabs.Search:
			if self.searchCurrentPage > 1:
				self.searchCurrentPage -= 1
				self.updateSearch()
				self.updateStatus()
		if self.currentTab == Tabs.RecentlyUsed:
			if self.recentlyUsedCurrentPage > 1:
				self.recentlyUsedCurrentPage -= 1
				self.updateSearch()
				self.updateStatus()
		if self.currentTab == Tabs.Favorites:
			if self.favoritesCurrentPage > 1:
				self.favoritesCurrentPage -= 1
				self.updateSearch()
				self.updateStatus()

	def nextPage(self):
		total_pages = (len(self.searchResults) + self.kaomojiHelper.resultsPerPage - 1) // self.kaomojiHelper.resultsPerPage
		if self.searchCurrentPage < total_pages:
			self.searchCurrentPage += 1
			self.updateSearch()
			self.updateStatus()

	def firstPage(self):
		if self.searchCurrentPage != 1:
			self.searchCurrentPage = 1
			self.updateSearch()
			self.updateStatus()

	def lastPage(self):
		total_results = len(self.searchResults)
		total_pages = (total_results + self.kaomojiHelper.resultsPerPage - 1) // self.kaomojiHelper.resultsPerPage
		if self.searchCurrentPage != total_pages:
			self.searchCurrentPage = total_pages
			self.updateSearch()
			self.updateStatus()

	def searchChanged(self, text):
		if self.currentTab != Tabs.Search:
			self.currentTab = Tabs.Search
			self.mainUI.TabsWidget.setCurrentIndex(Tabs.Search.value)
		self.search(text)

	def tabChanged(self, index):
		self.currentTab = index

	def search(self, query: str):
		self.searchResults = []
		for kaomoji, info in self.kaomojiHelper.kaomojis.items():
			if query.lower() in ' '.join(info['original_tags']).lower():
				self.searchResults.append(kaomoji)
		self.searchCurrentPage = 1
		self.updateSearch()
		self.updateStatus()

	def updateSearch(self):
		start_index = (self.searchCurrentPage - 1) * self.kaomojiHelper.resultsPerPage
		end_index = start_index + self.kaomojiHelper.resultsPerPage

		if not self.mainUI.SearchLineEdit.text().strip():
			self.searchResults = list(self.kaomojiHelper.kaomojis.keys())
			displayed_results = self.searchResults[start_index:end_index]
		else:
			if not self.searchResults:
				displayed_results = []
			else:
				displayed_results = self.searchResults[start_index:end_index]

	def updateStatus(self):
		total_results = len(self.searchResults)

		if not self.searchResults:
			return

		start_index = (self.searchCurrentPage - 1) * self.kaomojiHelper.resultsPerPage + 1
		end_index = min(start_index + self.kaomojiHelper.resultsPerPage - 1, total_results)

		if self.currentTab == Tabs.Search:
			self.mainUI.SearchStatusLabel.setText(f'{start_index}-{end_index} results | {total_results} (total)')
		if self.currentTab == Tabs.RecentlyUsed:
			self.mainUI.RecentlyUsedStatusLabel.setText(f'{start_index}-{end_index} results | {total_results} (total)')
		if self.currentTab == Tabs.Favorites:
			self.mainUI.FavoritesStatusLabel.setText(f'{start_index}-{end_index} results | {total_results} (total)')

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
