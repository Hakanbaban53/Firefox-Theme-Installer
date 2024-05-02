import json
import customtkinter
from PIL import Image
from functions.combined_modal import CombinedModal
from functions.get_os_properties import OSProperties



class home_page(customtkinter.CTkFrame):
    os_values = OSProperties().get_values()

    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.text_data = {}
        with open("../RealFire_Installer/data/installer_data.json", "r") as file:
            self.text_data = json.load(file)

        self.button_data = self.text_data.get("common_values")["navigation_buttons"]


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
            size=(390, 64),
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

        self.select_action_image = customtkinter.CTkImage(
            light_image=Image.open(
                "../RealFire_Installer/assets/backgrounds/header_title_background.png"
            ),
            dark_image=Image.open(
                "../RealFire_Installer/assets/backgrounds/header_title_background.png"
            ),
            size=(270, 36),
        )

        self.remove_button_image = customtkinter.CTkImage(
            dark_image=Image.open("../RealFire_Installer/assets/icons/remove_icon.png"), 
            light_image=Image.open("../RealFire_Installer/assets/icons/remove_icon.png"), 
            size=(20, 24)
        )

        self.install_button_image = customtkinter.CTkImage(
            dark_image=Image.open("../RealFire_Installer/assets/icons/install_icon.png"), 
            light_image=Image.open("../RealFire_Installer/assets/icons/install_icon.png"), 
            size=(20, 20)
        )

        self.exit_button_image = customtkinter.CTkImage(
            dark_image=Image.open("../RealFire_Installer/assets/icons/exit_icon.png"), 
            light_image=Image.open("../RealFire_Installer/assets/icons/exit_icon.png"), 
            size=(20, 20)
        )

        self.attention_icon = customtkinter.CTkImage(
            light_image=Image.open("../RealFire_Installer/assets/icons/attention.png"),
            dark_image=Image.open("../RealFire_Installer/assets/icons/attention.png"),
            size=(24, 24),
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


        """
            //////////////////////////////
            ////Home Page Declarations////
            //////////////////////////////
                                            """
        home_page_frame = customtkinter.CTkFrame(
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

        self.header_title_background_label = customtkinter.CTkLabel(
            master=home_page_frame,
            text="Welcome the RealFire Installer",
            image=self.header_title_background,
            text_color="White",
            font=("Inter", 24, "bold"),
        )
        self.header_title_background_label.grid(
            row=0, column=0, columnspan=2, padx=203, pady=(75,0), sticky="NSEW"
        )

        self.line_top_image_label = customtkinter.CTkLabel(
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
        operation_system = customtkinter.CTkLabel(
            master=home_page_frame,
            text="Detected Operation System: ",
            text_color="White",
            font=("Inter", 20, "bold"),
        )
        operation_system.grid(row=2, column=0, columnspan=1, padx=(175,0), sticky="ew")

        os_frame = customtkinter.CTkFrame(
            master=home_page_frame,
            # width=440,  # Adjust initial width as needed
            # height=54,
            corner_radius=12,
            fg_color="white",
        )
        os_frame.grid(row=2, column=1, columnspan=1, padx=(0,185), sticky="ew")

        os_label = customtkinter.CTkLabel(
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
        self.select_action_label = customtkinter.CTkLabel(
            master=home_page_frame,
            text="Please Select the Action",
            image=self.select_action_image,
            text_color="White",
            font=("Inter", 20, "bold"),
        )
        self.select_action_label.grid(
            row=3, column=0, columnspan=2, padx=60, pady=(70,30), sticky="ew"
        )

        navigation_frame = customtkinter.CTkFrame(
            master=home_page_frame,
            width=460,
            height=54,
            corner_radius=12,
            border_width=4,
            fg_color="white",
            border_color="#F89F24",
        )
        navigation_frame.grid(row=4, column=0, columnspan=2, sticky="")

        remove_button = customtkinter.CTkButton(
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

        install_button = customtkinter.CTkButton(
            master=navigation_frame,
            width=float(self.button_data["width"]),
            height=float(self.button_data["height"]),
            corner_radius=float(self.button_data["corner_radius"]),
            bg_color=self.button_data["bg_color"],
            fg_color=self.button_data["fg_color"],
            hover_color=self.button_data["hover_color"],
            text_color=self.button_data["text_color"],
            font=(self.button_data["font_family"], int(self.button_data["font_size"])),
            image=self.install_button_image,
            text="Install",
            command=lambda: controller.show_frame("install_page"),
        )
        install_button.pack(padx=5, pady=10, side="right")

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
        self.detect_files_frame = customtkinter.CTkFrame(
            master=home_page_frame,
            corner_radius=12,
            fg_color="white",
        )
        self.detect_files_frame.grid(row=5, column=0, padx=0, pady=20, columnspan=2, sticky="")
        
        # Create the label to display the invalid entries count
        self.detect_files_text = customtkinter.CTkLabel(
            master=self.detect_files_frame,
            text="Cannot Locate The Files ",
            text_color="#f04141",
            font=("Arial", 16, "bold"),  # Adjust font size and family as needed
            image=self.attention_icon,
            compound="right",
        )
        self.detect_files_text.pack(padx=10, pady=10)

    """
        //////////////////////////////
        /Other Functions Declarations/
        //////////////////////////////
                                        """

    def update_parameters(self, **kwargs):
        # Process and use the parameters as needed
        pass

    # def locate_files(self):
        
