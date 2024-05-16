from json import load
from customtkinter import CTkFrame, CTkImage, CTkLabel, CTkFont, CTkFrame, CTkButton, CTkEntry, CTkCheckBox, StringVar
from PIL import Image
from modals.combined_modal import CombinedModal
from functions.get_os_properties import OSProperties
from functions.get_folder_locations import get_profile_folder
from functions.special_input_functions import SpecialInputFunc


class remove_page(CTkFrame):
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
        self.remove_button_image = CTkImage(
            dark_image=Image.open("../RealFire-Installer/assets/icons/remove_icon.png"),
            light_image=Image.open(
                "../RealFire-Installer/assets/icons/remove_icon.png"
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


        """
            //////////////////////////////
            ///Remove Page Declarations///
            //////////////////////////////
                                            """
        remove_page_frame = CTkFrame(
            self,
            fg_color="#2B2631",
            # border_width=4,
            # bg_color="#2B2631",
            # border_color="#F89F24",
        )
        remove_page_frame.grid(row=0, column=1, sticky="SW")
        remove_page_frame.columnconfigure(0, weight=1)

        self.header_title_background_label = CTkLabel(
            master=remove_page_frame,
            text="Remove RealFire",
            image=self.header_title_background,
            text_color="White",
            font=CTkFont(family="Inter", size=24, weight="bold"),
            bg_color="#2B2631",
        )
        self.header_title_background_label.grid(
            row=0, column=0, columnspan=2, padx=248, pady=(75, 0), sticky="NSEW"
        )

        self.line_top_image_label = CTkLabel(
            master=remove_page_frame,
            text="",
            image=self.line_top_image,
        )
        self.line_top_image_label.grid(
            row=1, column=0, columnspan=2, padx=10, pady=(20, 30), sticky="NSEW"
        )

        inputs_frame = CTkFrame(
            master=remove_page_frame,
            width=440,
            height=54,
            corner_radius=12,
            fg_color="#2B2631",
        )
        inputs_frame.grid(
            row=2, column=0, columnspan=2, padx=10, pady=(20, 30), sticky="NSEW"
        )

        """
            //////////////////////////////
            ////Entries Declarations////
            //////////////////////////////
                                            """
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
            bg_color=self.input_data["bg_color"],
            text_color=self.input_data["text_color"],
            border_color=self.input_data["border_color"],
            border_width=int(self.input_data["border_width"]),
            corner_radius=int(self.input_data["corner_radius"]),
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
            bg_color=self.input_data["bg_color"],
            text_color=self.input_data["text_color"],
            border_color=self.input_data["border_color"],
            border_width=int(self.input_data["border_width"]),
            corner_radius=int(self.input_data["corner_radius"]),
            placeholder_text=self.input_values["application_folder"],
        )
        self.application_folder_entry.grid(
            row=1, column=1, padx=(10, 4), pady=10, sticky="ew"
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
            font=(self.button_data["font_family"], int(self.button_data["font_size"]) - 4),
        )
        self.edit_checkbox.grid(row=3, column=1, padx=10, pady=10, sticky="NSEW")


        """
            //////////////////////////////
            ////Key Bind Declarations////
            //////////////////////////////
                                            """
        self.key_bind(self.profile_folder_name_entry)
        self.key_bind(self.application_folder_entry)
        

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
            row=4, column=0, columnspan=2, padx=(10, 4), pady=10
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

        navigation_frame.grid(row=0, column=1, padx=20, sticky="E")

        self.remove_button = CTkButton(
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
                come_from_which_page="remove",
                profile_folder=SpecialInputFunc().get_variables(self.profile_folder_name_entry),
                application_folder=SpecialInputFunc().get_variables(self.application_folder_entry),
            ),
            image=self.remove_button_image,
            compound="right",
            text="Remove",
        )

        self.remove_button.pack(padx=(5, 20), pady=10, side="right")

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
    def key_bind(self, entry_widget):
        entry_widget.bind(
            "<KeyRelease>",
            lambda event: self.on_key_release(entry_widget),
        )
        entry_widget.bind(
            "<FocusOut>",
            lambda event: self.on_key_release(entry_widget),
        )

    def on_key_release(self, entry_widget):
        SpecialInputFunc().validate_file_location(entry_widget)
        self.update_button_and_frame()

    def update_button_and_frame(self):
        if SpecialInputFunc().update_invalid_entries_display():
            self.remove_button.configure(state="normal")
            self.invalid_entry_frame.grid_remove()
        else:
            self.remove_button.configure(state="disabled")
            self.invalid_entries_text.configure(
                text=f"  {len(SpecialInputFunc().return_invalid_entries())} entries is invalid"
            )
            self.invalid_entry_frame.grid()

    def update_parameters(self, **kwargs):
        pass

    def checkbox_event(self):
        if self.check_var.get() == "on":
            # Enable entries
            self.application_folder_entry.configure(state="normal")
            self.profile_folder_name_entry.configure(state="normal")

        else:
            # Disable entries
            self.application_folder_entry.configure(state="disabled")
            self.profile_folder_name_entry.configure(state="disabled")
