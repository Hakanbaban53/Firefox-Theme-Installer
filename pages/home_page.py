from json import load
from time import sleep
from tkinter import PhotoImage, Label, TclError
from itertools import cycle
from customtkinter import CTkFrame, CTkImage, CTkLabel, CTkFrame, CTkButton, StringVar, CTkCheckBox
from PIL import Image
from modals.check_files_modal import FileInstallerModal
from modals.combined_modal import CombinedModal
from functions.get_os_properties import OSProperties
from threading import Thread
from functions.detect_files import FileManager



class home_page(CTkFrame):
    os_values = OSProperties().get_values()

    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
        self.controller = controller
        self.text_data = {}
        with open("../RealFire-Installer/data/installer_data.json", "r") as file:
            self.text_data = load(file)

        self.button_data = self.text_data.get("common_values")["navigation_buttons"]


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
            size=(390, 64),
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

        self.select_action_image = CTkImage(
            light_image=Image.open(
                "../RealFire-Installer/assets/backgrounds/header_title_background.png"
            ),
            dark_image=Image.open(
                "../RealFire-Installer/assets/backgrounds/header_title_background.png"
            ),
            size=(270, 36),
        )

        self.remove_button_image = CTkImage(
            dark_image=Image.open("../RealFire-Installer/assets/icons/remove_icon.png"), 
            light_image=Image.open("../RealFire-Installer/assets/icons/remove_icon.png"), 
            size=(20, 24)
        )

        self.install_button_image = CTkImage(
            dark_image=Image.open("../RealFire-Installer/assets/icons/install_icon.png"), 
            light_image=Image.open("../RealFire-Installer/assets/icons/install_icon.png"), 
            size=(20, 20)
        )

        self.exit_button_image = CTkImage(
            dark_image=Image.open("../RealFire-Installer/assets/icons/exit_icon.png"), 
            light_image=Image.open("../RealFire-Installer/assets/icons/exit_icon.png"), 
            size=(20, 20)
        )
        self.reload_icon = CTkImage(
            light_image=Image.open(
                "../RealFire-Installer/assets/icons/reload_icon.png"
            ),
            dark_image=Image.open(
                "../RealFire-Installer/assets/icons/reload_icon.png"
            ),
            size=(20, 20),
        )


        self.attention_icon = PhotoImage(file="../RealFire-Installer/assets/icons/attention.png", height=24, width=24)
        self.check_icon = PhotoImage(file="../RealFire-Installer/assets/icons/check.png", height=20, width=20)

        """
            //////////////////////////////
            ////Home Page Declarations////
            //////////////////////////////
                                            """
        home_page_frame = CTkFrame(
            self,
            fg_color="#2B2631",
            # border_width=4,
            # bg_color="#2B2631",
            # border_color="#F89F24",
        )
        home_page_frame.grid(
            row=0, column=1, sticky="SW"
        )
        home_page_frame.columnconfigure(0, weight=1)

        self.header_title_background_label = CTkLabel(
            master=home_page_frame,
            text="Welcome the RealFire Installer",
            image=self.header_title_background,
            text_color="White",
            font=("Inter", 24, "bold"),
        )
        self.header_title_background_label.grid(
            row=0, column=0, columnspan=2, padx=203, pady=(75,0), sticky="NSEW"
        )

        self.line_top_image_label = CTkLabel(
            master=home_page_frame,
            text="",
            image=self.line_top_image,
        )
        self.line_top_image_label.grid(row=1, column=0, columnspan=2, padx=10, pady=(20,30), sticky="NSEW")


        """
            ///////////////////////////////
            /Operation System Declarations/
            ///////////////////////////////
                                            """
        operation_system = CTkLabel(
            master=home_page_frame,
            text="Detected Operation System: ",
            text_color="White",
            font=("Inter", 20, "bold"),
        )
        operation_system.grid(row=2, column=0, columnspan=1, padx=(175,0), sticky="ew")

        os_frame = CTkFrame(
            master=home_page_frame,
            # width=440,  # Adjust initial width as needed
            # height=54,
            corner_radius=12,
            fg_color="white",
        )
        os_frame.grid(row=2, column=1, columnspan=1, padx=(0,185), sticky="ew")

        os_label = CTkLabel(
            master=os_frame,
            text=self.os_values["os_name"] + " ",  # Initial text (can be empty)
            text_color=self.os_values["os_color"],
            font=("Arial", 20, "bold"),  # Adjust font size and family as needed
            image=self.os_icon_image,
            compound="right",
        )

        os_label.pack(
            padx=10, pady=10, side="left"
        )  # Pad the label within the frame




        """
            /////////////////////////////
            ///Navigation Declarations///
            /////////////////////////////
                                        """
        self.select_action_label = CTkLabel(
            master=home_page_frame,
            text="Please Select the Action",
            image=self.select_action_image,
            text_color="White",
            font=("Inter", 20, "bold"),
        )
        self.select_action_label.grid(
            row=3, column=0, columnspan=2, padx=60, pady=(70,30), sticky="ew"
        )

        navigation_frame = CTkFrame(
            master=home_page_frame,
            width=460,
            height=54,
            corner_radius=12,
            border_width=4,
            fg_color="white",
            border_color="#F89F24",
        )
        navigation_frame.grid(row=4, column=0, columnspan=2, sticky="")

        remove_button = CTkButton(
            master=navigation_frame,
            width=float(self.button_data["width"]),
            height=float(self.button_data["height"]),
            corner_radius=float(self.button_data["corner_radius"]),
            bg_color=self.button_data["bg_color"],
            fg_color=self.button_data["fg_color"],
            hover_color=self.button_data["hover_color"],
            text_color=self.button_data["text_color"],
            font=(self.button_data["font_family"], int(self.button_data["font_size"])),
            image=self.remove_button_image,
            text="Remove",
            compound="right",
            command=lambda: controller.show_frame("remove_page"),
        )
        remove_button.pack(padx=(5, 20), pady=10, side="right")

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
            state="disabled",
            image=self.install_button_image,
            text="Install",
            command=lambda: controller.show_frame("install_page"),
        )
        self.install_button.pack(padx=5, pady=10, side="right")

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
            image=self.exit_button_image,
            text="Exit",
            command=lambda: CombinedModal(self, "Exit"),
        )
        exit_button.pack(padx=(20, 5), pady=10, side="left")

        """
            ///////////////////////////
            /Detect Files Declarations/
            ///////////////////////////
                                        """
        self.detect_files_frame = CTkFrame(
            master=home_page_frame,
            corner_radius=12,
            fg_color="white",
        )
        self.detect_files_frame.grid(row=5, column=0, padx=0, pady=(20,10), columnspan=2, sticky="")

        self.detect_files_text = Label(
            master=self.detect_files_frame,
            text="Checking The Files   ",
            fg="#000000",
            bg="#FFFFFF",
            font=("Arial", 16, "bold"),
            compound="right",
        )
        self.detect_files_text.grid(row=0, column=0, padx=10, pady=10, sticky="")
        thread = Thread(target=self.locate_files)
        thread.start()

        self.install_files_button = CTkButton(
            master=self.detect_files_frame,
            text="Install Missing Files",
            width=float(self.button_data["width"]),
            height=float(self.button_data["height"]),
            corner_radius=float(self.button_data["corner_radius"]),
            bg_color=self.button_data["bg_color"],
            fg_color=self.button_data["fg_color"],
            hover_color=self.button_data["hover_color"],
            text_color=self.button_data["text_color"],
            font=(self.button_data["font_family"], int(self.button_data["font_size"])),
            command=self.install_files,
        )
        
        self.recheck_skip_frame = CTkFrame(
            master=home_page_frame,
            fg_color= "#2B2631"
        )
        self.recheck_skip_frame.grid(row=6, column=0, padx=0, pady=0, columnspan=2, sticky="")
        
        self.check_var = StringVar(value="off")
        self.user_know_what_do = CTkCheckBox(
            self.recheck_skip_frame,
            text="I know what I do",
            text_color="#FFFFFF",
            font=("Arial", 16, "bold"),
            command=self.checkbox_event,
            variable=self.check_var,
            onvalue="on",
            offvalue="off",
        )

        self.recheck_button = CTkButton(
            self.recheck_skip_frame,
            width=40,
            height=40,
            text="",
            fg_color= "#FFFFFF",
            command=self.recheck_files,  # Bind the recheck_files method
            image=self.reload_icon
        )
        self.recheck_button.grid(row=1, column=0, padx=0, pady=0, columnspan=2, sticky="")


    """
        //////////////////////////////
        /Other Functions Declarations/
        //////////////////////////////
                                        """

    def load_gif(self):
        kareler = []
        sayac = 0
        while True:
            try:
                kare = PhotoImage(file="../RealFire-Installer/assets/icons/block_spin.gif", format=f'gif -index {sayac}')
                kareler.append(kare)
                sayac += 2
            except TclError:
                break
        return cycle(kareler)

    def update_fps(self, kareler):
        kare = next(kareler)
        self.detect_files_text.config(image=kare)
        self.animasyon_id = self.master.after(100, self.update_fps, kareler)

    def recheck_files(self):
        self.detect_files_text.config(text="Checking The Files  ", fg="#000000")
        self.install_button.configure(state="disabled")
        self.install_files_button.grid_remove()
        self.user_know_what_do.grid_remove()
        thread = Thread(target=self.locate_files)
        thread.start()

    def install_files(self):
        modal = FileInstallerModal(self, self.detect_files_text, self.install_button)
        self.wait_window(modal)
        self.recheck_files()

    def locate_files(self):
        kareler = self.load_gif()
        self.update_fps(kareler)
        sleep(1)
        self.file_check_result = FileManager("../RealFire-Installer/data/installer_files_data.json").check_files_exist()
        self.master.after_cancel(self.animasyon_id)
        if len(self.file_check_result) == 0:
            self.master.after_cancel(self.animasyon_id)
            self.detect_files_text.config(text="All Files Installed  ", fg="#10dc60", image=self.check_icon)
            self.install_button.configure(state="normal")
            self.recheck_button.grid(row=6, column=0, padx=0, pady=0, sticky="")
            self.user_know_what_do.grid_remove()

        else:
            self.master.after_cancel(self.animasyon_id)
            self.detect_files_text.config(text="Some Files Are Missing  ", fg="#f04141", image=self.attention_icon)
            self.install_files_button.grid(row=1, column=0, padx=10, pady=10, sticky="")
            self.user_know_what_do.grid(row=6, column=0, padx=10, pady=0, sticky="")
            self.recheck_button.grid(row=6, column=1, padx=10, pady=0, sticky="")

        
    def checkbox_event(self):
        if self.user_know_what_do.get() == "on":
            self.install_button.configure( 
                state="normal"
            )
            self.install_files_button.configure(
                state="disabled"
            )
            self.detect_files_text.config(
                text="Skipped by User  ",
                fg="#f04141",
                image=self.attention_icon
            )
            self.recheck_button.configure(
                state="disabled"
            )
        else:
            self.install_button.configure(
                state="disabled"
            )
            self.install_files_button.configure(
                state="normal"
            )
            self.detect_files_text.config(
                text="Some Files Are Missing  ",
                fg="#f04141",
                image=self.attention_icon
            )
            self.recheck_button.configure(
                state="normal"
            )

    def update_parameters(self, **kwargs):
        # Process and use the parameters as needed
        pass
