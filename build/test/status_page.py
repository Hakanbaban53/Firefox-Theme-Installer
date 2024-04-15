from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import customtkinter
from PIL import Image


from custom_exit_message import CombinedModal

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(
    r"/home/hakan/Documents/GitHub/pythonInstaller/build/assets"
)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class status_page(tk.Frame):
    def __init__(self, parent, controller, os_properties):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.os_properties = os_properties

        self.come_from_which_page = None

        os_name = self.os_properties.get_os()

        os_text_color = self.os_properties.get_os_color()

        os_icon_path = self.os_properties.os_icon()

        self.button_font = customtkinter.CTkFont(family="Inter", size=20)

        status_page_frame = customtkinter.CTkFrame(
            self,
            fg_color="#2B2631",
            # border_width=4,
            # bg_color="#2B2631",
            # border_color="#F89F24",
        )
        status_page_frame.place(x=311.0, y=0.0)
        status_page_frame.columnconfigure(0, weight=1)

        self.header_title_background = customtkinter.CTkImage(
            light_image=Image.open(
                "/home/hakan/Documents/GitHub/pythonInstaller/build/assets/backgrounds/header_title_background.png"
            ),
            dark_image=Image.open(
                "/home/hakan/Documents/GitHub/pythonInstaller/build/assets/backgrounds/header_title_background.png"
            ),
            size=(250, 64),
        )
        self.header_title_background_label = customtkinter.CTkLabel(
            master=status_page_frame,
            text="Status",
            image=self.header_title_background,
            text_color="White",
            font=customtkinter.CTkFont(family="Inter", size=24, weight="bold"),
            bg_color="#2B2631",
        )
        self.header_title_background_label.grid(
            row=0, column=0, columnspan=2, padx=273, pady=(75,0), sticky="NSEW"
        )

        self.line_top_image = customtkinter.CTkImage(
            light_image=Image.open(
                "/home/hakan/Documents/GitHub/pythonInstaller/build/assets/backgrounds/line_top.png"
            ),
            dark_image=Image.open(
                "/home/hakan/Documents/GitHub/pythonInstaller/build/assets/backgrounds/line_top.png"
            ),
            size=(650, 6),
        )
        self.line_top_image_label = customtkinter.CTkLabel(
            master=status_page_frame,
            text="",
            image=self.line_top_image,
        )
        self.line_top_image_label.grid(row=1, column=0, columnspan=2, padx=10, pady=(20,30), sticky="NSEW")

        self.action_label = customtkinter.CTkLabel(
            master=status_page_frame,
            fg_color="#2B2631",
            text_color="white",
            text="",
            font=customtkinter.CTkFont(family="Inter", size=18, weight="bold"),
        )
        self.action_label.grid(row=2, column=0, padx=20, pady=10, sticky="W")

        self.progress_bar = customtkinter.CTkProgressBar(
            master=status_page_frame,
            orientation="horizontal",
            height=24,
            bg_color="#2B2631",
            fg_color="white",
            progress_color="#9747FF",
        )
        self.progress_bar.grid(row=3, column=0, padx=30, pady=10, sticky="NSEW")
        self.progress_bar.set(0)
        start_button = customtkinter.CTkButton(
            self,
            text="Simulate Progress",
            command=lambda: self.simulate_progress(self.progress_bar),
        )
        start_button.pack()

        self.output_entry = customtkinter.CTkTextbox(
            master=status_page_frame,
            height=190,
            fg_color="white",
            text_color="black",
            corner_radius=12,
            bg_color="#2B2631",
        )

        self.output_entry.grid(row=4, column=0, padx=60, pady=20, sticky="NSEW")

        bottom_frame = customtkinter.CTkFrame(
            self,
            fg_color="#2B2631",
        )
        bottom_frame.place(x=500.0, y=600.0)

        navigation_frame = customtkinter.CTkFrame(
            master=bottom_frame,
            width=440,
            height=54,
            corner_radius=12,
            border_width=4,
            bg_color="#2B2631",
            fg_color="white",
            border_color="#F89F24",
        )

        navigation_frame.grid(row=0, column=1, padx=20, sticky="E")

        image_path = relative_to_assets(
            "icons/finish_icon.png"
        )  # Get the absolute path
        image = Image.open(image_path)
        self.finish_button_image = customtkinter.CTkImage(
            dark_image=image, light_image=image, size=(20, 20)
        )

        finish_button = customtkinter.CTkButton(
            master=navigation_frame,
            text="Finish",
            fg_color="#D9D9D9",
            hover_color="#EEEEEE",
            bg_color="white",
            corner_radius=12,
            command=self.attention,
            width=122.0,
            height=38.0,
            image=self.finish_button_image,
            compound="right",
            text_color="#000000",
            font=self.button_font,
        )

        finish_button.pack(padx=(5, 20), pady=10, side="right")

        image_path = relative_to_assets("icons/back_icon.png")  # Get the absolute path
        image = Image.open(image_path)
        self.back_button_image = customtkinter.CTkImage(
            dark_image=image, light_image=image, size=(24, 20)
        )

        self.back_button = customtkinter.CTkButton(
            master=navigation_frame,
            text="Back",
            fg_color="#D9D9D9",
            hover_color="#EEEEEE",
            bg_color="white",
            corner_radius=12,
            # state=tk.DISABLED,
            width=122.0,
            height=38.0,
            image=self.back_button_image,
            text_color="#000000",
            font=self.button_font,
        )

        self.back_button.pack(padx=5, pady=10, side="right")
        self.update_parameters()

        image_path = relative_to_assets("icons/exit_icon.png")  # Get the absolute path
        image = Image.open(image_path)
        self.exit_button_image = customtkinter.CTkImage(
            dark_image=image, light_image=image, size=(20, 20)
        )

        exit_button = customtkinter.CTkButton(
            master=navigation_frame,
            text="Exit",
            fg_color="#D9D9D9",
            hover_color="#EEEEEE",
            bg_color="white",
            corner_radius=12,
            command=self.exit_confirmation,
            width=122.0,
            height=38.0,
            image=self.exit_button_image,
            text_color="#000000",
            font=self.button_font,
        )
        exit_button.pack(padx=(20, 5), pady=10, side="left")


        os_frame = customtkinter.CTkFrame(
            master=bottom_frame,
            width=440,  # Adjust initial width as needed
            height=54,
            corner_radius=12,
            bg_color="#2B2631",
            fg_color="white",
        )
        os_frame.grid(row=0, column=0, padx=20, sticky="W")

        self.os_label = customtkinter.CTkLabel(
            master=os_frame,
            text=os_name,
            text_color=os_text_color,
            font=("Arial", 20, "bold"),  # Adjust font size and family as needed
        )
        self.os_label.pack(
            padx=(10, 4), pady=10, side="left"
        )  # Pad the label within the frame

        image = Image.open(os_icon_path)
        self.os_icon_image = customtkinter.CTkImage(
            dark_image=image, light_image=image, size=(20, 24)
        )

        os_image = customtkinter.CTkLabel(
            master=os_frame,
            text="",
            image=self.os_icon_image,  # Set the image
        )
        os_image.pack(
            padx=(4, 10), pady=10, side="right"
        )  # Pack on the right side with padding

    def simulate_progress(self, progress_bar):
        """Simulates a task with a progress bar.

        Args:
            progress_bar (ctk.CTkProgressBar): The progress bar to update.
        """

        for i in range(101):
            progress_bar.set(i / 100)  # Update progress as a percentage
            self.update_idletasks()
            self.after(5)  # Adjust delay between updates (milliseconds)
            self.output_entry.insert("end", "Your text goes here\n")

        if self.come_from_which_page == "install":
            self.action_label.configure(text="Installed")
        elif self.come_from_which_page == "remove":
            self.action_label.configure(text="Removed")
        

    def attention(self):
        CombinedModal(
            self,
            "Attention!",
            "RealFire Succesfully installed.\n Please restart firefox twice!",
            "OK",
            "OK",
        )

    def exit_confirmation(self):
        CombinedModal(self, "Exit Confirmation", "Are you sure you want to exit?")

    def update_parameters(self, **kwargs):
        # # Process and use the parameters as needed
        self.come_from_which_page = kwargs.get("come_from_which_page")

        if self.come_from_which_page == "install":
            self.action_label.configure(text="Instaling...")
        elif self.come_from_which_page == "remove":
            self.action_label.configure(text="Removing...")


        self.back_button.configure(
            command=lambda: self.controller.show_frame(
                f"{self.come_from_which_page}_page"
            ),
        )
        pass

