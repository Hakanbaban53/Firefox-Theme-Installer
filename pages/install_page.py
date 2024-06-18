from json import load
from os import path

from tkinter import colorchooser
from customtkinter import (
    CTkFrame,
    CTkImage,
    CTkLabel,
    CTkFont,
    CTkButton,
    CTkEntry,
    CTkCheckBox,
    StringVar,
    CTkComboBox,
)
from PIL import Image

from modals.combined_modal import CombinedModal
from functions.get_os_properties import OSProperties
from functions.get_folder_locations import get_profile_folder
from functions.special_input_functions import SpecialInputFunc

class InstallPage(CTkFrame):
    def __init__(self, parent, controller, base_dir):
        super().__init__(parent)
        self.controller = controller
        self.base_dir = base_dir
        
        self.ICON_PATH = path.join(self.base_dir, "assets", "icons/")
        self.BACKGROUND_PATH = path.join(self.base_dir, "assets", "backgrounds/")
        self.DATA_PATH = path.join(self.base_dir, "data", "installer_data.json")

        self.os_values = OSProperties(self.DATA_PATH).get_values()
        self.input_values = OSProperties(self.DATA_PATH).get_locations()
        self.profile_folder_location = get_profile_folder(self.DATA_PATH)

        self.load_text_data()
        self.button_data = self.text_data.get("common_values")["navigation_buttons"]
        self.input_data = self.text_data.get("common_values")["inputs"]

        self.configure_layout()
        self.create_widgets()

    def load_text_data(self):
        with open(self.DATA_PATH, "r", encoding="utf-8") as file:
            self.text_data = load(file)

    def load_image(self, file_name, size):
        return CTkImage(
            light_image=Image.open(file_name),
            dark_image=Image.open(file_name),
            size=size,
        )

    def configure_layout(self):
        self.fg_color = "#2B2631"
        self.grid(row=0, column=1, sticky="SW")
        self.columnconfigure(0, weight=1)

        self.install_page_frame = CTkFrame(
            self,
            fg_color="#2B2631",
        )
        self.install_page_frame.grid(row=0, column=0, sticky="SW")
        self.install_page_frame.columnconfigure(0, weight=1)

    def create_widgets(self):
        self.create_header()
        self.create_inputs()
        self.create_invalid_entry_frame()
        self.create_bottom_widgets()
        self.update_button_and_frame()
        self.checkbox_event()

    def create_header(self):
        header_title_bg = self.load_image(
            f"{self.BACKGROUND_PATH}header_title_background.png", (300, 64)
        )
        line_top_img = self.load_image(f"{self.BACKGROUND_PATH}line_top.png", (650, 6))

        header_label = CTkLabel(
            self.install_page_frame,
            text="Install RealFire",
            image=header_title_bg,
            text_color="White",
            font=CTkFont(family="Inter", size=24, weight="bold"),
            bg_color="#2B2631",
        )
        header_label.grid(
            row=0, column=0, columnspan=2, padx=248, pady=(75, 0), sticky="NSEW"
        )

        line_top_label = CTkLabel(self.install_page_frame, text="", image=line_top_img)
        line_top_label.grid(
            row=1, column=0, columnspan=2, padx=10, pady=(20, 30), sticky="NSEW"
        )

    def create_inputs(self):
        inputs_frame = CTkFrame(
            self.install_page_frame,
            width=440,
            height=54,
            corner_radius=12,
            fg_color="#2B2631",
        )
        inputs_frame.grid(
            row=2, column=0, columnspan=2, padx=40, pady=(20, 30), sticky="NSEW"
        )

        self.create_input_widgets(inputs_frame)
        self.create_edit_checkbox(inputs_frame)

    def create_input_widgets(self, frame):
        # Profile Name
        self.profile_folder_label = CTkLabel(
            master=frame,
            text_color="white",
            font=CTkFont(family="Inter", size=18, weight="bold"),
            text="Profile Folder",
        )
        self.profile_folder_label.grid(row=0, column=0, padx=(10, 4), pady=(14,2), sticky="w")

        self.profile_folder_entry = CTkEntry(
            master=frame,
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
        self.profile_folder_entry.grid(
            row=1, column=0, padx=(10, 4), pady=10, sticky="ew"
        )

        # Application Folder
        self.application_folder_label = CTkLabel(
            master=frame,
            text_color="white",
            font=CTkFont(family="Inter", size=18, weight="bold"),
            text="Application Folder",
        )
        self.application_folder_label.grid(row=0, column=1, padx=(10, 4), pady=(14,2), sticky="w")

        self.application_folder_entry = CTkEntry(
            master=frame,
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
            master=frame,
            text_color="white",
            font=CTkFont(family="Inter", size=18, weight="bold"),
            text="New Tab Wallpaper Location",
        )
        self.newtab_wallpaper_label.grid(row=2, column=0, padx=(10, 4), pady=(14,2), sticky="w")

        self.newtab_wallpaper_entry = CTkEntry(
            master=frame,
            width=int(self.input_data["width"]),
            height=int(self.input_data["height"]),
            fg_color=self.input_data["fg_color"],
            text_color=self.input_data["text_color"],
            corner_radius=int(self.input_data["corner_radius"]),
            border_width=int(self.input_data["border_width"]),
            bg_color=self.input_data["bg_color"],
            border_color=self.input_data["border_color"],
            placeholder_text="Default Wallpaper",
        )
        self.newtab_wallpaper_entry.grid(
            row=3, column=0, padx=(10, 4), pady=10, sticky="ew"
        )


        # Accent Color
        self.accent_color_label = CTkLabel(
            master=frame,
            text_color="white",
            font=CTkFont(family="Inter", size=18, weight="bold"),
            text="Accent Color",
        )
        self.accent_color_label.grid(row=2, column=1, padx=(10, 4), pady=(14,2), sticky="w")

        self.default_color = None
        self.accent_color_values = {
            "RealFire Purple": "#771D76",
            "RealFire Orange": "#F08D27",
            "Blue": "#0000FF",
            "Red": "#FF0000",
            "AccentColor": "accentColor",
            "Custom": None  # Placeholder for custom color
        }
        self.selected_color = None  # Store custom color

        initial_color = self.default_color if self.default_color else self.accent_color_values["RealFire Purple"]

        self.accent_color_combobox = CTkComboBox(
            master=frame,
            width=int(self.input_data["width"]),
            height=int(self.input_data["height"]),
            fg_color=self.input_data["fg_color"],
            text_color=self.input_data["text_color"],
            corner_radius=int(self.input_data["corner_radius"]),
            border_width=int(self.input_data["border_width"]),
            bg_color=self.input_data["bg_color"],
            border_color=self.input_data["border_color"],
            button_color=initial_color,
            button_hover_color=initial_color,
            values=list(self.accent_color_values.keys()),
            command=self.on_accent_color_select,
        )

        if self.default_color:
            self.accent_color_combobox.set(self.default_color)
        else:
            self.accent_color_combobox.set("AccentColor")


        self.accent_color_combobox.grid(
            row=3, column=1, padx=(10, 4), pady=10, sticky="ew"
        )


        self.key_bind(self.profile_folder_entry)
        self.key_bind(self.application_folder_entry)
        self.key_bind(self.application_folder_entry)
        self.key_bind(self.newtab_wallpaper_entry, {".png", ".jpg", ".jpeg", ".gif"})


    def create_edit_checkbox(self, frame):
        self.check_var = StringVar(value="off")
        edit_checkbox = CTkCheckBox(
            master=frame,
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
        edit_checkbox.grid(row=5, column=1, padx=(10, 4), pady=10, sticky="ew")

    def create_invalid_entry_frame(self):
        self.invalid_entry_frame = CTkFrame(
            self.install_page_frame,
            width=440,
            height=54,
            corner_radius=12,
            bg_color="#2B2631",
            fg_color="white",
        )
        self.invalid_entry_frame.grid(
            row=4, column=0, columnspan=2, padx=(10, 4), pady=10
        )

        attention_icon = self.load_image(f"{self.ICON_PATH}attention.png", (24, 24))
        self.invalid_entries_text = CTkLabel(
            self.invalid_entry_frame,
            text="",
            text_color="#f04141",
            font=("Arial", 16, "bold"),
            image=attention_icon,
            compound="left",
        )
        self.invalid_entries_text.pack(padx=10, pady=10)

    def create_bottom_widgets(self):
        bottom_frame = CTkFrame(self, fg_color="#2B2631")
        bottom_frame.place(x=190.0, y=600.0)

        navigation_frame = CTkFrame(
            bottom_frame,
            width=440,
            height=54,
            corner_radius=12,
            border_width=4,
            bg_color="#2B2631",
            fg_color="white",
            border_color="#F89F24",
        )
        navigation_frame.grid(row=0, column=1, sticky="E")

        self.create_navigation_buttons(navigation_frame)
        self.create_os_info(bottom_frame)

    def create_navigation_buttons(self, parent):
        self.install_button = self.create_navigation_button(
            parent,
            "Install",
            self.ICON_PATH + "install_icon.png",
            command=lambda: self.controller.show_frame(
                "status_page",
                come_from_which_page="install",
                profile_folder=SpecialInputFunc().get_variables(self.profile_folder_entry),
                application_folder=SpecialInputFunc().get_variables(self.application_folder_entry),
                new_tab_wallpaper=SpecialInputFunc().get_variables(self.newtab_wallpaper_entry),
                accent_color=self.get_variables_combobox(self.accent_color_combobox),
            ),
            padding_x=(10, 20),
            side="right",
            img_side="right",
        )

        self.back_button = self.create_navigation_button(
            parent,
            "Back",
            self.ICON_PATH + "back_icon.png",
            padding_x=(5, 5),
            side="right",
            command=lambda: self.controller.show_frame("home_page"),
        )
        self.create_navigation_button(
            parent,
            "Exit",
            self.ICON_PATH + "exit_icon.png",
            lambda: CombinedModal(self, self.base_dir, "Exit"),
            padding_x=(20, 10),
            side="left",
        )

    def create_navigation_button(
        self,
        parent,
        text,
        image_path,
        command,
        padding_x,
        side,
        img_side="left",
        **kwargs,
    ):
        button_image = self.load_image(image_path, (20, 20))
        button = CTkButton(
            parent,
            width=float(self.button_data["width"]),
            height=float(self.button_data["height"]),
            corner_radius=float(self.button_data["corner_radius"]),
            bg_color=self.button_data["bg_color"],
            fg_color=self.button_data["fg_color"],
            hover_color=self.button_data["hover_color"],
            text_color=self.button_data["text_color"],
            font=(self.button_data["font_family"], int(self.button_data["font_size"])),
            image=button_image,
            text=text,
            compound=img_side,
            command=command,
            **kwargs,
        )
        button.pack(padx=padding_x, pady=10, side=side)
        return button

    def create_os_info(self, parent):
        os_icon_image = self.load_image(
            f"{self.ICON_PATH}{self.os_values['os_name'].lower()}.png", (20, 24)
        )

        os_frame = CTkFrame(parent, corner_radius=12, fg_color="white")
        os_frame.grid(row=0, column=0, padx=20, sticky="W")

        os_label = CTkLabel(
            os_frame,
            text=f"{self.os_values['os_name']} ",
            text_color=self.os_values["os_color"],
            font=("Arial", 20, "bold"),
            image=os_icon_image,
            compound="right",
        )
        os_label.pack(padx=10, pady=10, side="right")

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

    def on_accent_color_select(self, choice):
        if choice.lower() == "custom":
            self.selected_color = colorchooser.askcolor(title="Choose your color")[1]
            if self.selected_color:
                self.accent_color_combobox.set(self.selected_color)
                if self.selected_color=="accentColor":
                    self.accent_color_combobox.configure(button_color="#771D76", button_hover_color="#771D76")
                else:
                    self.accent_color_combobox.configure(button_color=self.selected_color, button_hover_color=self.selected_color)
        else:
            self.selected_color = self.accent_color_values.get(choice, "#0000FF")
            if self.selected_color=="accentColor":
                self.accent_color_combobox.configure(button_color="#771D76", button_hover_color="#771D76")
            else:
                self.accent_color_combobox.configure(button_color=self.selected_color, button_hover_color=self.selected_color)

    def get_variables_combobox(self, combobox_widget):
        selected_value = combobox_widget.get()
        return selected_value if selected_value else "Blue"

    def checkbox_event(self):
        if self.check_var.get() == "on":
            self.application_folder_entry.configure(state="normal")
            self.profile_folder_entry.configure(state="normal")
            self.newtab_wallpaper_entry.configure(state="normal")
            self.accent_color_combobox.configure(state="normal")
        else:
            self.application_folder_entry.configure(state="disabled")
            self.profile_folder_entry.configure(state="disabled")
            self.newtab_wallpaper_entry.configure(state="disabled")
            self.accent_color_combobox.configure(state="disabled")

    def update_parameters(self, **kwargs):
        pass
