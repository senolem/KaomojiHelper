import json
from pynput.keyboard import Key, Controller
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QFrame,
)

class KaomojiHelper(QWidget):
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
        self.results_layout: QVBoxLayout
        self.results_frame: QFrame
        self.first_page_btn: QPushButton
        self.prev_page_btn: QPushButton
        self.last_page_btn: QPushButton
        self.next_page_btn: QPushButton
        self.results_label: QLabel
        self.message_label: QLabel

        self.setWindowTitle("KaomojiHelper")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet('background-color: #ccc;')
        self.create_widgets()
        
        # For keyboard input
        self.controller: Controller = Controller()

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
        start_index = (self.current_page - 1) * self.results_per_page
        end_index = start_index + self.results_per_page

        if not self.search_entry.text().strip():
            if self.recent_kaomojis:
                self.results = self.recent_kaomojis
                displayed_results = self.results[-self.results_per_page:]
            else:
                self.results = list(self.kaomojis.keys())
                displayed_results = self.results[start_index:end_index]
        else:
            if not self.results:
                self.message_label.text = 'No kaomoji found with your search terms'
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
        self.search_entry.setStyleSheet("background-color: white;")
        self.search_entry.textChanged.connect(self.search)
        self.layout.addWidget(self.search_entry)

        # Search results
        self.results_frame = QFrame()
        self.results_layout = QVBoxLayout(self.results_frame)
        self.layout.addWidget(self.results_frame)
        
        self.results_buttons = [QPushButton() for _ in range(self.results_per_page)]
        for btn in self.results_buttons:
            btn.setStyleSheet('background-color: white;')
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

        self.next_page_btn = QPushButton('>')
        self.next_page_btn.clicked.connect(self.next_page)
        self.pages_frame.addWidget(self.next_page_btn)

        self.last_page_btn = QPushButton('>>')
        self.last_page_btn.clicked.connect(self.last_page)
        self.pages_frame.addWidget(self.last_page_btn)

        # Search results label
        self.results_label = QLabel('0-0 results | 0 (total)')
        self.pages_frame.addWidget(self.results_label)

        # Message
        self.message_label = QLabel()
        self.results_layout.addWidget(self.message_label)

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

if __name__ == '__main__':
    app = QApplication([])
    kaomojiHelper = KaomojiHelper()
    kaomojiHelper.show()
    app.exec()
        