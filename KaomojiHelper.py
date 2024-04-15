import json
import threading
import keyboard
import tkinter

class Search:
	def __init__(self):
		self.recent_kaomojis = []
		self.results = []
		self.current_page = 1
		self.results_per_page = 10
		self.max_recent_kaomojis = 100

		self.kaomojis = self.load()
		self.window = tkinter.Tk()
		self.window.overrideredirect(True) # no window title bar
		self.window.title('KaomojiHelper')
		self.window.attributes('-topmost', True) # set at topmost
		self.window.geometry('600x400')
		self.window.configure(bg='black')
		self.create_widgets()

		self.update()
		self.window.rowconfigure(0, weight=1)
		self.window.columnconfigure(0, weight=1)

	def load(self):
		with open('kaomojis.json', 'r', encoding='utf-8') as file:
			return json.load(file)
	
	def search(self, query):
		self.results = []
		for kaomoji, info in self.kaomojis.items():
			if query.lower() in ' '.join(info['original_tags']).lower():
				self.results.append(kaomoji)
		self.current_page = 1
		self.update()
	
	def update(self):
		for widget in self.results_frame.winfo_children():
			widget.destroy()

		start_index = (self.current_page - 1) * self.results_per_page
		end_index = start_index + self.results_per_page

		if not self.search_entry.get().strip():
			if self.recent_kaomojis:
				self.results = self.recent_kaomojis
				displayed_results = self.results[-self.results_per_page:]
			else:
				self.results = list(self.kaomojis.keys())
				displayed_results = self.results[start_index:end_index]
		else:
			if not self.results:
				self.show_message('No kaomoji found with your search terms')
				displayed_results = []
			else:
				displayed_results = self.results[start_index:end_index]

		self.update_results(displayed_results)
		self.update_pages()
	
	def update_results(self, displayed_results):
		for i, kaomoji in enumerate(displayed_results):
			btn = tkinter.Button(self.results_frame, text=kaomoji, command=lambda k=kaomoji: self.insert(k))
			btn.grid(row=i, column=0, sticky='ew')

	def insert(self, kaomoji):
		self.window.withdraw()
		keyboard.write(kaomoji)

		recent_slice = self.recent_kaomojis[-self.results_per_page:]
		if kaomoji not in recent_slice:
			self.recent_kaomojis.append(kaomoji)
		self.recent_kaomojis = self.recent_kaomojis[-self.max_recent_kaomojis:]
		self.update()
	
	def set_keybinds(self):
		keyboard.add_hotkey('esc', lambda: self.window.withdraw())
		keyboard.add_hotkey('k', lambda: self.focus())
	
	def create_widgets(self):
		self.window.rowconfigure(0, weight=0)
		self.window.rowconfigure(1, weight=1)
		self.window.rowconfigure(2, weight=0)
	
		self.window.columnconfigure(0, weight=1)
	
		self.search_entry = tkinter.Entry(self.window, bg='black')
		self.search_entry.grid(row=0, column=0, sticky='ew')
		self.search_entry.bind('<KeyRelease>', lambda event: self.search(self.search_entry.get()))

		self.results_frame = tkinter.Frame(self.window)
		self.results_frame.grid(row=1, column=0, sticky='nsew')
		self.results_frame.columnconfigure(0, weight=1)

		self.pages_frame = tkinter.Frame(self.window)
		self.pages_frame.grid(row=2, column=0, sticky='nsew')
		self.pages_frame.columnconfigure(2, weight=1)

	def focus(self):
		self.window.deiconify()
		self.search_entry.focus()
	
	def update_pages(self):
		total_results = len(self.results)

		for widget in self.pages_frame.winfo_children():
			widget.destroy()

		if not self.results:
			return

		start_index = (self.current_page - 1) * self.results_per_page + 1
		end_index = min(start_index + self.results_per_page - 1, total_results)

		self.pages_frame.grid(row=2, column=0, sticky='nsew')

		first_btn = tkinter.Button(self.pages_frame, text='<<', command=self.first_page)
		first_btn.grid(row=0, column=0, sticky='ew')

		prev_btn = tkinter.Button(self.pages_frame, text='<', command=self.prev_page)
		prev_btn.grid(row=0, column=1, sticky='ew')

		page_label = tkinter.Label(self.pages_frame, text=f'{start_index}-{end_index} results | {total_results} (total)')
		page_label.grid(row=0, column=2, sticky='ew')

		next_btn = tkinter.Button(self.pages_frame, text='>', command=self.next_page)
		next_btn.grid(row=0, column=3, sticky='ew')

		last_btn = tkinter.Button(self.pages_frame, text='>>', command=self.last_page)
		last_btn.grid(row=0, column=4, sticky='ew')

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
	
	def show_message(self, text):
		self.message = tkinter.Label(self.results_frame, text=text)
		self.message.grid(row=0, column=0, sticky='ew')

	def run(self):
		self.window.mainloop()

if __name__ == '__main__':
	search = Search()
	search.run()
		