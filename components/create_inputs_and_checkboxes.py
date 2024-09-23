from os import path
from tkinter import BooleanVar
from installer_core.data_tools.load_json_data import LoadJsonData
from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkCheckBox


class InputsAndCheckboxes:
    def __init__(self, base_dir, app_language, frame):
        self.frame = frame
        load_json_data = LoadJsonData()
        INPUTS_DATA_PATH = path.join(
            base_dir,
            "data",
            "components",
            "inputs_and_checkboxes",
            "data",
            "inputs_data.json",
        )
        self.inputs_data = load_json_data.load_json_data(INPUTS_DATA_PATH)

        INPUTS_LABELS_DATA_PATH = path.join(
            base_dir,
            "data",
            "components",
            "inputs_and_checkboxes",
            "language",
            f"{app_language}.json",
        )
        self.inputs_labels_data = load_json_data.load_json_data(INPUTS_LABELS_DATA_PATH)
        self.create_inputs_and_checkboxes_frame()
        self.check_var = BooleanVar(value=False)
        self.CSL = BooleanVar(value=False)

    def create_inputs_and_checkboxes_frame(self):
        # Create the frame to hold widgets
        inputs_data = self.inputs_data["create_inputs_and_checkboxes"]
        self.inputs_checkboxes_frame = CTkFrame(
            self.frame,
            width=inputs_data["inputs_checkboxes_frame"]["width"],
            height=inputs_data["inputs_checkboxes_frame"]["height"],
            corner_radius=inputs_data["inputs_checkboxes_frame"]["corner_radius"],
            fg_color=inputs_data["inputs_checkboxes_frame"]["fg_color"],
        )
        self.inputs_checkboxes_frame.grid(
            row=inputs_data["inputs_checkboxes_frame"]["grid_data"]["row"],
            column=inputs_data["inputs_checkboxes_frame"]["grid_data"]["column"],
            columnspan=inputs_data["inputs_checkboxes_frame"]["grid_data"]["columnspan"],
            padx=inputs_data["inputs_checkboxes_frame"]["grid_data"]["padx"],
            pady=inputs_data["inputs_checkboxes_frame"]["grid_data"]["pady"],
            sticky=inputs_data["inputs_checkboxes_frame"]["grid_data"]["sticky"],
        )

    def create_profile_folder_widget(self, profile_folder_location):
        inputs_data = self.inputs_data["create_inputs_and_checkboxes"]["create_input_and_checkbox_widgets"]

        # Profile Folder Label
        profile_folder_label = CTkLabel(
            master=self.inputs_checkboxes_frame,
            text=self.inputs_labels_data["profile_folder_label"],
            text_color=inputs_data["profile_folder_label"]["text_color"],
            font=eval(inputs_data["profile_folder_label"]["font"]),
        )
        profile_folder_label.grid(
            row=inputs_data["profile_folder_label"]["grid_data"]["row"],
            column=inputs_data["profile_folder_label"]["grid_data"]["column"],
            padx=inputs_data["profile_folder_label"]["grid_data"]["padx"],
            pady=inputs_data["profile_folder_label"]["grid_data"]["pady"],
            sticky=inputs_data["profile_folder_label"]["grid_data"]["sticky"],
        )

        # Profile Folder Entry
        self.profile_folder_entry = CTkEntry(
            master=self.inputs_checkboxes_frame,
            width=inputs_data["profile_folder_entry"]["width"],
            height=inputs_data["profile_folder_entry"]["height"],
            fg_color=inputs_data["profile_folder_entry"]["fg_color"],
            text_color=inputs_data["profile_folder_entry"]["text_color"],
            corner_radius=inputs_data["profile_folder_entry"]["corner_radius"],
            border_width=inputs_data["profile_folder_entry"]["border_width"],
            bg_color=inputs_data["profile_folder_entry"]["bg_color"],
            border_color=inputs_data["profile_folder_entry"]["border_color"],
            placeholder_text=profile_folder_location,
        )
        self.profile_folder_entry.grid(
            row=inputs_data["profile_folder_entry"]["grid_data"]["row"],
            column=inputs_data["profile_folder_entry"]["grid_data"]["column"],
            padx=inputs_data["profile_folder_entry"]["grid_data"]["padx"],
            pady=inputs_data["profile_folder_entry"]["grid_data"]["pady"],
            sticky=inputs_data["profile_folder_entry"]["grid_data"]["sticky"],
        )

        return self.profile_folder_entry

    def create_application_folder_widget(self, application_folder):
        inputs_data = self.inputs_data["create_inputs_and_checkboxes"]["create_input_and_checkbox_widgets"]

        # Application Folder Label
        application_folder_label = CTkLabel(
            master=self.inputs_checkboxes_frame,
            text=self.inputs_labels_data["application_folder_label"],
            text_color=inputs_data["application_folder_label"]["text_color"],
            font=eval(inputs_data["application_folder_label"]["font"]),
        )
        application_folder_label.grid(
            row=inputs_data["application_folder_label"]["grid_data"]["row"],
            column=inputs_data["application_folder_label"]["grid_data"]["column"],
            padx=inputs_data["application_folder_label"]["grid_data"]["padx"],
            pady=inputs_data["application_folder_label"]["grid_data"]["pady"],
            sticky=inputs_data["application_folder_label"]["grid_data"]["sticky"],
        )

        # Application Folder Entry
        self.application_folder_entry = CTkEntry(
            master=self.inputs_checkboxes_frame,
            width=inputs_data["application_folder_entry"]["width"],
            height=inputs_data["application_folder_entry"]["height"],
            fg_color=inputs_data["application_folder_entry"]["fg_color"],
            text_color=inputs_data["application_folder_entry"]["text_color"],
            corner_radius=inputs_data["application_folder_entry"]["corner_radius"],
            border_width=inputs_data["application_folder_entry"]["border_width"],
            bg_color=inputs_data["application_folder_entry"]["bg_color"],
            border_color=inputs_data["application_folder_entry"]["border_color"],
            placeholder_text=application_folder,
        )
        self.application_folder_entry.grid(
            row=inputs_data["application_folder_entry"]["grid_data"]["row"],
            column=inputs_data["application_folder_entry"]["grid_data"]["column"],
            padx=inputs_data["application_folder_entry"]["grid_data"]["padx"],
            pady=inputs_data["application_folder_entry"]["grid_data"]["pady"],
            sticky=inputs_data["application_folder_entry"]["grid_data"]["sticky"],
        )

        return self.application_folder_entry

    def create_CSL_checkbox(self):
        inputs_data = self.inputs_data["create_inputs_and_checkboxes"]["create_input_and_checkbox_widgets"]

        CSL_checkbox = CTkCheckBox(
            master=self.inputs_checkboxes_frame,
            text=self.inputs_labels_data["CSL_checkbox"],
            fg_color=inputs_data["CSL_checkbox"]["fg_color"],
            hover_color=inputs_data["CSL_checkbox"]["hover_color"],
            text_color=inputs_data["CSL_checkbox"]["text_color"],
            bg_color=inputs_data["CSL_checkbox"]["bg_color"],
            font=eval(inputs_data["CSL_checkbox"]["font"]),
            border_color=inputs_data["CSL_checkbox"]["border_color"],
            variable=self.CSL,
            onvalue=True,
            offvalue=False,
        )
        CSL_checkbox.grid(
            row=inputs_data["CSL_checkbox"]["grid_data"]["row"],
            column=inputs_data["CSL_checkbox"]["grid_data"]["column"],
            padx=inputs_data["CSL_checkbox"]["grid_data"]["padx"],
            pady=inputs_data["CSL_checkbox"]["grid_data"]["pady"],
            sticky=inputs_data["CSL_checkbox"]["grid_data"]["sticky"],
        )

        return self.CSL

    def create_edit_checkbox(self, command):
        inputs_data = self.inputs_data["create_inputs_and_checkboxes"]["create_input_and_checkbox_widgets"]

        edit_checkbox = CTkCheckBox(
            master=self.inputs_checkboxes_frame,
            text=self.inputs_labels_data["edit_checkbox"],
            fg_color=inputs_data["edit_checkbox"]["fg_color"],
            hover_color=inputs_data["edit_checkbox"]["hover_color"],
            text_color=inputs_data["edit_checkbox"]["text_color"],
            bg_color=inputs_data["edit_checkbox"]["bg_color"],
            font=eval(inputs_data["edit_checkbox"]["font"]),
            border_color=inputs_data["edit_checkbox"]["border_color"],
            command=command,
            variable=self.check_var,
            onvalue=True,
            offvalue=False,
        )
        edit_checkbox.grid(
            row=inputs_data["edit_checkbox"]["grid_data"]["row"],
            column=inputs_data["edit_checkbox"]["grid_data"]["column"],
            padx=inputs_data["edit_checkbox"]["grid_data"]["padx"],
            pady=inputs_data["edit_checkbox"]["grid_data"]["pady"],
            sticky=inputs_data["edit_checkbox"]["grid_data"]["sticky"],
        )

        return self.check_var
