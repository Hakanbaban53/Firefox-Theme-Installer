import os
from subprocess import run, CalledProcessError, PIPE
from functions.get_os_properties import OSProperties

class FileActions:
    def __init__(self, data_file_path):
        self.os_name = OSProperties(data_file_path).get_os()
        self.commands = []

    def move_file(self, source, destination):
        if not os.path.exists(source):
            # print(f"Source file does not exist: {source}")
            return
        command = ''
        if self.os_name.lower() == "windows":
            command = f'move "{source.replace("/", "\\")}" "{destination.replace("/", "\\")}"'
        elif self.os_name.lower() == "linux":
            command = f'cp "{source}" "{destination}"'
        elif self.os_name.lower() == "darwin":  # macOS
            command = f'mv "{source}" "{destination}"'
        else:
            return
        self.commands.append(command)

    def move_folder(self, source, destination):
        if not os.path.exists(source):
            # print(f"Source file does not exist: {source}")
            return

        command = ''
        if self.os_name.lower() == "windows":
            command = f'move "{source.replace("/", "\\")}" "{destination.replace("/", "\\")}"'
        elif self.os_name.lower() == "linux":
            command = f'cp -rf "{source}" "{destination}"'
        elif self.os_name.lower() == "darwin":  # macOS
            command = f'mv "{source}" "{destination}"'
        else:
            return
        self.commands.append(command)

    def move_existing_file(self, source, destination):
        if not os.path.exists(source):
            # print(f"Source file does not exist: {source}")
            return
        
        command = ''
        if self.os_name.lower() == "windows":
            command = f'move "{source.replace("/", "\\")}" "{destination.replace("/", "\\")}"'
        elif self.os_name.lower() == "linux":
            command = f'mv "{source}" "{destination}"'
        elif self.os_name.lower() == "darwin":  # macOS
            command = f'mv "{source}" "{destination}"'
        else:
            return

        self.commands.append(command)

    def remove_file(self, file_path):
        if not os.path.exists(file_path):
            return
        
        
        command = ''
        if self.os_name.lower() == "windows":
            command = f'del "{file_path.replace("/", "\\")}"'
        elif self.os_name.lower() == "linux":
            command = f'rm "{file_path}"'
        elif self.os_name.lower() == "darwin":  # macOS
            command = f'rm "{file_path}"'
        else:
            return
        self.commands.append(command)

    def remove_folder(self, folder_path):
        if not os.path.exists(folder_path):
            return
        
        command = ''
        if self.os_name.lower() == "windows":
            command = f'rd /s /q "{folder_path.replace("/", "\\")}"'
        elif self.os_name.lower() == "linux" or self.os_name.lower() == "darwin":  # macOS
            command = f'rm -rf "{folder_path}"'
        else:
            return
        self.commands.append(command)

    def execute_operations(self, progress_bar, output_entry):
        total_operations = len(self.commands)
        
        for i, command in enumerate(self.commands):
            try:
                result = run(command, shell=True, check=True, stdout=PIPE, stderr=PIPE)
                output = result.stdout.decode('utf-8').strip()
                error = result.stderr.decode('utf-8').strip()

                progress = (i + 1) / total_operations
                progress_bar.set(progress)

                output_entry.configure(state='normal')
                
                output_entry.insert("end", f"Completed: {command}\n")
                
                if output:
                    output_entry.insert("end", f"Output: {output}\n")
                if error:
                    output_entry.insert("end", f"Error: {error}\n")

            except CalledProcessError as e:
                output_entry.configure(state='normal')
                output_entry.insert("end", f"Failed: {command} with error {e.stderr.decode('utf-8').strip()}\n")
            except Exception as e:
                output_entry.configure(state='normal')
                output_entry.insert("end", f"Failed: {command} with error {e}\n")
            finally:
                output_entry.configure(state='disabled')
                output_entry.see("end")

                progress_bar.master.update_idletasks()

        self.commands.clear()
