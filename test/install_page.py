import os
from pathlib import Path
from tkinter import colorchooser
import customtkinter
from custom_exit_message import CombinedModal
from PIL import Image

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(
    r"/home/hakan/Documents/GitHub/pythonInstaller/assets"
)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class install_page(customtkinter.CTkFrame):
    def __init__(self, parent, controller, os_properties):
        customtkinter.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.os_properties = os_properties

        self.invalid_entries = []
        os_name = self.os_properties.get_os()
        text_color = self.os_properties.get_os_color()
        os_icon_path = self.os_properties.os_icon()
        self.button_font = customtkinter.CTkFont(family="Inter", size=20)
        install_page_frame = customtkinter.CTkFrame(
            self,
            fg_color="#2B2631",
            # border_width=4,
            # bg_color="#2B2631",
            # border_color="#F89F24",
        )
        install_page_frame.place(x=311.0, y=0.0)
        install_page_frame.columnconfigure(0, weight=1)
        self.header_title_background = customtkinter.CTkImage(
            light_image=Image.open(
                "/home/hakan/Documents/GitHub/pythonInstaller/assets/backgrounds/header_title_background.png"
            ),
            dark_image=Image.open(
                "/home/hakan/Documents/GitHub/pythonInstaller/assets/backgrounds/header_title_background.png"
            ),
            size=(300, 64),
        )
        self.header_title_background_label = customtkinter.CTkLabel(
            master=install_page_frame,
            text="Status",
            image=self.header_title_background,
            text_color="White",
            font=customtkinter.CTkFont(family="Inter", size=24, weight="bold"),
            bg_color="#2B2631",
        )
        self.header_title_background_label.grid(
            row=0, column=0, columnspan=2, padx=248, pady=(75, 0), sticky="NSEW"
        )

        self.line_top_image = customtkinter.CTkImage(
            light_image=Image.open(
                "/home/hakan/Documents/GitHub/pythonInstaller/assets/backgrounds/line_top.png"
            ),
            dark_image=Image.open(
                "/home/hakan/Documents/GitHub/pythonInstaller/assets/backgrounds/line_top.png"
            ),
            size=(650, 6),
        )
        self.line_top_image_label = customtkinter.CTkLabel(
            master=install_page_frame,
            text="",
            image=self.line_top_image,
        )
        self.line_top_image_label.grid(
            row=1, column=0, columnspan=2, padx=10, pady=(20, 30), sticky="NSEW"
        )

        inputs_frame = customtkinter.CTkFrame(
            master=install_page_frame,
            width=440,
            height=54,
            corner_radius=12,
            fg_color="#2B2631",
        )
        inputs_frame.grid(
            row=2, column=0, columnspan=2, padx=10, pady=(20, 30), sticky="NSEW"
        )

        # Profile Name
        self.profile_folder_name_label = customtkinter.CTkLabel(
            master=inputs_frame,
            text_color="white",
            font=customtkinter.CTkFont(family="Inter", size=18, weight="bold"),
            text="Profile Folder",
        )
        self.profile_folder_name_label.grid(row=0, column=0, padx=(10, 4), sticky="w")

        self.profile_folder_name_entry = customtkinter.CTkEntry(
            master=inputs_frame,
            width=342,
            height=38,
            fg_color="white",
            text_color="black",
            corner_radius=8,
            border_width=3,
            bg_color="#2B2631",
            border_color="purple",
            placeholder_text="profile_folder_name_entry",
        )
        self.profile_folder_name_entry.grid(
            row=1, column=0, padx=(10, 4), pady=10, sticky="ew"
        )
        self.profile_folder_name_entry.bind(
            "<FocusOut>",
            lambda event: self.validate_location(self.profile_folder_name_entry, None),
        )

        # Checkbox
        self.check_var = customtkinter.StringVar(value="off")
        self.edit_checkbox = customtkinter.CTkCheckBox(
            master=inputs_frame,
            text="Edit Inputs",
            command=self.checkbox_event,
            fg_color="#F08D27",
            hover_color="#F08D27",
            bg_color="#2B2631",
            text_color="white",
            variable=self.check_var,
            onvalue="on",
            offvalue="off",
        )
        self.edit_checkbox.grid(row=5, column=1, padx=(10, 4), pady=10, sticky="ew")

        # Firefox Folder
        self.firefox_folder_label = customtkinter.CTkLabel(
            master=inputs_frame,
            text_color="white",
            font=customtkinter.CTkFont(family="Inter", size=18, weight="bold"),
            text="Firefox Folder",
        )
        self.firefox_folder_label.grid(row=0, column=1, padx=(10, 4), sticky="w")

        self.firefox_folder_entry = customtkinter.CTkEntry(
            master=inputs_frame,
            width=342,
            height=38,
            fg_color="white",
            text_color="black",
            corner_radius=8,
            border_width=3,
            bg_color="#2B2631",
            border_color="orange",
            placeholder_text="firefox_folder_entry",
        )
        self.firefox_folder_entry.grid(
            row=1, column=1, padx=(10, 4), pady=10, sticky="ew"
        )
        self.firefox_folder_entry.bind(
            "<FocusOut>",
            lambda event: self.validate_location(self.firefox_folder_entry, None),
        )

        # Application Folder
        self.application_folder_label = customtkinter.CTkLabel(
            master=inputs_frame,
            text_color="white",
            font=customtkinter.CTkFont(family="Inter", size=18, weight="bold"),
            text="Application Folder",
        )
        self.application_folder_label.grid(row=2, column=0, padx=(10, 4), sticky="w")

        self.application_folder_entry = customtkinter.CTkEntry(
            master=inputs_frame,
            width=342,
            height=38,
            fg_color="white",
            text_color="black",
            corner_radius=8,
            border_width=3,
            bg_color="#2B2631",
            border_color="green",
            placeholder_text="application_folder_entry",
        )
        self.application_folder_entry.grid(
            row=3, column=0, padx=(10, 4), pady=10, sticky="ew"
        )
        self.application_folder_entry.bind(
            "<FocusOut>",
            lambda event: self.validate_location(self.application_folder_entry, None),
        )

        # Accent Color
        self.accent_color_label = customtkinter.CTkLabel(
            master=inputs_frame,
            text_color="white",
            font=customtkinter.CTkFont(family="Inter", size=18, weight="bold"),
            text="Accent Color",
        )
        self.accent_color_label.grid(row=2, column=1, padx=(10, 4), sticky="w")
        self.accent_color_values = ["Blue", "Red", "Custom"]  # Initial values
        self.selected_color = None  # Store custom color

        self.accent_color_combobox = customtkinter.CTkComboBox(
            master=inputs_frame,
            width=342,
            height=38,
            fg_color="white",
            text_color="black",
            values=self.accent_color_values,  # Use initial values
            command=self.on_accent_color_select,
            corner_radius=8,
            border_width=3,
            bg_color="#2B2631",
            border_color="purple",
        )
        # Set default selection (if desired)
        if "default_color" in self.__dict__:  # Check if default_color is defined
            self.accent_color_combobox.set(self.default_color)
        else:
            self.accent_color_combobox.set(
                self.accent_color_values[0]
            )  # Set first value as default
        self.accent_color_combobox.grid(
            row=3, column=1, padx=(10, 4), pady=10, sticky="ew"
        )

        # New tab wallpaper
        self.newtab_wallpaper_label = customtkinter.CTkLabel(
            master=inputs_frame,
            text_color="white",
            font=customtkinter.CTkFont(family="Inter", size=18, weight="bold"),
            text="New Tab Wallpaper Location",
        )
        self.newtab_wallpaper_label.grid(row=4, column=0, padx=(10, 4), sticky="w")

        self.newtab_wallpaper_entry = customtkinter.CTkEntry(
            master=inputs_frame,
            width=342,
            height=38,
            fg_color="white",
            text_color="black",
            corner_radius=8,
            border_width=3,
            bg_color="#2B2631",
            border_color="green",
            placeholder_text="newtab_wallpaper_entry",
        )
        self.newtab_wallpaper_entry.grid(
            row=5, column=0, padx=(10, 4), pady=10, sticky="ew"
        )
        self.newtab_wallpaper_entry.bind(
            "<FocusOut>",
            lambda event: self.validate_location(self.newtab_wallpaper_entry, ".png"),
        )

        self.invalid_entry_frame = customtkinter.CTkFrame(
            master=inputs_frame,
            width=440,  # Adjust initial width as needed
            height=54,
            corner_radius=12,
            bg_color="#2B2631",
            fg_color="white",
        )
        self.invalid_entry_frame.grid(
            row=6, column=0, columnspan=2, padx=(10, 4), pady=10
        )
        # Load the attention icon image
        self.attention_icon = customtkinter.CTkImage(
            light_image=Image.open(
                "/home/hakan/Documents/GitHub/pythonInstaller/assets/icons/attention.png"
            ),
            dark_image=Image.open(
                "/home/hakan/Documents/GitHub/pythonInstaller/assets/icons/attention.png"
            ),
            size=(24, 24),
        )
        # Create the label to display the invalid entries count
        self.invalid_entries_text = customtkinter.CTkLabel(
            master=self.invalid_entry_frame,
            text="",
            text_color="#f04141",
            font=("Arial", 16, "bold"),  # Adjust font size and family as needed
            image=self.attention_icon,
            compound="left",
        )
        self.invalid_entries_text.pack(padx=10, pady=10)
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
        image_path = relative_to_assets("icons/install_icon.png")  # Get the absolute path
        image = Image.open(image_path)
        self.install_button_image = customtkinter.CTkImage(
            dark_image=image, light_image=image, size=(20, 20)
        )
        self.install_button = customtkinter.CTkButton(
            master=navigation_frame,
            text="Install",
            fg_color="#D9D9D9",
            hover_color="#EEEEEE",
            bg_color="white",
            corner_radius=12,
            command=lambda: controller.show_frame(
                "status_page",
                come_from_which_page="install",
                profile_folder=self.get_variables(self.profile_folder_name_entry),
                application_folder=self.get_variables(self.application_folder_entry),
                new_tab_wallpaper=self.get_variables(self.newtab_wallpaper_entry),
                firefox_folder=self.get_variables(self.firefox_folder_entry),
                accent_color=self.get_variables_combobox(self.accent_color_combobox),
            ),
            width=122.0,
            height=38.0,
            image=self.install_button_image,
            compound="right",
            text_color="#000000",
            font=self.button_font,
        )
        self.install_button.pack(padx=(5, 20), pady=10, side="right")
        image_path = relative_to_assets("icons/back_icon.png")  # Get the absolute path
        image = Image.open(image_path)
        self.back_button_image = customtkinter.CTkImage(
            dark_image=image, light_image=image, size=(24, 20)
        )
        back_button = customtkinter.CTkButton(
            master=navigation_frame,
            text="Back",
            fg_color="#D9D9D9",
            hover_color="#EEEEEE",
            bg_color="white",
            corner_radius=12,
            command=lambda: controller.show_frame("home_page"),
            width=122.0,
            height=38.0,
            image=self.back_button_image,
            text_color="#000000",
            font=self.button_font,
        )
        back_button.pack(padx=5, pady=10, side="right")
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
            text_color=text_color,
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

        self.update_invalid_entries_display()
        self.checkbox_event()

    def on_accent_color_select(self, color):
        if color == "Custom":
            self.choose_custom_color()

    def choose_custom_color(self):
        color = colorchooser.askcolor(title="Choose Custom Color")
        if color[1]:  # Check if a color was chosen
            self.selected_color = color[1]
            self.accent_color_values.append(
                self.selected_color
            )  # Add custom color to values
            self.accent_color_combobox.set(self.selected_color)  # Set custo
            self.accent_color_combobox.configure(button_color=self.selected_color)

    def validate_location(self, entry_widget, file_extension=None):
        location = entry_widget.get()

        if (os.path.exists(location) or location == "") and file_extension == None:
            entry_widget.configure(border_color="#10dc60")
            # Remove entry from invalid_entries if it exists
            if entry_widget in self.invalid_entries:
                self.invalid_entries.remove(entry_widget)
        elif (
            os.path.isfile(location)
            and location.lower().endswith(".png")
            or location == ""
        ) and file_extension == ".png":
            entry_widget.configure(border_color="#10dc60")
            # Remove entry from invalid_entries if it exists
            if entry_widget in self.invalid_entries:
                self.invalid_entries.remove(entry_widget)
        else:
            entry_widget.configure(border_color="#f04141")
            # Add entry to invalid_entries if it's not already in the list
            if entry_widget not in self.invalid_entries:
                self.invalid_entries.append(entry_widget)

        self.update_invalid_entries_display()

    def update_invalid_entries_display(self):
        if len(self.invalid_entries) == 0:
            self.install_button.configure(state="normal")
            # Hide the invalid entry frame if there are no invalid entries
            self.invalid_entry_frame.grid_remove()
        else:
            self.install_button.configure(state="disabled")
            # Show the invalid entry frame and update the text with the count of invalid entries
            self.invalid_entries_text.configure(
                text=f"  {len(self.invalid_entries)} entries is invalid"
            )
            self.invalid_entry_frame.grid()

    def get_variables(self, entry):
        input_value = entry.get()
        placeholder_text = entry.cget("placeholder_text")
        if input_value:
            return input_value
        else:
            return placeholder_text

    def get_variables_combobox(self, combobox_widget):
        selected_value = combobox_widget.get()
        if selected_value:
            return selected_value
        else:
            return "blue"

    def exit_confirmation(self):
        print("Install page exit_confirmation func")
        CombinedModal(self, "Exit")

    def update_parameters(self, **kwargs):
        # # Process and use the parameters as needed
        # self.param1 = kwargs.get("param1")
        # self.param2 = kwargs.get("param2")
        # self.param3 = kwargs.get("param3")
        # self.install_button.configure(
        #     command=lambda: self.controller.show_frame(
        #         "status_page",
        #         param1=self.param1,
        #         param2=self.param2,
        #         param3=self.param3,
        #     )
        # )
        # self.os_label.configure(text=self.param1, text_color=self.param2)
        # self.os_icon_image.configure(file=self.param3)
        pass

    def checkbox_event(self):
        if self.check_var.get() == "on":
            # Enable entries
            self.accent_color_combobox.configure(state="normal")
            self.newtab_wallpaper_entry.configure(state="normal")
            self.firefox_folder_entry.configure(state="normal")
            self.application_folder_entry.configure(state="normal")
            self.profile_folder_name_entry.configure(state="normal")
        else:
            # Disable entries
            self.accent_color_combobox.configure(state="disabled")
            self.newtab_wallpaper_entry.configure(state="disabled")
            self.firefox_folder_entry.configure(state="disabled")
            self.application_folder_entry.configure(state="disabled")
            self.profile_folder_name_entry.configure(state="disabled")
