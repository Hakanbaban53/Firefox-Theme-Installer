import os
import sys
from json import load
from customtkinter import CTk, CTkImage, CTkLabel, CTkFont, CTkFrame
from PIL import Image
from components.set_window_icon import SetWindowIcon
from modals.info_modals import InfoModals
from pages.home_page import HomePage
from pages.install_page import InstallPage
from pages.remove_page import RemovePage
from pages.status_page import StatusPage

class MultiPageApp(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Determine base directory using _MEIPASS or current script directory
        self.base_dir = getattr(
            sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__))
        )  # Also I send the other pages and functions this path.

        installer_data_path = os.path.join(self.base_dir, "data", "installer_data.json")
        with open(installer_data_path, "r", encoding="utf-8") as file:
            self.text_data = load(file)


        self.configure_layout()
        self.center_window()
        self.create_widgets()

    def configure_layout(self):
        self.title(self.text_data["common_values"]["installer_info"]["installer_title"])
        self.geometry("1115x666")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.exit_confirmation)
        self.configure(bg="#2B2631")

        icon_setter = SetWindowIcon(self.base_dir)
        icon_setter.set_window_icon(self)

    def create_widgets(self):
        self.installer_img = CTkImage(
            light_image=Image.open(
                os.path.join(
                    self.base_dir, "assets", "backgrounds", "installer_img.png"
                )
            ),
            dark_image=Image.open(
                os.path.join(
                    self.base_dir, "assets", "backgrounds", "installer_img.png"
                )
            ),
            size=(315, 666),
        )

        self.installer_img_label = CTkLabel(
            self,
            text=self.text_data["common_values"]["installer_info"]["installer_version"],
            text_color="white",
            image=self.installer_img,
            font=CTkFont(family="Inter", size=14),
        )
        self.installer_img_label.place(x=0, y=0)  # Place image label at (0, 0)

        self.container = CTkFrame(self, fg_color="#2B2631")  # Set matching background color
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}

    def create_frame(self, page_class):
        frame = page_class(self.container, self, self.base_dir)

        frame.configure(
            fg_color="#2B2631",
            corner_radius=0,
        )

        frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        return frame

    def slide_to_frame(self, current_frame, next_frame, x=0, speed=20, direction='left'):
        # Determine slide directions based on relative positions
        window_width = self.winfo_width()
        target_x = 0 if direction == 'left' else window_width + 315

        # Apply easing for smoother sliding effect
        def ease_in_out(t):
            return 3 * (t ** 2) - 2 * (t ** 3)

        next_frame.place(x=target_x + window_width if direction == 'left' else -window_width, y=0, relwidth=1, relheight=1)
        next_frame.lift()
        self.update()

        def slide_step(position):
            ease_position = int(ease_in_out(position / window_width) * window_width)
            current_pos = ease_position + 315 if direction == 'left' else window_width - ease_position

            # Position frames based on easing calculation
            next_frame.place(x=target_x - (window_width - current_pos), y=0)
            current_frame.place(x=current_pos, y=0) if direction == 'left' else current_frame.place(x=current_pos -800, y=0)

            if position < window_width:
                self.after(5, slide_step, position + speed)
            else:
                current_frame.place_forget()
                next_frame.place(x=315, y=0, relwidth=1, relheight=1)

        slide_step(x)

    def show_frame(self, page_name, **kwargs):
        self.installer_img_label.lift()

        page_class = {
            "home_page": HomePage,
            "install_page": InstallPage,
            "remove_page": RemovePage,
            "status_page": StatusPage,
        }.get(page_name)

        if page_class:
            if page_class not in self.frames:
                self.frames[page_class] = self.create_frame(page_class)

            current_frame = None
            for frame in self.frames.values():
                if frame.winfo_ismapped():
                    current_frame = frame
                    break

            next_frame = self.frames[page_class]
            if current_frame is not None:
                direction = 'left' if list(self.frames.values()).index(current_frame) > list(self.frames.values()).index(next_frame) else 'right'
                self.slide_to_frame(current_frame, next_frame, 0, speed=20, direction=direction)
            else:
                next_frame.place(x=315, y=0, relwidth=1, relheight=1)

            next_frame.update_parameters(**kwargs)
            next_frame.tkraise()

    def exit_confirmation(self):
        InfoModals(self, self.base_dir, "Exit")

    def center_window(self):
        """Center the modal window on the screen."""
        self.update_idletasks()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry("+{}+{}".format(x, y))

if __name__ == "__main__":
    app = MultiPageApp()
    app.show_frame("home_page")
    app.mainloop()
