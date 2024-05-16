from subprocess import run
from functions.get_os_properties import OSProperties

class FileActions:
    def __init__(self):
        self.os_name = OSProperties().get_os()
        self.commands = []

    def move_file(self, source, destination):
        if self.os_name == "Windows":
            self.commands.append(f'move "{source}" "{destination}"')
        elif self.os_name == "Linux":
            self.commands.append(f'cp "{source}" "{destination}"')
        elif self.os_name == "Darwin":  # macOS
            self.commands.append(f'mv "{source}" "{destination}"')
        else:
            print("Unsupported operating system.")

    def move_folder(self, source, destination):
        if self.os_name == "Windows":
            self.commands.append(f'move "{source}" "{destination}"')
        elif self.os_name == "Linux":
            self.commands.append(f'cp -rf "{source}" "{destination}"')
        elif self.os_name == "Darwin":  # macOS
            self.commands.append(f'mv "{source}" "{destination}"')
        else:
            print("Unsupported operating system.")

    def remove_file(self, file_path):
        if self.os_name == "Windows":
            self.commands.append(f'del "{file_path}"')
        elif self.os_name == "Linux":
            self.commands.append(f'rm "{file_path}"')
        elif self.os_name == "Darwin":  # macOS
            self.commands.append(f'rm "{file_path}"')
        else:
            print("Unsupported operating system.")

    def remove_folder(self, folder_path):
        if self.os_name == "Windows":
            self.commands.append(f'rd /s /q "{folder_path}"')
        elif self.os_name == "Linux" or self.os_name == "Darwin":  # macOS
            self.commands.append(f'rm -rf "{folder_path}"')
        else:
            print("Unsupported operating system.")

    def execute_operations(self, progress_bar, output_entry):
        total_operations = len(self.commands)
        for i, command in enumerate(self.commands):
            try:
                run(command, shell=True, check=True)

                # Update progress bar and output entry after each operation
                progress = (i + 1) / total_operations
                progress_bar.set(progress)
                output_entry.insert("end", f"Completed: {command}\n")
            except Exception as e:
                output_entry.insert("end", f"Failed: {command} with error {e}\n")
            finally:
                # Ensure the UI is updated
                progress_bar.master.update_idletasks()

        # Clear the commands list after all commands have been executed
        self.commands.clear()




