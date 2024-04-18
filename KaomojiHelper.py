import json
from pynput import keyboard
from PyQt6.QtWidgets import (
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
from PyQt6.QtCore import Qt, pyqtSignal
from enum import Enum

class KaomojiHelper(QWidget):
    
    class Keybinds(Enum):
        SHOW = 1
        HIDE = 2
        PREV = 3
        NEXT = 4

    keyboard_signal = pyqtSignal(Keybinds) # signal for keybinds callbacks to be executed in main thread instead of keyboard monitoring thread

    def __init__(self):
        super().__init__()
        # Data
        self.recent_kaomojis: list[str] = []
        self.results: list[str] = []
        self.current_page: int = 1
        self.results_per_page: int = 10
        self.max_recent_kaomojis: int = 100
        self.kaomojis = self.load()
        
        # GUI stuff
        self.layout: QVBoxLayout
        self.search_entry: QLineEdit
        self.title_label: QLabel
        self.message_label: QLabel
        self.results_layout: QVBoxLayout
        self.results_frame: QFrame
        self.first_page_btn: QPushButton
        self.prev_page_btn: QPushButton
        self.last_page_btn: QPushButton
        self.next_page_btn: QPushButton
        self.results_label: QLabel

        self.setWindowTitle("KaomojiHelper")
        self.setGeometry(100, 100, 600, 400)
        self.create_widgets()
        
        # For keyboard input and monitoring
        self.controller: keyboard.Controller = keyboard.Controller()
        self.listener: keyboard.Listener = keyboard.Listener(on_release=self.on_release)
        self.listener.start()
        self.keyboard_signal.connect(self.control_gui)

    def load(self):
        with open('kaomojis.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def search(self, query: str):
        self.results = []
        for kaomoji, info in self.kaomojis.items():
            if query.lower() in ' '.join(info['original_tags']).lower():
                self.results.append(kaomoji)
        self.current_page = 1
        self.update()
    
    def update(self):
        self.message_label.setVisible(False)
        start_index = (self.current_page - 1) * self.results_per_page
        end_index = start_index + self.results_per_page

        if not self.search_entry.text().strip():
            if self.recent_kaomojis:
                self.title_label.setText('Recently used')
                self.results = self.recent_kaomojis
                displayed_results = self.results[-self.results_per_page:]
            else:
                self.title_label.setText('All kaomojis')
                self.results = list(self.kaomojis.keys())
                displayed_results = self.results[start_index:end_index]
        else:
            self.title_label.setText('Search results')
            if not self.results:
                self.message_label.setText('No kaomoji found with your search terms')
                self.message_label.setVisible(True)
                displayed_results = []
            else:
                displayed_results = self.results[start_index:end_index]

        self.update_results(displayed_results)
        self.update_pages()
    
    def update_results(self, displayed_results: list[str]):
        for btn in self.results_buttons:
            btn.setVisible(False)
            
        for i, kaomoji in enumerate(displayed_results):
            if i < self.results_per_page:
                btn = self.results_buttons[i]
                btn.setText(kaomoji)
                btn.setVisible(True)
                
    def on_button_clicked(self):
        button = self.sender()
        if button:
            kaomoji = button.text()
            self.insert(kaomoji)

    def insert(self, kaomoji: str):
        if not kaomoji.strip():
            return

        self.hide()
        self.controller.type(kaomoji)

        recent_slice = self.recent_kaomojis[-self.results_per_page:]
        if kaomoji not in recent_slice:
            self.recent_kaomojis.append(kaomoji)
        self.recent_kaomojis = self.recent_kaomojis[-self.max_recent_kaomojis:]
        self.update()

    def create_widgets(self):
        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Search entry
        self.search_entry = QLineEdit()
        self.search_entry.textChanged.connect(self.search)
        self.layout.addWidget(self.search_entry)
        
        # Title
        self.title_label = QLabel('All kaomojis')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.set
        self.layout.addWidget(self.title_label)

        # Search results
        self.results_frame = QFrame()
        self.results_layout = QVBoxLayout(self.results_frame)
        self.layout.addWidget(self.results_frame)
        
        self.results_buttons = [QPushButton() for _ in range(self.results_per_page)]
        for btn in self.results_buttons:
            btn.clicked.connect(self.on_button_clicked)
            self.results_layout.addWidget(btn)

        # Pages controls
        self.pages_frame = QHBoxLayout()
        self.layout.addLayout(self.pages_frame)

        self.first_page_btn = QPushButton('<<')
        self.first_page_btn.clicked.connect(self.first_page)
        self.pages_frame.addWidget(self.first_page_btn)

        self.prev_page_btn = QPushButton('<')
        self.prev_page_btn.clicked.connect(self.prev_page)
        self.pages_frame.addWidget(self.prev_page_btn)
        
        self.results_label = QLabel('0-0 results | 0 (total)')
        self.pages_frame.addWidget(self.results_label)

        self.next_page_btn = QPushButton('>')
        self.next_page_btn.clicked.connect(self.next_page)
        self.pages_frame.addWidget(self.next_page_btn)

        self.last_page_btn = QPushButton('>>')
        self.last_page_btn.clicked.connect(self.last_page)
        self.pages_frame.addWidget(self.last_page_btn)
        
        # Message
        self.message_label = QLabel()
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setVisible(False)
        self.results_layout.addWidget(self.message_label)
        
        # Update list at launch
        self.update()

    def update_pages(self):
        total_results = len(self.results)

        if not self.results:
            return

        start_index = (self.current_page - 1) * self.results_per_page + 1
        end_index = min(start_index + self.results_per_page - 1, total_results)

        self.results_label.setText(f'{start_index}-{end_index} results | {total_results} (total)')

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update()

    def next_page(self):
        total_pages = (len(self.results) + self.results_per_page - 1) // self.results_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.update()

    def first_page(self):
        if self.current_page != 1:
            self.current_page = 1
            self.update()

    def last_page(self):
        total_results = len(self.results)
        total_pages = (total_results + self.results_per_page - 1) // self.results_per_page
        if self.current_page != total_pages:
            self.current_page = total_pages
            self.update()
            
    def control_gui(self, key: Keybinds):
        if key == self.Keybinds.SHOW:
            self.show()
        if key == self.Keybinds.HIDE:
            self.hide()
        if key == self.Keybinds.PREV:
            self.prev_page()
        if key == self.Keybinds.NEXT:
            self.next_page()
    
    def on_release(self, key: keyboard.Key):
        if hasattr(key, 'char'):
            if (key.char == 'k'):
                self.keyboard_signal.emit(self.Keybinds.SHOW)
        if key == keyboard.Key.esc:
            self.keyboard_signal.emit(self.Keybinds.HIDE)
        if key == keyboard.Key.left:
            self.keyboard_signal.emit(self.Keybinds.PREV)
        if key == keyboard.Key.right:
            self.keyboard_signal.emit(self.Keybinds.NEXT)

    def center(self):
        frame_geo = self.frameGeometry()
        screen = self.window().windowHandle().screen()
        center_loc = screen.geometry().center()
        frame_geo.moveCenter(center_loc)
        self.move(frame_geo.topLeft())
            

if __name__ == '__main__':
    app = QApplication([])
    kaomojiHelper = KaomojiHelper()
    kaomojiHelper.show()
    kaomojiHelper.center()
    app.exec()
        