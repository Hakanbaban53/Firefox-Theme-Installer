import os
from subprocess import run, CalledProcessError, PIPE

class FileActions:
    def __init__(self, os_name):
        self.os_name = os_name
        self.commands = []

    def elevate_windows_command(self, batched_commands):
        # Batch all commands into a single string
        batched_command_str = " & ".join(batched_commands)
        return f'powershell -Command "Start-Process cmd -ArgumentList \'/c {batched_command_str}\' -Verb RunAs"'

    def elevate_linux_command(self, batched_commands):
        # Batch all commands into a single string for Linux/macOS
        batched_command_str = " && ".join(batched_commands)
        return f'pkexec bash -c "{batched_command_str}"'

    def copy_file(self, source, destination):
        if not os.path.exists(source):
            print(f"Source file does not exist: {source}")
            return
        print(f"Copying {source} to {destination}")

        if self.os_name.lower() in ["linux", "darwin"]:
            command = f'cp "{source}" "{destination}"'
        elif self.os_name.lower() == "windows":
            command = f'copy "{source.replace("/", "\\")}" "{destination.replace("/", "\\")}"'
        
        self.commands.append(command)

    def move_file(self, source, destination):
        if not os.path.exists(source):
            print(f"Source file does not exist: {source}")
            return

        if self.os_name.lower() in ["linux", "darwin"]:
            command = f'mv "{source}" "{destination}"'
        elif self.os_name.lower() == "windows":
            command = f'move "{source.replace("/", "\\")}" "{destination.replace("/", "\\")}"'
        
        self.commands.append(command)

    def copy_folder(self, source, destination):
        if not os.path.exists(source):
            print(f"Source folder does not exist: {source}")
            return

        if self.os_name.lower() in ["linux", "darwin"]:
            command = f'cp -rf "{source}" "{destination}"'
        elif self.os_name.lower() == "windows":
            command = f'xcopy /e /i "{source.replace("/", "\\")}" "{destination.replace("/", "\\")}"'
        
        self.commands.append(command)

    def move_folder(self, source, destination):
        if not os.path.exists(source):
            print(f"Source folder does not exist: {source}")
            return

        if self.os_name.lower() in ["linux", "darwin"]:
            command = f'mv "{source}" "{destination}"'
        elif self.os_name.lower() == "windows":
            command = f'move "{source.replace("/", "\\")}" "{destination.replace("/", "\\")}"'
        
        self.commands.append(command)

    def remove_file(self, file_path):
        if not os.path.exists(file_path):
            print(f"File does not exist: {file_path}")
            return
        print(f"Removing {file_path}")
        
        if self.os_name.lower() in ["linux", "darwin"]:
            command = f'rm "{file_path}"'
        elif self.os_name.lower() == "windows":
            command = f'del "{file_path.replace("/", "\\")}"'
        
        self.commands.append(command)

    def remove_folder(self, folder_path):
        if not os.path.exists(folder_path):
            print(f"Folder does not exist: {folder_path}")
            return

        if self.os_name.lower() in ["linux", "darwin"]:
            command = f'rm -rf "{folder_path}"'
        elif self.os_name.lower() == "windows":
            command = f'rd /s /q "{folder_path.replace("/", "\\")}"'
        
        self.commands.append(command)

    def execute_operations(self, progress_bar, output_entry=None):
        total_operations = len(self.commands)
        if total_operations == 0:
            return

        if output_entry:
            output_entry.configure(state='normal')

        if self.os_name.lower() == "windows":
            batched_command = self.elevate_windows_command(self.commands)
            commands_to_execute = [batched_command]
        elif self.os_name.lower() in ["linux", "darwin"]:
            batched_command = self.elevate_linux_command(self.commands)
            commands_to_execute = [batched_command]
        else:
            commands_to_execute = self.commands

        for i, command in enumerate(commands_to_execute):
            try:
                result = run(command, shell=True, check=True, stdout=PIPE, stderr=PIPE)
                output = result.stdout.decode('utf-8').strip()
                error = result.stderr.decode('utf-8').strip()

                if output_entry:
                    output_entry.insert("end", f"Completed: {command}\n")
                
                if output and output_entry:
                    output_entry.insert("end", f"Output: {output}\n")
                if error and output_entry:
                    output_entry.insert("end", f"Error: {error}\n")

            except CalledProcessError as e:
                if output_entry:
                    output_entry.insert("end", f"Failed: {command} with error {e.stderr.decode('utf-8').strip()}\n")
            except Exception as e:
                if output_entry:
                    output_entry.insert("end", f"Failed: {command} with error {e}\n")

            progress = (i + 1) / total_operations
            if progress_bar:
                progress_bar.set(progress)
                progress_bar.master.update_idletasks()

        if output_entry:
            output_entry.configure(state='disabled')
        self.commands.clear()
