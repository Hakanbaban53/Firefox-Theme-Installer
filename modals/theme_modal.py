from os import path
from tkinter import ttk, Toplevel, DISABLED, LEFT, END, NORMAL, BOTH
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry

from components.set_window_icon import SetWindowIcon
from installer_core.component_tools.thread_manager import ThreadManager
from installer_core.data_tools.get_theme_data import ThemeManager
from installer_core.data_tools.load_json_data import LoadJsonData
from installer_core.window_tools.center_window import CenterWindow
from modals.theme_detail_modal import ThemeDetailModal


class ThemeModal(Toplevel):
    def __init__(self, parent, base_dir, cache_dir):
        super().__init__(parent)
        # Load the UI data from the JSON file
        UI_DATA_PATH = path.join(base_dir, "data", "modals", "theme_modal", "language", "en.json")
        THEME_DATA_PATH = path.join(
            base_dir, "data", "modals", "theme_modal", "data", "theme_data.json"
        )
        load_json_data = LoadJsonData()
        self.ui_data = load_json_data.load_json_data(UI_DATA_PATH)
        self.theme_data = load_json_data.load_json_data(THEME_DATA_PATH)

        # Add this mapping for your column headers to data keys
        self.column_mapping = {
            self.ui_data["treeview"]["columns"][0]: "title",  # "Başlık" -> "title"
            self.ui_data["treeview"]["columns"][1]: "description"  # "Açıklama" -> "description"
        }

        self.base_dir = base_dir
        self.cache_dir = cache_dir
        self.configure_layout(parent)
        CenterWindow(self).center_window()

        self.thread_manager = ThreadManager()
        self.theme_manager = ThemeManager(
            json_file_path=path.join(self.cache_dir, self.theme_data["data_path"]),
            json_file_url=self.theme_data["data_url"],
        )
        self.image_cache_dir = path.join(self.cache_dir, "image_cache")

        self.sort_order = "asc"
        self.sort_column = self.ui_data["treeview"]["columns"][0]
        self.current_page = 1
        self.items_per_page = self.theme_data["items_per_page"]
        self.total_pages = 1

        self.create_widgets()
        self.populate_tags()
        self.load_themes()

    def configure_layout(self, parent):
        self.configure(bg="#2B2631")
        self.transient(parent)
        self.geometry("640x610")  # Set the size of the modal for center_window function
        self.resizable(False, False)
        self.wait_visibility()
        self.grab_set()
        self.theme_modal_frame = CTkFrame(
            self, fg_color="#2B2631"
        )
        self.theme_modal_frame.pack(
            fill=BOTH, expand=True, padx=10, pady=10
        )  # Using pack because of the grid layout not working with treeview. (Center_window func not working properly with treeview soo I fix like this :D)
        self.theme_modal_frame.columnconfigure(0, weight=1)

        SetWindowIcon(self.base_dir).set_window_icon(self)

    def create_widgets(self):
        self.create_search_bar()
        self.create_treeview()
        self.create_navigation_buttons()
        self.create_tag_filter()

    def create_search_bar(self):
        self.search_entry = CTkEntry(
            self.theme_modal_frame,
            text_color="#000000",
            border_width=0,
            placeholder_text=self.ui_data["search_bar"][
                "placeholder_text"
            ],
        )
        self.search_entry.grid(row=0, column=0, sticky="EW")
        self.search_entry.bind("<KeyRelease>", self.update_search)

    def create_treeview(self):
        self.tree = ttk.Treeview(
            self.theme_modal_frame,
            columns=self.ui_data["treeview"]["columns"],
            show="headings",
            height=self.items_per_page,
        )

        # Dynamically set column headers based on language data
        for col in self.ui_data["treeview"]["columns"]:
            self.tree.heading(
                col,
                text=col,  # Use translated column names
                command=lambda c=col: self.sort_column_click(c)
            )

        self.tree.column(
            self.ui_data["treeview"]["columns"][1],
            width=400,
        )
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW")
        self.tree.tag_configure(
            "oddrow",
            background="#F1F1F1",
            font=("Inter", 11),
        )
        self.tree.tag_configure(
            "evenrow",
            background="#FFFFFF",
            font=("Inter", 11),
        )

        self.tree.bind("<Double-1>", self.open_theme_detail)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def create_navigation_buttons(self):
        navigation_frame = CTkFrame(self.theme_modal_frame, fg_color="#FFFFFF")
        navigation_frame.grid(row=2, column=0, padx=10, pady=10, sticky="")
        self.select_button = CTkButton(
            navigation_frame,
            text=self.ui_data["buttons"]["select_button"]["text"],
            text_color="#ffffff",
            width=75,
            font=("Inter", 16, "bold"),
            command=self.select_theme,
            state=DISABLED,
        )
        self.select_button.grid(row=0, column=0, padx=10, pady=10, sticky="")

        self.detail_info_text = CTkLabel(
            navigation_frame,
            text=self.ui_data["detail_info_text"]["text"],
        )
        self.detail_info_text.grid(row=1, column=0, sticky="")

        pagination_frame = CTkFrame(navigation_frame, corner_radius=6)
        pagination_frame.grid(row=2, column=0, padx=10, pady=10, sticky="")
        self.prev_button = CTkButton(
            pagination_frame,
            text=self.ui_data["buttons"]["pagination"]["prev_button"][
                "text"
            ],
            command=self.prev_page,
            width=75,
            fg_color="#db7f1f",
            hover_color="#ed963b",
            text_color="#ffffff",
        )
        self.prev_button.pack(side=LEFT, padx=5, pady=5)
        self.page_label = CTkLabel(
            pagination_frame,
            text=self.ui_data["pagination"]["label_template"].format(
                current=self.current_page, total=self.total_pages
            ),
        )
        self.page_label.pack(side=LEFT, padx=5)
        self.next_button = CTkButton(
            pagination_frame,
            text=self.ui_data["buttons"]["pagination"]["next_button"][
                "text"
            ],
            command=self.next_page,
            width=75,
            fg_color="#db7f1f",
            hover_color="#ed963b",
            text_color="#ffffff",
        )
        self.next_button.pack(side=LEFT, padx=5)

    def create_tag_filter(self):
        tags_frame = CTkFrame(self.theme_modal_frame, fg_color="#F8F8F8")
        tags_frame.grid(row=4, column=0, padx=1, pady=10, sticky="")

        self.tag_combobox = ttk.Combobox(tags_frame)
        self.tag_combobox.grid(row=0, column=0, padx=10, pady=10, sticky="EW")
        self.tag_combobox.bind("<KeyRelease>", self.filter_combobox)
        self.tag_combobox.bind("<<ComboboxSelected>>", self.update_search)

        self.tag_info_label = CTkLabel(
            tags_frame, text=self.ui_data["tags"]["text"]
        )
        self.tag_info_label.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="W")

    def populate_tags(self):
        tags = {
            tag for theme in self.theme_manager.get_all_themes() for tag in theme.tags
        }
        sorted_tags = sorted(tags)
        self.all_tags = sorted_tags
        self.tag_combobox["values"] = sorted_tags
        self.tag_combobox.set("")  # Default to empty

    def update_search(self, event=None):
        self.current_page = 1
        self.update_treeview()

    def filter_combobox(self, event=None):
        input_text = self.tag_combobox.get().lower()
        filtered_tags = [tag for tag in self.all_tags if input_text in tag.lower()]
        self.tag_combobox["values"] = filtered_tags

    def retry_loading_themes(self):
        try:
            self.select_button.configure(text=self.ui_data["retrying"]["text"])
            self.theme_manager = ThemeManager(
                path.join(
                    self.cache_dir, self.theme_data["data_path"]
                ),
                self.theme_data["data_url"],
            )
            self.update_treeview()  # Update the treeview after retrying
            if self.theme_manager.get_all_themes():
                self.populate_tags()
                self.select_button.configure(
                    text=self.ui_data["buttons"]["select_button"]["text"],
                    fg_color="#7D31D7",
                    hover_color="#9747FF",
                    command=self.select_theme,  # Set the original command
                    width=75,
                    state=DISABLED,  # Initially disable until a theme is selected
                )
        except Exception as e:
            self.display_error_message(f"{self.ui_data["error_messages"]["retry_failed"]} {e}")
        finally:
            self.enable_buttons()

    def load_themes(self):
        self.disable_buttons()
        self.thread_manager.start_thread(
            target=self.retry_loading_themes, on_finish=self.enable_buttons
        )

    def disable_buttons(self):
        self.select_button.configure(state=DISABLED)
        self.prev_button.configure(state=DISABLED)
        self.next_button.configure(state=DISABLED)

    def enable_buttons(self):
        self.update_pagination_controls()

    def update_treeview(self):
        search_query = self.search_entry.get().lower()
        selected_tag = self.tag_combobox.get()

        if not self.theme_manager.get_all_themes():
            self.display_error_message(self.ui_data["error_messages"]["no_themes"])
            return

        filtered_themes = self.get_filtered_themes(search_query, selected_tag)
        self.total_pages = self.calculate_total_pages(filtered_themes)

        self.tree.delete(*self.tree.get_children())  # Clear Treeview
        self.add_themes_to_treeview(filtered_themes)

        self.update_pagination_controls()

    def display_error_message(self, message):
        self.tree.delete(*self.tree.get_children())  # Clear Treeview
        self.tree.insert("", END, values=(message,), tags=("errorrow",))
        self.tree.tag_configure("errorrow", background="#FFCCCC", foreground="#D8000C")
        self.select_button.configure(
            text=self.ui_data["buttons"]["error_button"]["text"],
            text_color="#ffffff",
            hover_color="#fc3d47",
            fg_color="#D8000C",
            command=self.load_themes,
            state=NORMAL,
        )

    def get_filtered_themes(self, search_query, selected_tag):
        return [
            theme
            for theme in self.theme_manager.get_all_themes()
            if search_query in theme.title.lower()
            and (not selected_tag or selected_tag in theme.tags)
        ]

    def calculate_total_pages(self, filtered_themes):
        return (len(filtered_themes) + self.items_per_page - 1) // self.items_per_page

    def add_themes_to_treeview(self, filtered_themes):
        sorted_themes = sorted(
            filtered_themes,
            key=lambda t: getattr(t, self.column_mapping[self.sort_column], ""),  # Use mapped data field
            reverse=self.sort_order == "desc",
        )
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = min(start_index + self.items_per_page, len(sorted_themes))

        for index, theme in enumerate(sorted_themes[start_index:end_index], start=start_index):
            row_tag = "oddrow" if index % 2 == 0 else "evenrow"
            self.tree.insert(
                "", END, values=(theme.title, theme.description), tags=(row_tag,)
            )

    def update_pagination_controls(self):
        self.prev_button.configure(state=NORMAL if self.current_page > 1 else DISABLED)
        self.next_button.configure(
            state=NORMAL if self.current_page < self.total_pages else DISABLED
        )
        self.page_label.configure(
            text=f"{self.ui_data['pagination']["label_template"]} {self.current_page} / {self.total_pages}"
        )

    def sort_column_click(self, column):
        if self.sort_column == column:
            self.sort_order = "desc" if self.sort_order == "asc" else "asc"
        else:
            self.sort_column = column
            self.sort_order = "asc"
        self.update_treeview()


    def on_select(self, event):
        selected_theme = self.tree.focus()
        self.select_button.configure(state=NORMAL if selected_theme else DISABLED)

    def select_theme(self):
        selected_item = self.tree.selection()
        if selected_item:
            theme_title = self.tree.item(selected_item[0], "values")[0]
            self.theme_selected = self.theme_manager.get_theme_by_title(theme_title)
        self.destroy()

    def open_theme_detail(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            selected_item = selected_items[0]
            selected_theme = self.tree.item(selected_item)["values"][0]
            theme_data = next(
                (
                    theme
                    for theme in self.theme_manager.get_all_themes()
                    if theme.title == selected_theme
                ),
                None,
            )

            if theme_data:
                ThemeDetailModal(self, theme_data, base_dir=self.base_dir)

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_treeview()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_treeview()
