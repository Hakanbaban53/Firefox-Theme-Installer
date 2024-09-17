import sys
from os import path
from tkinter import Frame, Tk
from customtkinter import CTkLabel
from components.set_window_icon import SetWindowIcon
from installer_core.data_tools.image_loader import ImageLoader
from installer_core.data_tools.load_json_data import LoadJsonData
from installer_core.window_tools.center_window import CenterWindow
from modals.info_modals import InfoModals
from pages.home_page import HomePage
from pages.install_page import InstallPage
from pages.remove_page import RemovePage
from pages.status_page import StatusPage


class MultiPageApp(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_dir = getattr(sys, "_MEIPASS", path.abspath(path.dirname(__file__)))

        base_data_path = path.join(self.base_dir, "data", "installer_data.json")
        self.base_data = LoadJsonData().load_json_data(base_data_path)

        self.configure_layout()
        self.create_widgets()

    def configure_layout(self):
        """Set window title, geometry, and icon."""
        installer_title = self.base_data["installer_info"]["installer_title"]
        self.title(installer_title)
        self.geometry(f"{self.base_data["window_settings"]["window_width"]}x{self.base_data["window_settings"]["window_height"]}")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.exit_confirmation)
        SetWindowIcon(self.base_dir).set_window_icon(self)
        CenterWindow(self).center_window()

    def create_widgets(self):
        """Create image label and container frame for page content."""
        self.create_image_label()
        self.create_page_container()


    def create_image_label(self):
        """Create and place the image label with a background image."""
        self.image_frame = Frame(
            master=self,
            width=315,
            height=666,
        )
        self.image_frame.place(x=0, y=0)

        image_loader = ImageLoader(path.join(self.base_dir, "assets", "backgrounds"))
        installer_img = image_loader.load_installer_img("installer_img.png")
        
        installer_version = self.base_data["installer_info"]["installer_version"]
        self.background_label = CTkLabel(
            self.image_frame,
            image=installer_img,
            text=installer_version,
            text_color="white",
            font=("Inter", 14)
        )
        self.background_label.pack(fill="both", expand=True)

    def create_page_container(self):
        """Create a container to hold all the frames (pages) of the application."""
        self.container = Frame(self, bg=self.base_data["window_settings"]["bg_color"])
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}

    def create_frame(self, page_class):
        """Create and return a new frame for the specified page class."""
        frame = page_class(self.container, self, self.base_dir)
        frame.configure(bg=self.base_data["window_settings"]["bg_color"])
        frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        return frame

    def show_frame(self, page_name, **kwargs):
        """Display the frame associated with the given page name, sliding it into view."""
        self.image_frame.lift()

        # Map page name to its corresponding class
        page_class = {
            "home_page": HomePage,
            "install_page": InstallPage,
            "remove_page": RemovePage,
            "status_page": StatusPage,
        }.get(page_name)

        if not page_class:
            print(f"Page '{page_name}' not found.")
            return

        # If the frame does not exist yet, create it
        if page_class not in self.frames:
            self.frames[page_class] = self.create_frame(page_class)

        current_frame = self.get_current_frame()
        next_frame = self.frames[page_class]

        if current_frame:
            direction = "left" if self.is_left_direction(current_frame, next_frame) else "right"
            self.slide_to_frame(current_frame, next_frame, 0, speed=20, direction=direction)
        else:
            next_frame.place(x=self.base_data["window_settings"]["default_padding_x"], y=0, relwidth=1, relheight=1)

        next_frame.update_parameters(**kwargs)
        next_frame.tkraise()

    def get_current_frame(self):
        """Return the currently visible frame."""
        for frame in self.frames.values():
            if frame.winfo_ismapped():
                return frame
        return None

    def slide_to_frame(
        self, current_frame, next_frame, x=0, speed=20, direction="left"
    ):
        # Determine slide directions based on relative positions
        window_width = self.winfo_width()
        target_x = 0 if direction == "left" else window_width + 315

        # Apply easing for smoother sliding effect
        def ease_in_out(t):
            return 3 * (t**2) - 2 * (t**3)

        next_frame.place(
            x=target_x + window_width if direction == "left" else -window_width,
            y=0,
            relwidth=1,
            relheight=1,
        )
        next_frame.lift()
        self.update()

        def slide_step(position):
            ease_position = int(ease_in_out(position / window_width) * window_width)
            current_pos = (
                ease_position + 315
                if direction == "left"
                else window_width - ease_position
            )

            # Position frames based on easing calculation
            next_frame.place(x=target_x - (window_width - current_pos), y=0)
            (
                current_frame.place(x=current_pos, y=0)
                if direction == "left"
                else current_frame.place(x=current_pos - 800, y=0)
            )

            if position < window_width:
                self.after(5, slide_step, position + speed)
            else:
                current_frame.place_forget()
                next_frame.place(x=315, y=0, relwidth=1, relheight=1)

        slide_step(x)

    def is_left_direction(self, current_frame, next_frame):
        """Determine if the sliding direction is left based on frame order."""
        return list(self.frames.values()).index(current_frame) > list(self.frames.values()).index(next_frame)

    def exit_confirmation(self):
        """Display exit confirmation modal."""
        InfoModals(self, self.base_dir, "Exit")

    def center_window(self):
        """Center the application window on the screen."""
        self.update_idletasks()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"+{x}+{y}")


if __name__ == "__main__":
    app = MultiPageApp()
    app.center_window()
    app.show_frame("home_page")
    app.mainloop()
