class CenterWindow:
    def __init__(self, window):
        self.window = window

    def center_window(self):
        """Center the application window on the screen."""
        self.window.update_idletasks()
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"+{x}+{y}")