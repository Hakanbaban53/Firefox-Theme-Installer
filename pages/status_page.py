from json import load
from threading import Thread
from customtkinter import CTkFrame, CTkImage, CTkLabel, CTkFont, CTkFrame, CTkProgressBar, CTkTextbox, CTkButton
from PIL import Image
from modals.combined_modal import CombinedModal
from functions.get_os_properties import OSProperties
from functions.install_files import FileActions


class status_page(CTkFrame):
    os_values = OSProperties().get_values()

    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
        self.controller = controller
        self.file_actions = FileActions()

        self.come_from_which_page = None
        with open("../RealFire-Installer/data/installer_data.json", "r") as file:
            self.text_data = load(file)

        self.button_data = self.text_data.get("common_values")["navigation_buttons"]

        #self.bind("<Visibility>", self.start_simulate_progress)

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
            size=(250, 64),
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
        self.check_icon = CTkImage(
            light_image=Image.open(
                "../RealFire-Installer/assets/icons/check.png"
            ),
            dark_image=Image.open(
                "../RealFire-Installer/assets/icons/check.png"
            ),
            size=(20, 20),
        )
        self.finish_button_image = CTkImage(
            dark_image=Image.open(
                "../RealFire-Installer/assets/icons/finish_icon.png"
                ),
            light_image=Image.open(
                "../RealFire-Installer/assets/icons/finish_icon.png"
            ),
            size=(20, 20),
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
            ///Status Page Declarations///
            //////////////////////////////
                                            """
        status_page_frame = CTkFrame(
            self,
            fg_color="#2B2631",
            # border_width=4,
            # bg_color="#2B2631",
            # border_color="#F89F24",
        )
        status_page_frame.grid(row=0, column=1, sticky="SW")
        status_page_frame.columnconfigure(0, weight=1)

        self.header_title_background_label = CTkLabel(
            master=status_page_frame,
            text="Status",
            image=self.header_title_background,
            text_color="White",
            font=CTkFont(family="Inter", size=24, weight="bold"),
        )
        self.header_title_background_label.grid(
            row=0, column=0, columnspan=2, padx=273, pady=(75, 0), sticky="NSEW"
        )

        self.line_top_image_label = CTkLabel(
            master=status_page_frame,
            text="",
            image=self.line_top_image,
        )
        self.line_top_image_label.grid(
            row=1, column=0, columnspan=2, padx=10, pady=(20, 30), sticky="NSEW"
        )


        self.action_label = CTkLabel(
            master=status_page_frame,
            fg_color="#2B2631",
            text_color="#FFFFFF",
            text="",
            image=None,
            compound="right",
            font=CTkFont(family="Inter", size=18, weight="bold"),
        )
        self.action_label.grid(row=2, column=0, padx=60, pady=10, sticky="W")

        self.progress_bar = CTkProgressBar(
            master=status_page_frame,
            orientation="horizontal",
            height=24,
            fg_color="#666666",
            progress_color="#9747FF",
        )
        self.progress_bar.grid(row=3, column=0, padx=50, pady=10, sticky="NSEW")
        self.progress_bar.set(0)

        self.output_entry = CTkTextbox(
            master=status_page_frame,
            height=190,
            fg_color="white",
            text_color="black",
            corner_radius=12,
        )
        self.output_entry.grid(row=4, column=0, padx=60, pady=20, sticky="NSEW")


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
            fg_color="white",
            border_color="#F89F24",
        )
        navigation_frame.grid(row=0, column=1, sticky="E")

        finish_button = CTkButton(
            master=navigation_frame,
            width=float(self.button_data["width"]),
            height=float(self.button_data["height"]),
            corner_radius=float(self.button_data["corner_radius"]),
            bg_color=self.button_data["bg_color"],
            fg_color=self.button_data["fg_color"],
            hover_color=self.button_data["hover_color"],
            text_color=self.button_data["text_color"],
            font=(self.button_data["font_family"], int(self.button_data["font_size"])),
            text="Finish",
            compound="right",
            command=lambda: CombinedModal(self, "Attention"),
            image=self.finish_button_image,
        )
        finish_button.pack(padx=(5, 20), pady=10, side="right")

        self.back_button = CTkButton(
            master=navigation_frame,
            width=float(self.button_data["width"]),
            height=float(self.button_data["height"]),
            corner_radius=float(self.button_data["corner_radius"]),
            bg_color=self.button_data["bg_color"],
            fg_color=self.button_data["fg_color"],
            hover_color=self.button_data["hover_color"],
            text_color=self.button_data["text_color"],
            font=(self.button_data["font_family"], int(self.button_data["font_size"])),
            text="Back",
            state="disabled",
            image=self.back_button_image,
        )
        self.back_button.pack(padx=5, pady=10, side="right")


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
            text="Exit",
            image=self.exit_button_image,
            command=lambda: CombinedModal(self, "Exit"),
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
        
    def update_text(self):
        if self.come_from_which_page == "install":
            self.action_label.configure(text="Installed  ", image=self.check_icon, compound="right")
        elif self.come_from_which_page == "remove":
            self.action_label.configure(text="Removed  ", image=self.check_icon, compound="right")

    def update_parameters(self, **kwargs):
        self.come_from_which_page = kwargs.get("come_from_which_page")
        self.profile_folder = kwargs.get("profile_folder")
        self.application_folder = kwargs.get("application_folder")
        self.new_tab_wallpaper = kwargs.get("new_tab_wallpaper")
        self.accent_color = kwargs.get("accent_color")

        if self.come_from_which_page == "install":
            self.action_label.configure(text="Instaling...")
            self.file_actions.move_file("../RealFire-Installer/fx-autoconfig/config.js", self.application_folder)
            self.file_actions.move_file("../RealFire-Installer/fx-autoconfig/mozilla.cfg", self.application_folder)

            self.file_actions.move_file("../RealFire-Installer/fx-autoconfig/config-prefs.js", f"{self.application_folder}/defaults/pref/")
            self.file_actions.move_file("../RealFire-Installer/fx-autoconfig/local-settings.js", f"{self.application_folder}/defaults/pref/")

            self.file_actions.move_folder("../RealFire-Installer/chrome", self.profile_folder)
            self.file_actions.move_file("../RealFire-Installer/fx-autoconfig/user.js", self.profile_folder)


        elif self.come_from_which_page == "remove":
            self.action_label.configure(text="Removing...")
            self.file_actions.remove_file(f"{self.application_folder}/config.js")
            self.file_actions.remove_file(f"{self.application_folder}/mozilla.cfg")

            self.file_actions.remove_file(f"{self.application_folder}/defaults/pref/config-prefs.js")
            self.file_actions.remove_file(f"{self.application_folder}/defaults/pref/local-settings.js")

            self.file_actions.remove_file(f"{self.profile_folder}/user.js")
            self.file_actions.remove_folder(f"{self.profile_folder}/chrome")

        operation_thread = Thread(target=self.file_actions.execute_operations, args=(self.progress_bar, self.output_entry))
        operation_thread.start()
        
        self.after(500, self.update_text)


        # For Testing
        # self.back_button.configure(
        #     command=lambda: self.controller.show_frame(
        #         f"{self.come_from_which_page}_page"
        #     ),
        # )
