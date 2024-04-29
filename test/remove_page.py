import os
from pathlib import Path
import customtkinter
from custom_exit_message import CombinedModal
from PIL import Image


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(
    r"/home/hakan/Documents/GitHub/pythonInstaller/assets"
)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class remove_page(customtkinter.CTkFrame):
    def __init__(self, parent, controller, os_properties):
        customtkinter.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.os_properties = os_properties

        os_name = self.os_properties.get_os()

        self.invalid_entries = []

        text_color = self.os_properties.get_os_color()

        os_icon_path = self.os_properties.os_icon()

        self.button_font = customtkinter.CTkFont(family="Inter", size=20)

        remove_page_frame = customtkinter.CTkFrame(
            self,
            fg_color="#2B2631",
            # border_width=4,
            # bg_color="#2B2631",
            # border_color="#F89F24",
        )
        remove_page_frame.place(x=311.0, y=0.0)
        remove_page_frame.columnconfigure(0, weight=1)

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
            master=remove_page_frame,
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
            master=remove_page_frame,
            text="",
            image=self.line_top_image,
        )
        self.line_top_image_label.grid(
            row=1, column=0, columnspan=2, padx=10, pady=(20, 30), sticky="NSEW"
        )
        

        inputs_frame = customtkinter.CTkFrame(
            master=remove_page_frame,
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
            placeholder_text="Folder Profile Name",
            corner_radius=8,
            border_width=3,
            bg_color="#2B2631",
            border_color="purple",
        )
        self.profile_folder_name_entry.grid(
            row=1, column=0, padx=(10, 4), pady=10, sticky="ew"
        )
        self.profile_folder_name_entry.bind("<FocusOut>", lambda event: self.validate_file_location(self.profile_folder_name_entry))

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
        self.edit_checkbox.grid(row=3, column=1, padx=(10, 4), pady=10, sticky="ew")

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
            placeholder_text="Firefox Folder Location",
            corner_radius=8,
            border_width=3,
            bg_color="#2B2631",
            border_color="orange",
        )
        self.firefox_folder_entry.grid(
            row=1, column=1, padx=(10, 4), pady=10, sticky="ew"
        )
        self.firefox_folder_entry.bind("<FocusOut>", lambda event: self.validate_file_location(self.firefox_folder_entry))

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
            placeholder_text="Application Folder",
            corner_radius=8,
            border_width=3,
            bg_color="#2B2631",
            border_color="green",
        )
        self.application_folder_entry.grid(
            row=3, column=0, padx=(10, 4), pady=10, sticky="ew"
        )
        self.application_folder_entry.bind("<FocusOut>", lambda event: self.validate_file_location(self.application_folder_entry))

        self.invalid_entry_frame = customtkinter.CTkFrame(
            master=inputs_frame,
            width=440,  # Adjust initial width as needed
            height=54,
            corner_radius=12,
            bg_color="#2B2631",
            fg_color="white",
        )
        self.invalid_entry_frame.grid(row=4, column=0, columnspan=2, padx=(10, 4), pady=10)


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

        image_path = relative_to_assets("icons/remove_icon.png")  # Get the absolute path
        image = Image.open(image_path)
        self.remove_button_image = customtkinter.CTkImage(
            dark_image=image, light_image=image, size=(20, 24)
        )

        self.remove_button = customtkinter.CTkButton(
            master=navigation_frame,
            text="Remove",
            fg_color="#D9D9D9",
            hover_color="#EEEEEE",
            bg_color="white",
            corner_radius=12,
            command=lambda: controller.show_frame(
                "status_page", come_from_which_page="remove",
                profile_folder=self.get_variables(self.profile_folder_name_entry),
                application_folder=self.get_variables(self.application_folder_entry),
                firefox_folder=self.get_variables(self.firefox_folder_entry),
            ),
            width=122.0,
            height=38.0,
            image=self.remove_button_image,
            compound="right",
            text_color="#000000",
            font=self.button_font,
        )

        self.remove_button.pack(padx=(5, 20), pady=10, side="right")

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


    def validate_file_location(self, entry_widget):
        location = entry_widget.get()
        if os.path.exists(location) or location == "":
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
            self.remove_button.configure(state="normal")
            # Hide the invalid entry frame if there are no invalid entries
            self.invalid_entry_frame.grid_remove()
        else:
            self.remove_button.configure(state="disabled")
            # Show the invalid entry frame and update the text with the count of invalid entries
            self.invalid_entries_text.configure(
                text=f"  {len(self.invalid_entries)} entries is invalid"
            )
            self.invalid_entry_frame.grid()

    def exit_confirmation(self):
        print("Remove page exit_confirmation func")
        CombinedModal(self, "Exit")

    def get_variables(self, entry):
        input_value = entry.get()
        placeholder_text = entry.cget("placeholder_text")
        if input_value:
            return input_value
        else:
            return placeholder_text

    def update_parameters(self, **kwargs):
        # # Process and use the parameters as needed
        # self.param1 = kwargs.get("param1")
        # self.param2 = kwargs.get("param2")
        # self.param3 = kwargs.get("param3")

        # self.remove_button.configure(
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
            self.firefox_folder_entry.configure(state="normal")
            self.application_folder_entry.configure(state="normal")
            self.profile_folder_name_entry.configure(state="normal")

        else:
            # Disable entries
            self.firefox_folder_entry.configure(state="disabled")
            self.application_folder_entry.configure(state="disabled")
            self.profile_folder_name_entry.configure(state="disabled")

