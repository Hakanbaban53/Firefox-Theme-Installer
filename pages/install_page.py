from json import load
from tkinter import colorchooser
from customtkinter import CTkFrame, CTkImage, CTkLabel, CTkFont, CTkFrame, CTkButton, CTkEntry, CTkCheckBox, StringVar, CTkComboBox
from PIL import Image
from modals.combined_modal import CombinedModal
from functions.get_os_properties import OSProperties
from functions.get_folder_locations import get_profile_folder
from functions.special_input_functions import SpecialInputFunc



class install_page(CTkFrame):
    os_values = OSProperties().get_values()
    input_values = OSProperties().get_locations()
    profile_folder_location = get_profile_folder()

    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
        self.controller = controller

        with open("../RealFire-Installer/data/installer_data.json", "r") as file:
            self.text_data = load(file)

        self.button_data = self.text_data.get("common_values")["navigation_buttons"]
        self.input_data = self.text_data.get("common_values")["inputs"]

        """
            /////////////////////////////
            /Image Location Declarations/
            /////////////////////////////
                                        """
        self.header_title_background = CTkImage(
            light_image=Image.open(
                "../RealFire-Installer/assets/backgrounds/header_title_background.png"
            ),
            dark_image=Image.open(
                "../RealFire-Installer/assets/backgrounds/header_title_background.png"
            ),
            size=(300, 64),
        )
        self.line_top_image = CTkImage(
            light_image=Image.open(
                "../RealFire-Installer/assets/backgrounds/line_top.png"
            ),
            dark_image=Image.open(
                "../RealFire-Installer/assets/backgrounds/line_top.png"
            ),
            size=(650, 6),
        )
        self.os_icon_image = CTkImage(
            dark_image=Image.open(f"../RealFire-Installer/assets/icons/{self.os_values["os_name"].lower()}.png"), 
            light_image=Image.open(f"../RealFire-Installer/assets/icons/{self.os_values["os_name"].lower()}.png"),
            size=(20, 24)
        )
        self.attention_icon = CTkImage(
            light_image=Image.open("../RealFire-Installer/assets/icons/attention.png"),
            dark_image=Image.open("../RealFire-Installer/assets/icons/attention.png"),
            size=(24, 24),
        )
        self.install_button_image = CTkImage(
            dark_image=Image.open(
                "../RealFire-Installer/assets/icons/install_icon.png"
                ),
            light_image=Image.open(
                "../RealFire-Installer/assets/icons/install_icon.png"
            ),
            size=(20, 24),
        )
        self.back_button_image = CTkImage(
            dark_image=Image.open("../RealFire-Installer/assets/icons/back_icon.png"),
            light_image=Image.open("../RealFire-Installer/assets/icons/back_icon.png"),
            size=(20, 20),
        )
        self.exit_button_image = CTkImage(
            dark_image=Image.open("../RealFire-Installer/assets/icons/exit_icon.png"),
            light_image=Image.open("../RealFire-Installer/assets/icons/exit_icon.png"),
            size=(20, 20),
        )



        install_page_frame = CTkFrame(
            self,
            fg_color="#2B2631",
            # border_width=4,
            # bg_color="#2B2631",
            # border_color="#F89F24",
        )
        install_page_frame.grid(row=0, column=1, sticky="NE")
        install_page_frame.columnconfigure(0, weight=1)
        self.header_title_background_label = CTkLabel(
            master=install_page_frame,
            text="Install RealFire",
            image=self.header_title_background,
            text_color="White",
            font=CTkFont(family="Inter", size=24, weight="bold"),
            bg_color="#2B2631",
        )
        self.header_title_background_label.grid(
            row=0, column=0, columnspan=2, padx=248, pady=(75, 0), sticky="NSEW"
        )

        self.line_top_image_label = CTkLabel(
            master=install_page_frame,
            text="",
            image=self.line_top_image,
        )
        self.line_top_image_label.grid(
            row=1, column=0, columnspan=2, padx=10, pady=(20, 30), sticky="NSEW"
        )

        inputs_frame = CTkFrame(
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
        self.profile_folder_name_label = CTkLabel(
            master=inputs_frame,
            text_color="white",
            font=CTkFont(family="Inter", size=18, weight="bold"),
            text="Profile Folder",
        )
        self.profile_folder_name_label.grid(row=0, column=0, padx=(10, 4), sticky="w")

        self.profile_folder_name_entry = CTkEntry(
            master=inputs_frame,
            width=int(self.input_data["width"]),
            height=int(self.input_data["height"]),
            fg_color=self.input_data["fg_color"],
            text_color=self.input_data["text_color"],
            corner_radius=int(self.input_data["corner_radius"]),
            border_width=int(self.input_data["border_width"]),
            bg_color=self.input_data["bg_color"],
            border_color=self.input_data["border_color"],
            placeholder_text=self.profile_folder_location,
        )
        self.profile_folder_name_entry.grid(
            row=1, column=0, padx=(10, 4), pady=10, sticky="ew"
        )

        # Application Folder
        self.application_folder_label = CTkLabel(
            master=inputs_frame,
            text_color="white",
            font=CTkFont(family="Inter", size=18, weight="bold"),
            text="Application Folder",
        )
        self.application_folder_label.grid(row=0, column=1, padx=(10, 4), sticky="w")

        self.application_folder_entry = CTkEntry(
            master=inputs_frame,
            width=int(self.input_data["width"]),
            height=int(self.input_data["height"]),
            fg_color=self.input_data["fg_color"],
            text_color=self.input_data["text_color"],
            corner_radius=int(self.input_data["corner_radius"]),
            border_width=int(self.input_data["border_width"]),
            bg_color=self.input_data["bg_color"],
            border_color=self.input_data["border_color"],
            placeholder_text=self.input_values["application_folder"],
        )
        self.application_folder_entry.grid(
            row=1, column=1, padx=(10, 4), pady=10, sticky="ew"
        )

        # New tab wallpaper
        self.newtab_wallpaper_label = CTkLabel(
            master=inputs_frame,
            text_color="white",
            font=CTkFont(family="Inter", size=18, weight="bold"),
            text="New Tab Wallpaper Location",
        )
        self.newtab_wallpaper_label.grid(row=2, column=0, padx=(10, 4), sticky="w")

        self.newtab_wallpaper_entry = CTkEntry(
            master=inputs_frame,
            width=int(self.input_data["width"]),
            height=int(self.input_data["height"]),
            fg_color=self.input_data["fg_color"],
            text_color=self.input_data["text_color"],
            corner_radius=int(self.input_data["corner_radius"]),
            border_width=int(self.input_data["border_width"]),
            bg_color=self.input_data["bg_color"],
            border_color=self.input_data["border_color"],
            placeholder_text="newtab_wallpaper_entry",
        )
        self.newtab_wallpaper_entry.grid(
            row=3, column=0, padx=(10, 4), pady=10, sticky="ew"
        )


        # Accent Color
        self.accent_color_label = CTkLabel(
            master=inputs_frame,
            text_color="white",
            font=CTkFont(family="Inter", size=18, weight="bold"),
            text="Accent Color",
        )
        self.accent_color_label.grid(row=2, column=1, padx=(10, 4), sticky="w")
        self.accent_color_values = ["Blue", "Red", "AccentColor", "Custom"]  # Initial values
        self.selected_color = None  # Store custom color

        self.accent_color_combobox = CTkComboBox(
            master=inputs_frame,
            width=int(self.input_data["width"]),
            height=int(self.input_data["height"]),
            fg_color=self.input_data["fg_color"],
            text_color=self.input_data["text_color"],
            corner_radius=int(self.input_data["corner_radius"]),
            border_width=int(self.input_data["border_width"]),
            bg_color=self.input_data["bg_color"],
            border_color=self.input_data["border_color"],
            values=self.accent_color_values,  # Use initial values
            command=self.on_accent_color_select,
        )

        # Checkbox
        self.check_var = StringVar(value="off")
        self.edit_checkbox = CTkCheckBox(
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

        """
            //////////////////////////////
            ////Key Bind Declarations////
            //////////////////////////////
                                            """
        self.key_bind(self.profile_folder_name_entry)
        self.key_bind(self.application_folder_entry)
        self.key_bind(self.application_folder_entry)
        self.key_bind(self.newtab_wallpaper_entry, ".png")


        """
            //////////////////////////////////
            ////Invalid Entry Declarations////
            //////////////////////////////////
                                                """
        self.invalid_entry_frame = CTkFrame(
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

        # Create the label to display the invalid entries count
        self.invalid_entries_text = CTkLabel(
            master=self.invalid_entry_frame,
            text="",
            text_color="#f04141",
            font=("Arial", 16, "bold"),  # Adjust font size and family as needed
            image=self.attention_icon,
            compound="left",
        )
        self.invalid_entries_text.pack(padx=10, pady=10)

        """
            /////////////////////////////
            /Bottom Widgets Declarations/
            /////////////////////////////
                                            """
        bottom_frame = CTkFrame(
            self,
            fg_color="#2B2631",
        )
        bottom_frame.place(x=200.0, y=600.0)

        navigation_frame = CTkFrame(
            master=bottom_frame,
            width=440,
            height=54,
            corner_radius=12,
            border_width=4,
            bg_color="#2B2631",
            fg_color="white",
            border_color="#F89F24",
        )

        navigation_frame.grid(row=0, column=1, sticky="E")

        self.install_button = CTkButton(
            master=navigation_frame,
            width=float(self.button_data["width"]),
            height=float(self.button_data["height"]),
            corner_radius=float(self.button_data["corner_radius"]),
            bg_color=self.button_data["bg_color"],
            fg_color=self.button_data["fg_color"],
            hover_color=self.button_data["hover_color"],
            text_color=self.button_data["text_color"],
            font=(self.button_data["font_family"], int(self.button_data["font_size"])),
            command=lambda: controller.show_frame(
                "status_page",
                come_from_which_page="install",
                profile_folder=SpecialInputFunc().get_variables(self.profile_folder_name_entry),
                application_folder=SpecialInputFunc().get_variables(self.application_folder_entry),
                new_tab_wallpaper=SpecialInputFunc().get_variables(self.newtab_wallpaper_entry),
                accent_color=self.get_variables_combobox(self.accent_color_combobox),
            ),
            image=self.install_button_image,
            text="Install",
            compound="right",
        )

        self.install_button.pack(padx=(5, 20), pady=10, side="right")

        back_button = CTkButton(
            master=navigation_frame,
            width=float(self.button_data["width"]),
            height=float(self.button_data["height"]),
            corner_radius=float(self.button_data["corner_radius"]),
            bg_color=self.button_data["bg_color"],
            fg_color=self.button_data["fg_color"],
            hover_color=self.button_data["hover_color"],
            text_color=self.button_data["text_color"],
            font=(self.button_data["font_family"], int(self.button_data["font_size"])),
            command=lambda: controller.show_frame("home_page"),
            image=self.back_button_image,
            text="Back",
        )

        back_button.pack(padx=5, pady=10, side="right")

        exit_button = CTkButton(
            master=navigation_frame,
            width=float(self.button_data["width"]),
            height=float(self.button_data["height"]),
            corner_radius=float(self.button_data["corner_radius"]),
            bg_color=self.button_data["bg_color"],
            fg_color=self.button_data["fg_color"],
            hover_color=self.button_data["hover_color"],
            text_color=self.button_data["text_color"],
            font=(self.button_data["font_family"], int(self.button_data["font_size"])),
            command=lambda: CombinedModal(self, "Exit"),
            image=self.exit_button_image,
            text="Exit",
        )

        exit_button.pack(padx=(20, 5), pady=10, side="left")

        """
            ///////////////////////////////
            /Operation System Declarations/
            ///////////////////////////////
                                            """
        os_frame = CTkFrame(
            master=bottom_frame,
            # width=440,  # Adjust initial width as needed
            # height=54,
            corner_radius=12,
            fg_color="white",
        )
        os_frame.grid(row=0, column=0, padx=20, sticky="W")

        os_label = CTkLabel(
            master=os_frame,
            text=self.os_values["os_name"] + " ",  # Initial text (can be empty)
            text_color=self.os_values["os_color"],
            font=("Arial", 20, "bold"),  # Adjust font size and family as needed
            image=self.os_icon_image,
            compound="right",
        )

        os_label.pack(padx=10, pady=10, side="right")  # Pad the label within the frame
        self.update_button_and_frame()
        self.checkbox_event()


    """
        //////////////////////////////
        /Other Functions Declarations/
        //////////////////////////////
                                        """
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


    def get_variables_combobox(self, combobox_widget):
        selected_value = combobox_widget.get()
        if selected_value:
            return selected_value
        else:
            return "blue"
        
    def key_bind(self, entry_widget, file_extension=None):
        entry_widget.bind(
            "<KeyRelease>",
            lambda event: self.on_key_release(entry_widget, file_extension),
        )
        entry_widget.bind(
            "<FocusOut>",
            lambda event: self.on_key_release(entry_widget, file_extension),
        )

    def on_key_release(self, entry_widget, file_extension):
        SpecialInputFunc().validate_file_location(entry_widget, file_extension)
        self.update_button_and_frame()

    def update_button_and_frame(self):
        if SpecialInputFunc().update_invalid_entries_display():
            self.install_button.configure(state="normal")
            self.invalid_entry_frame.grid_remove()
        else:
            self.install_button.configure(state="disabled")
            self.invalid_entries_text.configure(
                text=f"  {len(SpecialInputFunc().return_invalid_entries())} entries is invalid"
            )
            self.invalid_entry_frame.grid()

    def update_parameters(self, **kwargs):
        pass

    def checkbox_event(self):
        if self.check_var.get() == "on":
            # Enable entries
            self.accent_color_combobox.configure(state="normal")
            self.newtab_wallpaper_entry.configure(state="normal")
            self.application_folder_entry.configure(state="normal")
            self.profile_folder_name_entry.configure(state="normal")
        else:
            # Disable entries
            self.accent_color_combobox.configure(state="disabled")
            self.newtab_wallpaper_entry.configure(state="disabled")
            self.application_folder_entry.configure(state="disabled")
            self.profile_folder_name_entry.configure(state="disabled")
