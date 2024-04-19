import os
import customtkinter
from PIL import Image


class CustomWidgetManager:
    def __init__(self):
        self.invalid_entries = []

    def create_invalid_entry_frame(
        self,
        frame_master,
        frame_corner_radius,
        frame_fg_color,
        frame_row,
        frame_column,
        frame_columnspan,
        frame_padx,
        frame_pady,
    ):
        invalid_entry_frame = customtkinter.CTkFrame(
            master=frame_master,
            corner_radius=frame_corner_radius,
            fg_color=frame_fg_color,
        )
        invalid_entry_frame.grid(
            row=frame_row,
            column=frame_column,
            columnspan=frame_columnspan,
            padx=frame_padx,
            pady=frame_pady,
        )
        return invalid_entry_frame

    def create_invalid_entries_text(self):
        attention_icon = customtkinter.CTkImage(
            light_image=Image.open("assets/icons/attention.png"),
            dark_image=Image.open("assets/icons/attention.png"),
            size=(24, 24),
        )
        invalid_entries_text = customtkinter.CTkLabel(
            master=self.invalid_entry_frame,
            text="  0 entries is invalid",
            text_color="#f04141",
            font=("Arial", 16, "bold"),  # Adjust font size and family as needed
            image=attention_icon,
            compound="left",
        )
        invalid_entries_text.pack(padx=10, pady=10)
        return invalid_entries_text

    def custom_label(
        self,
        master_frame,
        label_text,
        label_text_color,
        label_image,
        label_font,
        label_row,
        label_column,
        label_columnspan,
        label_padx=0,
        label_pady=0,
        label_sticky="",
    ):
        label_config = {
            "text": label_text,
            "text_color": label_text_color,
            "image": label_image,
            "font": label_font,
        }
        label_widget = customtkinter.CTkLabel(master=master_frame, **label_config)
        label_widget.grid(
            row=label_row,
            column=label_column,
            columnspan=label_columnspan,
            padx=label_padx,
            pady=label_pady,
            sticky=label_sticky,
        )
        return label_widget

    def custom_entry(
        self,
        master_frame,
        entry_placeholder_text,
        file,
        grid_row,
        grid_column,
        grid_padx=0,
        grid_pady=0,
        grid_sticky="",
    ):
        entry_config = {
            "width": 342,
            "height": 38,
            "fg_color": "white",
            "text_color": "black",
            "corner_radius": 8,
            "border_width": 3,
            "bg_color": "#2B2631",
            "border_color": "purple",
            "placeholder_text": entry_placeholder_text,
        }

        entry_widget = customtkinter.CTkEntry(master=master_frame, **entry_config)
        entry_widget.grid(
            row=grid_row,
            column=grid_column,
            padx=grid_padx,
            pady=grid_pady,
            sticky=grid_sticky,
        )

        if file:  # Only bind events if the file parameter is provided
            entry_widget.bind(
                "<FocusOut>", lambda event: self.validate_location(entry_widget, ".png")
            )
            entry_widget.bind(
                "<Return>", lambda event: self.validate_location(entry_widget, ".png")
            )
        else:
            entry_widget.bind(
                "<FocusOut>", lambda event: self.validate_location(entry_widget, None)
            )
            entry_widget.bind(
                "<Return>", lambda event: self.validate_location(entry_widget, None)
            )

        return entry_widget

    def validate_location(self, entry_widget, file_extension=None):
        location = entry_widget.get()

        if (os.path.exists(location) or location == "") and file_extension == None:
            entry_widget.configure(border_color="#10dc60")
            # Remove entry from invalid_entries if it exists
            if entry_widget in self.invalid_entries:
                self.invalid_entries.remove(entry_widget)
        elif (
            os.path.isfile(location)
            and location.lower().endswith(".png")
            or location == ""
        ) and file_extension == ".png":
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
            # Hide the invalid entry frame if there are no invalid entries
            self.invalid_entry_frame.grid_remove()
        else:
            # Show the invalid entry frame and update the text with the count of invalid entries
            self.invalid_entries_text.configure(
                text=f"  {len(self.invalid_entries)} entries is invalid"
            )
            self.invalid_entry_frame.grid()
