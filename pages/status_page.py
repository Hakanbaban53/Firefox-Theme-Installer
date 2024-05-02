import json
import customtkinter
from PIL import Image
from functions.combined_modal import CombinedModal
from functions.get_os_properties import OSProperties


class status_page(customtkinter.CTkFrame):
    os_values = OSProperties().get_values()

    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.come_from_which_page = None
        with open("../RealFire_Installer/data/installer_data.json", "r") as file:
            self.text_data = json.load(file)

        self.button_data = self.text_data.get("common_values")["navigation_buttons"]

        #self.bind("<Visibility>", self.start_simulate_progress)

        """
            /////////////////////////////
            /Image Location Declarations/
            /////////////////////////////
                                        """
        self.header_title_background = customtkinter.CTkImage(
            light_image=Image.open(
                "../RealFire_Installer/assets/backgrounds/header_title_background.png"
            ),
            dark_image=Image.open(
                "../RealFire_Installer/assets/backgrounds/header_title_background.png"
            ),
            size=(250, 64),
        )
        self.line_top_image = customtkinter.CTkImage(
            light_image=Image.open(
                "../RealFire_Installer/assets/backgrounds/line_top.png"
            ),
            dark_image=Image.open(
                "../RealFire_Installer/assets/backgrounds/line_top.png"
            ),
            size=(650, 6),
        )
        self.os_icon_image = customtkinter.CTkImage(
            dark_image=Image.open(f"../RealFire_Installer/assets/icons/{self.os_values["os_name"].lower()}.png"), 
            light_image=Image.open(f"../RealFire_Installer/assets/icons/{self.os_values["os_name"].lower()}.png"),
            size=(20, 24)
        )
        self.check_icon = customtkinter.CTkImage(
            light_image=Image.open(
                "../RealFire_Installer/assets/icons/check.png"
            ),
            dark_image=Image.open(
                "../RealFire_Installer/assets/icons/check.png"
            ),
            size=(20, 20),
        )
        self.finish_button_image = customtkinter.CTkImage(
            dark_image=Image.open(
                "../RealFire_Installer/assets/icons/finish_icon.png"
                ),
            light_image=Image.open(
                "../RealFire_Installer/assets/icons/finish_icon.png"
            ),
            size=(20, 20),
        )
        self.back_button_image = customtkinter.CTkImage(
            dark_image=Image.open("../RealFire_Installer/assets/icons/back_icon.png"),
            light_image=Image.open("../RealFire_Installer/assets/icons/back_icon.png"),
            size=(20, 20),
        )
        self.exit_button_image = customtkinter.CTkImage(
            dark_image=Image.open("../RealFire_Installer/assets/icons/exit_icon.png"),
            light_image=Image.open("../RealFire_Installer/assets/icons/exit_icon.png"),
            size=(20, 20),
        )


        """
            //////////////////////////////
            ///Status Page Declarations///
            //////////////////////////////
                                            """
        status_page_frame = customtkinter.CTkFrame(
            self,
            fg_color="#2B2631",
            # border_width=4,
            # bg_color="#2B2631",
            # border_color="#F89F24",
        )
        status_page_frame.grid(row=0, column=1, sticky="SW")
        status_page_frame.columnconfigure(0, weight=1)

        self.header_title_background_label = customtkinter.CTkLabel(
            master=status_page_frame,
            text="Status",
            image=self.header_title_background,
            text_color="White",
            font=customtkinter.CTkFont(family="Inter", size=24, weight="bold"),
        )
        self.header_title_background_label.grid(
            row=0, column=0, columnspan=2, padx=273, pady=(75, 0), sticky="NSEW"
        )

        self.line_top_image_label = customtkinter.CTkLabel(
            master=status_page_frame,
            text="",
            image=self.line_top_image,
        )
        self.line_top_image_label.grid(
            row=1, column=0, columnspan=2, padx=10, pady=(20, 30), sticky="NSEW"
        )

       
        self.action_label = customtkinter.CTkLabel(
            master=status_page_frame,
            fg_color="#2B2631",
            text_color="#FFFFFF",
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
        )
        self.output_entry.grid(row=4, column=0, padx=60, pady=20, sticky="NSEW")


        """
            /////////////////////////////
            /Bottom Widgets Declarations/
            /////////////////////////////
                                            """
        bottom_frame = customtkinter.CTkFrame(
            self,
            fg_color="#2B2631",
        )
        bottom_frame.place(x=200.0, y=600.0)

        navigation_frame = customtkinter.CTkFrame(
            master=bottom_frame,
            width=440,
            height=54,
            corner_radius=12,
            border_width=4,
            fg_color="white",
            border_color="#F89F24",
        )
        navigation_frame.grid(row=0, column=1, padx=20, sticky="E")

        finish_button = customtkinter.CTkButton(
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

        self.back_button = customtkinter.CTkButton(
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
            # state="disabled",
            image=self.back_button_image,
        )
        self.back_button.pack(padx=5, pady=10, side="right")


        exit_button = customtkinter.CTkButton(
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
        os_frame = customtkinter.CTkFrame(
            master=bottom_frame,
            # width=440,  # Adjust initial width as needed
            # height=54,
            corner_radius=12,
            fg_color="white",
        )
        os_frame.grid(row=0, column=0, padx=20, sticky="W")

        os_label = customtkinter.CTkLabel(
            master=os_frame,
            text=self.os_values["os_name"] + " ",  # Initial text (can be empty)
            text_color=self.os_values["os_color"],
            font=("Arial", 20, "bold"),  # Adjust font size and family as needed
            image=self.os_icon_image,
            compound="right",
        )

        os_label.pack(padx=10, pady=10, side="right")  # Pad the label within the frame
        # self.bind("<Visibility>", self.start_simulate_progress)


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
        
    def update_parameters(self, **kwargs):
        self.come_from_which_page = kwargs.get("come_from_which_page")
        self.profile_folder = kwargs.get("profile_folder")
        self.application_folder = kwargs.get("application_folder")
        self.new_tab_wallpaper = kwargs.get("new_tab_wallpaper")
        self.accent_color = kwargs.get("accent_color")

        if self.come_from_which_page == "install":
            self.action_label.configure(text="Instaling...")
        elif self.come_from_which_page == "remove":
            self.action_label.configure(text="Removing...")

        self.back_button.configure(
            command=lambda: self.controller.show_frame(
                f"{self.come_from_which_page}_page"
            ),
        )
