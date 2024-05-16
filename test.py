from pynput import keyboard

class Test():
    def __init__(self):
        self.controller = keyboard.Controller()
        self.listener = keyboard.Listener(on_release=self.on_release)
        self.listener.start()

        # Add a flag to indicate when to stop the listener
        self.running = True

    def on_release(self, key):
        print('aaa')

        # If you want to stop the listener under some condition, you can do it here
        if key == keyboard.Key.esc:
            self.stop()

    def stop(self):
        self.running = False
        self.listener.stop()

if __name__ == '__main__':
    test = Test()

    # Keep the main thread running until the user wants to exit
    while test.running:
        pass
