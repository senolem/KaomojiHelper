import configparser
import os

class Config:
    def __init__(self, filename='config.ini'):
        
        # Config file
        self.filename = filename
        if os.path.exists(filename):
            self.load()
        else:
            self.config = configparser.ConfigParser()
            self.createDefaultConfig()

    def load(self):
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

    def write(self):
        with open(self.filename, 'w') as f:
            self.config.write(f)

    def get(self, section, key):
        return self.config.get(section, key)
    
    def getBoolean(self, section, key):
        return self.config.getboolean(section, key)

    def getInt(self, section, key):
        return self.config.getint(section, key)

    def set(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        self.write()

    def createDefaultConfig(self):
        with open(self.filename, 'w') as f:
            self.config.write(f)

    def defaultValues(self) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config['GENERAL'] = {
            'kaomoji_set': 'kaomojis.json',
            'default_tab': 0,
            'launch_at_startup': False,
            'clear_search_entry_upon_inserting': False
        }
        config['APPEARANCE'] = {
            'theme': 0,
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