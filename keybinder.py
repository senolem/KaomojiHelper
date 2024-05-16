from pyqtkeybind import keybinder
from typing import Callable, Optional
from PySide6.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher

class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0

class EventDispatcher:
    """Install a native event filter to receive events from the OS"""

    def __init__(self, keybinder) -> None:
        self.win_event_filter = WinEventFilter(keybinder)
        self.event_dispatcher = QAbstractEventDispatcher.instance()
        self.event_dispatcher.installNativeEventFilter(self.win_event_filter)

class QtKeyBinder:
    def __init__(self, win_id: Optional[int]) -> None:
        keybinder.init()
        self.hotkeys = set()
        self.win_id = win_id
        self.event_dispatcher = EventDispatcher(keybinder=keybinder)

    def register_hotkey(self, hotkey: str, callback: Callable) -> None:
        if keybinder.register_hotkey(self.win_id, hotkey, callback):
            self.hotkeys.add(hotkey)

    def unregister_hotkey(self, hotkey: str) -> None:
        if hotkey in self.hotkeys:
            keybinder.unregister_hotkey(self.win_id, hotkey)
            self.hotkeys.remove(hotkey)
