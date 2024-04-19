from pathlib import Path
import customtkinter
from PIL import Image


from custom_exit_message import CombinedModal

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(
    r"/home/hakan/Documents/GitHub/pythonInstaller/build/assets"
)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class status_page(customtkinter.CTkFrame):
    def __init__(self, parent, controller, os_properties):
        customtkinter.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.os_properties = os_properties

        self.come_from_which_page = None

        os_name = self.os_properties.get_os()

        os_text_color = self.os_properties.get_os_color()

        os_icon_path = self.os_properties.os_icon()

        self.bind("<Visibility>", self.start_simulate_progress)

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
            row=0, column=0, columnspan=2, padx=273, pady=(75, 0), sticky="NSEW"
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
        self.line_top_image_label.grid(
            row=1, column=0, columnspan=2, padx=10, pady=(20, 30), sticky="NSEW"
        )

        self.check_icon = customtkinter.CTkImage(
            light_image=Image.open(
                "/home/hakan/Documents/GitHub/pythonInstaller/build/assets/icons/check.png"
            ),
            dark_image=Image.open(
                "/home/hakan/Documents/GitHub/pythonInstaller/build/assets/icons/check.png"
            ),
            size=(20, 20),
        )
        self.action_label = customtkinter.CTkLabel(
            master=status_page_frame,
            fg_color="#2B2631",
            text_color="white",
            text="",
            image=None,
            compound="right",
            font=customtkinter.CTkFont(family="Inter", size=18, weight="bold"),
        )
        self.action_label.grid(row=2, column=0, padx=60, pady=10, sticky="W")

        self.progress_bar = customtkinter.CTkProgressBar(
            master=status_page_frame,
            orientation="horizontal",
            height=24,
            bg_color="#2B2631",
            fg_color="white",
            progress_color="#9747FF",
        )
        self.progress_bar.grid(row=3, column=0, padx=50, pady=10, sticky="NSEW")
        self.progress_bar.set(0)

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

    def start_simulate_progress(self, event):
        # Unbind the event so that this function is not called again when the page becomes visible again
        self.unbind("<Visibility>")
        # Start the progress simulation
        self.simulate_progress(self.progress_bar)

    def simulate_progress(self, progress_bar):
        print("Status page simulate_progress func")
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
            self.action_label.configure(text="Installed  ", image=self.check_icon)
        elif self.come_from_which_page == "remove":
            self.action_label.configure(text="Removed  ", image=self.check_icon)

    def attention(self):
        print("Status page attention func")
        CombinedModal(self, "Attention")

    def exit_confirmation(self):
        print("Status page exit_confirmation func")
        CombinedModal(self, "Exit")

    def update_parameters(self, **kwargs):
        print("Status page parameters func")
        # # Process and use the parameters as needed
        self.come_from_which_page = kwargs.get("come_from_which_page")
        self.profile_folder = kwargs.get("profile_folder")
        self.application_folder = kwargs.get("application_folder")
        self.new_tab_wallpaper = kwargs.get("new_tab_wallpaper")
        self.firefox_folder = kwargs.get("firefox_folder")
        self.accent_color = kwargs.get("accent_color")
        # start_button = customtkinter.CTkButton(
        #     self,
        #     text="Simulate Progress",
        #     command=lambda: self.simulate_progress(self.progress_bar),
        # )
        # start_button.pack()
        if self.come_from_which_page == "install":
            self.action_label.configure(text="Instaling...")
            print(
                f"self.profile_folder={self.profile_folder}\nself.application_folder={self.application_folder}\nself.new_tab_wallpaper={self.new_tab_wallpaper}\nself.firefox_folder={self.firefox_folder}\nself.accent_color={self.accent_color}"
            )
        elif self.come_from_which_page == "remove":
            print(
                f"self.profile_folder={self.profile_folder}\nself.application_folder={self.application_folder}\nself.firefox_folder={self.firefox_folder}"
            )
            self.action_label.configure(text="Removing...")

        self.back_button.configure(
            command=lambda: self.controller.show_frame(
                f"{self.come_from_which_page}_page"
            ),
        )
