from PySide6 import QtCore
from pynput import keyboard

class KeyboardListener(QtCore.QObject):
    keyboardSignal = QtCore.Signal(list)
    
    def __init__(self):
        super().__init__()
        self.keysPressed = []

    def start(self):
        self.listener = keyboard.Listener(on_press=self.onPress, on_release=self.onRelease)
        self.listener.start()

    def stop(self):
        self.listener.stop()

    def onPress(self, key: keyboard.Key):
        if type(key) == keyboard._win32.KeyCode:
            keycode = key.vk
        else:
            keycode = key.value.vk

        if keycode not in self.keysPressed:
            self.keysPressed.append(keycode)
            self.keyboardSignal.emit(self.keysPressed)

    def onRelease(self, key: keyboard.Key):
        if type(key) == keyboard._win32.KeyCode:
            keycode = key.vk
        else:
            keycode = key.value.vk

        del self.keysPressed[self.keysPressed.index(keycode)]