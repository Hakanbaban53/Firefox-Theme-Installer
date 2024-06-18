import os
from re import compile
import platform

class VariableUpdater:
    def __init__(self, file_path):
        self.os_name = platform.system()
        self.file_path = self.normalize_path(file_path)
    
    def normalize_path(self, path):
        if self.os_name == "Windows":
            return path.replace("/", "\\")
        elif self.os_name in ["Linux", "Darwin"]:  # macOS
            return path.replace("\\", "/")
        else:
            raise ValueError(f"Unsupported OS: {self.os_name}")
    
    def read_file(self):
        with open(self.file_path, 'r') as file:
            return file.read()

    def write_file(self, content):
        with open(self.file_path, 'w') as file:
            file.write(content)

    def update_variable(self, variable_name, new_value):
        file_content = self.read_file()
        pattern = compile(rf'({variable_name}\s*:\s*)([^;]+)(;)')
        updated_file_content = pattern.sub(rf'\1{new_value}\3', file_content)
        self.write_file(updated_file_content)

# Example usage
# file_path = '..\RealFire-Installer\chrome\includes\\realfire-colours.css'
# variable = '--accent-color'
# new_value = '#ffff00'  # Replace with the desired new value. Color is yellow in this case.

# updater = VariableUpdater(file_path)
# updater.update_variable(variable, new_value)