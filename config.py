import configparser
import os

class Config:
    def __init__(self, filename='config.ini'):
        
        # Config file
        self.filename = filename
        if os.path.exists(filename):
            self.loadConfig()
        else:
            self.config = configparser.ConfigParser()
            self.createDefaultConfig()

        # Parsed config values
        self.kaomoji_set = self.config['GENERAL']['kaomoji_set']
        self.default_tab = self.config.getint('GENERAL', 'default_tab')
        self.launch_at_startup = self.config.getboolean('GENERAL', 'launch_at_startup')
        self.clear_search_entry_upon_inserting = self.config.getboolean('GENERAL', 'clear_search_entry_upon_inserting')
        
        self.theme = self.config['APPEARANCE']['theme']
        self.font = self.config['APPEARANCE']['theme']
        self.font_color = self.config['APPEARANCE']['theme']
        
        self.show_sound = self.config['MISCELLANEOUS']['show_sound']
        self.hide_sound = self.config['MISCELLANEOUS']['hide_sound']
        
        self.show_window = self.config['KEYBINDS']['show_window']
        self.hide_window = self.config['KEYBINDS']['hide_window']
        self.previous_page = self.config['KEYBINDS']['previous_page']
        self.next_page = self.config['KEYBINDS']['next_page']
        

    def loadConfig(self):
        write_needed = False
        self.config = configparser.ConfigParser()
        self.config.read(self.filename)
        
        for section, options in self.defaultValues().items():
            if section not in self.config:
                self.config[section] = options
                write_needed = True
            else:
                for option, default_value in options.items():
                    if option not in self.config[section]:
                        self.config[section][option] = default_value
                        write_needed = True
        if write_needed:
            self.writeConfig()

    def writeConfig(self):
        with open(self.filename, 'w') as f:
            self.config.write(f)

    def getValue(self, section, key):
        return self.config.get(section, key)

    def setValue(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)

    def createDefaultConfig(self):
        with open(self.filename, 'w') as f:
            self.config.write(f)

    def defaultValues(self) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config['GENERAL'] = {
            'kaomoji_set': 'kaomojis.json',
            'default_tab': 0,
            'launch_at_startup': True,
            'clear_search_entry_upon_inserting': False
        }
        config['APPEARANCE'] = {
            'theme': '',
            'font': '',
            'font_color': '#FFFFFF'
        }
        config['MISCELLANEOUS'] = {
            'show_sound': '',
            'hide_sound': ''
        }
        config['KEYBINDS'] = {
            'show_window': '',
            'hide_window': '',
            'previous_page': '',
            'next_page': ''
        }
        return config