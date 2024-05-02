import json
import customtkinter
from PIL import Image
from functions.combined_modal import CombinedModal
from pages.home_page import home_page
from pages.install_page import install_page
from pages.remove_page import remove_page
from pages.status_page import status_page


class MultiPageApp(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        customtkinter.CTk.__init__(self, *args, **kwargs)

        with open("../RealFire_Installer/data/installer_data.json", "r") as file:
            self.text_data = json.load(file)

        self.title(self.text_data["common_values"]["installer_info"]["installer_title"])
        self.geometry("1115x666")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.exit_confirmation)

        # Create the image label to be displayed across all pages
        self.installer_img = customtkinter.CTkImage(
            light_image=Image.open(
                "../RealFire_Installer/assets/backgrounds/installer_img.png"
            ),
            dark_image=Image.open(
                "../RealFire_Installer/assets/backgrounds/installer_img.png"
            ),
            size=(315, 666),
        )
        self.installer_img_label = customtkinter.CTkLabel(
            self,
            text=self.text_data["common_values"]["installer_info"]["installer_version"],
            text_color="white",
            image=self.installer_img,
            font=customtkinter.CTkFont(family="Inter", size=14),
        )
        self.installer_img_label.place(x=0, y=0)  # Place image label at (0, 0)

        self.container = customtkinter.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

    def create_frame(self, page_class):
        frame = page_class(self.container, self)
        frame.configure(
            fg_color="#2B2631",
            corner_radius=0,
        )

        frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        return frame

    def slide_to_frame(self, current_frame, next_frame, x, speed=35, direction=None):
        # Determine direction if not provided
        if direction is None:
            current_index = list(self.frames.values()).index(current_frame)
            next_index = list(self.frames.values()).index(next_frame)
            direction = "left" if current_index > next_index else "right"

        # Calculate x-coordinate based on direction
        if direction == "right":
            next_x = self.winfo_width() - x
            current_x = - x + 315
        else:
            next_x = x - self.winfo_width() + 625 # Adjusted calculation for moving back to previous page
            current_x = x + 2*315

        # Move frames to desired positions
        next_frame.place(x=next_x, y=0, relwidth=1, relheight=1)
        current_frame.place(x=current_x, y=0, relwidth=1, relheight=1)

        # Raise next_frame to the top
        next_frame.lift()

        # Update the tkinter window
        self.update()

        # Check if animation is complete
        if direction == "left" and x <= self.winfo_width() - 315:
            # Continue animation
            self.after(1, self.slide_to_frame, current_frame, next_frame, x + speed, speed, direction)
        elif direction == "right" and x <= self.winfo_width() - 315:
            # Continue animation
            self.after(1, self.slide_to_frame, current_frame, next_frame, x + speed, speed, direction)
        else:
            # Hide the current frame after transition
            current_frame.place_forget()


    def show_frame(self, page_name, **kwargs):
        self.installer_img_label.lift()
        
        page_class = {
            "home_page": home_page,
            "install_page": install_page,
            "remove_page": remove_page,
            "status_page": status_page,
        }.get(page_name) 

        if page_class:
            if page_class not in self.frames:
                self.frames[page_class] = self.create_frame(page_class)

            current_frame = None
            for frame in self.frames.values():
                if frame.winfo_ismapped():
                    current_frame = frame
                    break

            next_frame = self.frames[page_class]
            if current_frame is not None:
                self.slide_to_frame(current_frame, next_frame, 0)
            else:
                next_frame.place(x=315, y=0, relwidth=1, relheight=1)

            next_frame.update_parameters(**kwargs)
            next_frame.tkraise()

    def exit_confirmation(self):
        CombinedModal(self, "Exit")


if __name__ == "__main__":
    app = MultiPageApp()
    app.show_frame("home_page")
    app.mainloop()




# import os
# import subprocess
# import sys

# def run_as_admin():
#     # Use pkexec to execute a command with administrative privileges
#     cmd = "pkexec " + " ".join(sys.argv)
#     subprocess.call(cmd, shell=True)

# run_as_admin()
