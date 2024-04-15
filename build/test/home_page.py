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


class home_page(customtkinter.CTkFrame):
    def __init__(self, parent, controller, os_properties):
        customtkinter.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.os_properties = os_properties

        os_name = self.os_properties.get_os()

        text_color = self.os_properties.get_os_color()

        os_icon_path = self.os_properties.os_icon()

        self.button_font = customtkinter.CTkFont(family="Inter", size=20)

        home_page_frame = customtkinter.CTkFrame(
            self,
            fg_color="#2B2631",
            # border_width=4,
            # bg_color="#2B2631",
            # border_color="#F89F24",
        )
        home_page_frame.place(x=311.0, y=0.0)
        home_page_frame.columnconfigure(0, weight=1)

        self.header_title_background = customtkinter.CTkImage(
            light_image=Image.open(
                "/home/hakan/Documents/GitHub/pythonInstaller/build/assets/backgrounds/header_title_background.png"
            ),
            dark_image=Image.open(
                "/home/hakan/Documents/GitHub/pythonInstaller/build/assets/backgrounds/header_title_background.png"
            ),
            size=(390, 64),
        )
        self.header_title_background_label = customtkinter.CTkLabel(
            master=home_page_frame,
            text="Welcome the RealFire Installer",
            image=self.header_title_background,
            text_color="White",
            font=customtkinter.CTkFont(family="Inter", size=24, weight="bold"),
            bg_color="#2B2631",
        )
        self.header_title_background_label.grid(
            row=0, column=0, columnspan=2, padx=203, pady=(75,0), sticky="NSEW"
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
            master=home_page_frame,
            text="",
            image=self.line_top_image,
        )
        self.line_top_image_label.grid(row=1, column=0, columnspan=2, padx=10, pady=(20,30), sticky="NSEW")

        # Operation System
        operation_system = customtkinter.CTkLabel(
            master=home_page_frame,
            text="Detected Operation System",
            text_color="White",
            bg_color="#2B2631",
            font=customtkinter.CTkFont(family="Inter", size=20, weight="bold"),
        )
        operation_system.grid(row=2, column=0, columnspan=1, padx=(175,0), sticky="ew")

        os_frame = customtkinter.CTkFrame(
            master=home_page_frame,
            # width=440,  # Adjust initial width as needed
            # height=54,
            corner_radius=12,
            bg_color="#2B2631",
            fg_color="white",
        )
        os_frame.grid(row=2, column=1, columnspan=1, padx=(0,175), sticky="ew")

        os_label = customtkinter.CTkLabel(
            master=os_frame,
            text=os_name,  # Initial text (can be empty)
            text_color=text_color,
            font=("Arial", 20, "bold"),  # Adjust font size and family as needed
        )

        os_label.pack(
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

        self.select_action_image = customtkinter.CTkImage(
            light_image=Image.open(
                "/home/hakan/Documents/GitHub/pythonInstaller/build/assets/backgrounds/header_title_background.png"
            ),
            dark_image=Image.open(
                "/home/hakan/Documents/GitHub/pythonInstaller/build/assets/backgrounds/header_title_background.png"
            ),
            size=(270, 36),
        )
        self.select_action_label = customtkinter.CTkLabel(
            master=home_page_frame,
            text="Please Select the Action",
            image=self.select_action_image,
            text_color="White",
            font=customtkinter.CTkFont(family="Inter", size=20, weight="bold"),
            bg_color="#2B2631",
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
            bg_color="#2B2631",
            fg_color="white",
            border_color="#F89F24",
        )

        navigation_frame.grid(row=4, column=0, columnspan=2, sticky="")

        image_path = relative_to_assets(
            "icons/remove_icon.png"
        )  # Get the absolute path
        image = Image.open(image_path)
        self.remove_button_image = customtkinter.CTkImage(
            dark_image=image, light_image=image, size=(20, 24)
        )

        remove_button = customtkinter.CTkButton(
            master=navigation_frame,
            text="Remove",
            fg_color="#D9D9D9",
            hover_color="#EEEEEE",
            bg_color="white",
            corner_radius=12,
            command=lambda: controller.show_frame(
                "remove_page", param1=os_name, param2=text_color, param3=os_icon_path
            ),
            width=122.0,
            height=38.0,
            image=self.remove_button_image,
            compound="right",
            text_color="#000000",
            font=self.button_font,
        )

        remove_button.pack(padx=(5, 20), pady=10, side="right")

        image_path = relative_to_assets(
            "icons/install_icon.png"
        )  # Get the absolute path
        image = Image.open(image_path)
        self.install_button_image = customtkinter.CTkImage(
            dark_image=image, light_image=image, size=(20, 20)
        )

        install_button = customtkinter.CTkButton(
            master=navigation_frame,
            text="Install",
            fg_color="#D9D9D9",
            hover_color="#EEEEEE",
            bg_color="white",
            corner_radius=12,
            command=lambda: controller.show_frame(
                "install_page", param1=os_name, param2=text_color, param3=os_icon_path
            ),
            width=122.0,
            height=38.0,
            image=self.install_button_image,
            text_color="#000000",
            font=self.button_font,
        )

        install_button.pack(padx=5, pady=10, side="right")

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


    def exit_confirmation(self):
        CombinedModal(self, "Exit Confirmation", "Are you sure you want to exit?")

    def update_parameters(self, **kwargs):
        # Process and use the parameters as needed
        pass
