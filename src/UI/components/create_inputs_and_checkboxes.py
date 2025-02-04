from os import path
from tkinter import BooleanVar
from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkCheckBox

from core.data_tools.load_json_data import LoadJsonData
from data.static.components.inputs_and_checkboxes.data import APPLICATION_FOLDER_ENTRY_DATA, APPLICATION_FOLDER_LABEL_DATA, CREATE_INPUT_AND_CHECKBOX_WIDGETS, CSL_CHECKBOX, INPUTS_CHECKBOXES_FRAME_DATA, PROFILE_FOLDER_ENTRY_DATA, PROFILE_FOLDER_LABEL_DATA
from data.static.global_data import APP_LANGUAGE, BASE_DIR


class InputsAndCheckboxes:
    def __init__(self, frame):
        self.frame = frame
        load_json_data = LoadJsonData()

        INPUTS_LABELS_DATA_PATH = path.join(
            BASE_DIR,
            "data",
            "language",
            "components",
            "inputs_and_checkboxes",
            f"{APP_LANGUAGE}.json",
        )
        self.inputs_labels_data = load_json_data.load_json_data(INPUTS_LABELS_DATA_PATH)
        self.create_inputs_and_checkboxes_frame()
        self.check_var = BooleanVar(value=False)
        self.CSL = BooleanVar(value=False)

    def create_inputs_and_checkboxes_frame(self):
        # Create the frame to hold widgets
        self.inputs_checkboxes_frame = CTkFrame(
            self.frame,
            width=INPUTS_CHECKBOXES_FRAME_DATA["width"],
            height=INPUTS_CHECKBOXES_FRAME_DATA["height"],
            corner_radius=INPUTS_CHECKBOXES_FRAME_DATA["corner_radius"],
            fg_color=INPUTS_CHECKBOXES_FRAME_DATA["fg_color"],
        )
        self.inputs_checkboxes_frame.grid(
            row=INPUTS_CHECKBOXES_FRAME_DATA["grid_data"]["row"],
            column=INPUTS_CHECKBOXES_FRAME_DATA["grid_data"]["column"],
            columnspan=INPUTS_CHECKBOXES_FRAME_DATA["grid_data"]["columnspan"],
            padx=INPUTS_CHECKBOXES_FRAME_DATA["grid_data"]["padx"],
            pady=INPUTS_CHECKBOXES_FRAME_DATA["grid_data"]["pady"],
            sticky=INPUTS_CHECKBOXES_FRAME_DATA["grid_data"]["sticky"],
        )

    def create_profile_folder_widget(self, profile_folder_location):

        # Profile Folder Label
        profile_folder_label = CTkLabel(
            master=self.inputs_checkboxes_frame,
            text=self.inputs_labels_data["profile_folder_label"],
            text_color=PROFILE_FOLDER_LABEL_DATA["text_color"],
            font=eval(PROFILE_FOLDER_LABEL_DATA["font"]),
        )
        profile_folder_label.grid(
            row=PROFILE_FOLDER_LABEL_DATA["grid_data"]["row"],
            column=PROFILE_FOLDER_LABEL_DATA["grid_data"]["column"],
            padx=PROFILE_FOLDER_LABEL_DATA["grid_data"]["padx"],
            pady=PROFILE_FOLDER_LABEL_DATA["grid_data"]["pady"],
            sticky=PROFILE_FOLDER_LABEL_DATA["grid_data"]["sticky"],
        )

        # Profile Folder Entry
        self.profile_folder_entry = CTkEntry(
            master=self.inputs_checkboxes_frame,
            width=PROFILE_FOLDER_ENTRY_DATA["width"],
            height=PROFILE_FOLDER_ENTRY_DATA["height"],
            fg_color=PROFILE_FOLDER_ENTRY_DATA["fg_color"],
            text_color=PROFILE_FOLDER_ENTRY_DATA["text_color"],
            corner_radius=PROFILE_FOLDER_ENTRY_DATA["corner_radius"],
            border_width=PROFILE_FOLDER_ENTRY_DATA["border_width"],
            bg_color=PROFILE_FOLDER_ENTRY_DATA["bg_color"],
            border_color=PROFILE_FOLDER_ENTRY_DATA["border_color"],
            placeholder_text=profile_folder_location,
        )
        self.profile_folder_entry.grid(
            row=PROFILE_FOLDER_ENTRY_DATA["grid_data"]["row"],
            column=PROFILE_FOLDER_ENTRY_DATA["grid_data"]["column"],
            padx=PROFILE_FOLDER_ENTRY_DATA["grid_data"]["padx"],
            pady=PROFILE_FOLDER_ENTRY_DATA["grid_data"]["pady"],
            sticky=PROFILE_FOLDER_ENTRY_DATA["grid_data"]["sticky"],
        )

        return self.profile_folder_entry

    def create_application_folder_widget(self, application_folder):

        # Application Folder Label
        application_folder_label = CTkLabel(
            master=self.inputs_checkboxes_frame,
            text=self.inputs_labels_data["application_folder_label"],
            text_color=APPLICATION_FOLDER_LABEL_DATA["text_color"],
            font=eval(APPLICATION_FOLDER_LABEL_DATA["font"]),
        )
        application_folder_label.grid(
            row=APPLICATION_FOLDER_LABEL_DATA["grid_data"]["row"],
            column=APPLICATION_FOLDER_LABEL_DATA["grid_data"]["column"],
            padx=APPLICATION_FOLDER_LABEL_DATA["grid_data"]["padx"],
            pady=APPLICATION_FOLDER_LABEL_DATA["grid_data"]["pady"],
            sticky=APPLICATION_FOLDER_LABEL_DATA["grid_data"]["sticky"],
        )

        # Application Folder Entry
        self.application_folder_entry = CTkEntry(
            master=self.inputs_checkboxes_frame,
            width=APPLICATION_FOLDER_ENTRY_DATA["width"],
            height=APPLICATION_FOLDER_ENTRY_DATA["height"],
            fg_color=APPLICATION_FOLDER_ENTRY_DATA["fg_color"],
            text_color=APPLICATION_FOLDER_ENTRY_DATA["text_color"],
            corner_radius=APPLICATION_FOLDER_ENTRY_DATA["corner_radius"],
            border_width=APPLICATION_FOLDER_ENTRY_DATA["border_width"],
            bg_color=APPLICATION_FOLDER_ENTRY_DATA["bg_color"],
            border_color=APPLICATION_FOLDER_ENTRY_DATA["border_color"],
            placeholder_text=application_folder,
        )
        self.application_folder_entry.grid(
            row=APPLICATION_FOLDER_ENTRY_DATA["grid_data"]["row"],
            column=APPLICATION_FOLDER_ENTRY_DATA["grid_data"]["column"],
            padx=APPLICATION_FOLDER_ENTRY_DATA["grid_data"]["padx"],
            pady=APPLICATION_FOLDER_ENTRY_DATA["grid_data"]["pady"],
            sticky=APPLICATION_FOLDER_ENTRY_DATA["grid_data"]["sticky"],
        )

        return self.application_folder_entry

    def create_CSL_checkbox(self):

        CSL_checkbox = CTkCheckBox(
            master=self.inputs_checkboxes_frame,
            text=self.inputs_labels_data["CSL_checkbox"],
            fg_color=CSL_CHECKBOX["fg_color"],
            hover_color=CSL_CHECKBOX["hover_color"],
            text_color=CSL_CHECKBOX["text_color"],
            bg_color=CSL_CHECKBOX["bg_color"],
            font=eval(CSL_CHECKBOX["font"]),
            border_color=CSL_CHECKBOX["border_color"],
            variable=self.CSL,
            onvalue=True,
            offvalue=False,
        )
        CSL_checkbox.grid(
            row=CSL_CHECKBOX["grid_data"]["row"],
            column=CSL_CHECKBOX["grid_data"]["column"],
            padx=CSL_CHECKBOX["grid_data"]["padx"],
            pady=CSL_CHECKBOX["grid_data"]["pady"],
            sticky=CSL_CHECKBOX["grid_data"]["sticky"],
        )

        return self.CSL

    def create_edit_checkbox(self, command):

        edit_checkbox = CTkCheckBox(
            master=self.inputs_checkboxes_frame,
            text=self.inputs_labels_data["edit_checkbox"],
            fg_color=CREATE_INPUT_AND_CHECKBOX_WIDGETS["fg_color"],
            hover_color=CREATE_INPUT_AND_CHECKBOX_WIDGETS["hover_color"],
            text_color=CREATE_INPUT_AND_CHECKBOX_WIDGETS["text_color"],
            bg_color=CREATE_INPUT_AND_CHECKBOX_WIDGETS["bg_color"],
            font=eval(CREATE_INPUT_AND_CHECKBOX_WIDGETS["font"]),
            border_color=CREATE_INPUT_AND_CHECKBOX_WIDGETS["border_color"],
            command=command,
            variable=self.check_var,
            onvalue=True,
            offvalue=False,
        )
        edit_checkbox.grid(
            row=CREATE_INPUT_AND_CHECKBOX_WIDGETS["grid_data"]["row"],
            column=CREATE_INPUT_AND_CHECKBOX_WIDGETS["grid_data"]["column"],
            padx=CREATE_INPUT_AND_CHECKBOX_WIDGETS["grid_data"]["padx"],
            pady=CREATE_INPUT_AND_CHECKBOX_WIDGETS["grid_data"]["pady"],
            sticky=CREATE_INPUT_AND_CHECKBOX_WIDGETS["grid_data"]["sticky"],
        )

        return self.check_var
