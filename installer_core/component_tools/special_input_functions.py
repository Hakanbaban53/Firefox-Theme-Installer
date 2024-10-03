from os import path

class SpecialInputFunc:
    invalid_entries = []

    def validate_file_location(self, entry_widget, file_extension=None):
        location = entry_widget.get()

        if (path.exists(location) or location == "") and file_extension == None:
            entry_widget.configure(border_color="#10dc60")
            # Remove entry from invalid_entries if it exists
            if entry_widget in self.invalid_entries:
                self.invalid_entries.remove(entry_widget)
        elif (
            path.isfile(location)
            and location.lower().endswith(tuple(file_extension))
            or location == ""
        ):
            entry_widget.configure(border_color="#10dc60")
            # Remove entry from invalid_entries if it exists
            if entry_widget in self.invalid_entries:
                self.invalid_entries.remove(entry_widget)
        else:
            entry_widget.configure(border_color="#f04141")
            # Add entry to invalid_entries if it's not already in the list
            if entry_widget not in self.invalid_entries:
                self.invalid_entries.append(entry_widget)

    def return_invalid_entries(self):
        return self.invalid_entries

    def update_invalid_entries_display(self):
        if len(self.invalid_entries) == 0:
            return True
        else:
            return False

    def get_variables(self, entry):
        input_value = entry.get()
        placeholder_text = entry.cget("placeholder_text")
        if input_value:
            return input_value
        else:
            return placeholder_text
