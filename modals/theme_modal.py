from os import path, name
from tkinter import ttk, Toplevel, DISABLED, LEFT, END, NORMAL, BOTH
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry

from components.set_window_icon import SetWindowIcon
from installer_core.component_tools.thread_managing import ThreadManager
from installer_core.data_tools.get_theme_data import ThemeManager
from installer_core.data_tools.load_json_data import LoadJsonData
from modals.theme_detail_modal import ThemeDetailModal


class ThemeModal(Toplevel):
    def __init__(self, parent, base_dir, cache_dir):
        super().__init__(parent)
        # Load the UI data from the JSON file
        UI_DATA_PATH = path.join(base_dir, "data", "modals", "theme_modal_data.json")
        load_json_data = LoadJsonData()
        self.ui_data = load_json_data.load_json_data(UI_DATA_PATH)

        self.base_dir = base_dir
        self.cache_dir = cache_dir
        self.configure_layout(parent)
        self.center_window()

        self.thread_manager = ThreadManager()
        self.theme_manager = ThemeManager(
            json_file_path=path.join(
                self.cache_dir, self.ui_data["ThemeModal"]["themes"]["data_path"]
            ),
            json_file_url=self.ui_data["ThemeModal"]["themes"]["data_url"],
        )
        self.image_cache_dir = path.join(self.cache_dir, "image_cache")

        self.sort_order = "asc"
        self.sort_column = "Title"
        self.current_page = 1
        self.items_per_page = self.ui_data["ThemeModal"]["themes"]["items_per_page"]
        self.total_pages = 1

        self.create_widgets()
        self.populate_tags()
        self.load_themes()

    def configure_layout(self, parent):
        self.configure(bg=self.ui_data["ThemeModal"]["window"]["background_color"])
        self.transient(parent)
        self.geometry("640x610") # Set the size of the modal for center_window function
        self.resizable(False, False)
        self.wait_visibility()
        self.grab_set()
        self.theme_modal_frame = CTkFrame(
            self, fg_color=self.ui_data["ThemeModal"]["window"]["background_color"]
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
            text_color=self.ui_data["ThemeModal"]["search_bar"]["text_color"],
            border_width=self.ui_data["ThemeModal"]["search_bar"]["border_width"],
            placeholder_text=self.ui_data["ThemeModal"]["search_bar"][
                "placeholder_text"
            ],
        )
        self.search_entry.grid(row=0, column=0,sticky="EW")
        self.search_entry.bind("<KeyRelease>", self.update_search)

    def create_treeview(self):
        self.tree = ttk.Treeview(
            self.theme_modal_frame,
            columns=self.ui_data["ThemeModal"]["treeview"]["columns"],
            show="headings",
            height=self.items_per_page,
        )
        self.tree.heading(
            "Title", text="Title", command=lambda: self.sort_column_click("Title")
        )
        self.tree.heading(
            "Description",
            text="Description",
            command=lambda: self.sort_column_click("Description"),
        )
        self.tree.column(
            "Description",
            width=self.ui_data["ThemeModal"]["treeview"]["description_column_width"],
        )
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW")
        self.tree.tag_configure(
            "oddrow",
            background=self.ui_data["ThemeModal"]["treeview"]["oddrow_background"],
            font=eval(self.ui_data["ThemeModal"]["treeview"]["font"]),
        )
        self.tree.tag_configure(
            "evenrow",
            background=self.ui_data["ThemeModal"]["treeview"]["evenrow_background"],
            font=eval(self.ui_data["ThemeModal"]["treeview"]["font"]),
        )

        self.tree.bind("<Double-1>", self.open_theme_detail)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def create_navigation_buttons(self):
        navigation_frame = CTkFrame(self.theme_modal_frame, fg_color="#FFFFFF")
        navigation_frame.grid(row=2, column=0, padx=10, pady=10, sticky="")
        self.select_button = CTkButton(
            navigation_frame,
            text=self.ui_data["ThemeModal"]["buttons"]["select_button"]["text"],
            text_color=self.ui_data["ThemeModal"]["buttons"]["select_button"][
                "text_color"
            ],
            width=self.ui_data["ThemeModal"]["buttons"]["select_button"]["width"],
            font=eval(self.ui_data["ThemeModal"]["buttons"]["select_button"]["font"]),
            command=self.select_theme,
            state=DISABLED,
        )
        self.select_button.grid(row=0, column=0, padx=10, pady=10, sticky="")

        self.detail_info_text = CTkLabel(
            navigation_frame,
            text=self.ui_data["ThemeModal"]["detail_info_text"]["text"],
        )
        self.detail_info_text.grid(row=1, column=0, sticky="")

        pagination_frame = CTkFrame(navigation_frame, corner_radius=6)
        pagination_frame.grid(row=2, column=0, padx=10, pady=10, sticky="")
        self.prev_button = CTkButton(
            pagination_frame,
            text=self.ui_data["ThemeModal"]["buttons"]["pagination"]["prev_button"][
                "text"
            ],
            command=self.prev_page,
            width=self.ui_data["ThemeModal"]["buttons"]["pagination"]["prev_button"][
                "width"
            ],
            fg_color=self.ui_data["ThemeModal"]["buttons"]["pagination"]["prev_button"][
                "fg_color"
            ],
            hover_color=self.ui_data["ThemeModal"]["buttons"]["pagination"][
                "prev_button"
            ]["hover_color"],
            text_color=self.ui_data["ThemeModal"]["buttons"]["pagination"][
                "prev_button"
            ]["text_color"],
        )
        self.prev_button.pack(side=LEFT, padx=5, pady=5)
        self.page_label = CTkLabel(
            pagination_frame,
            text=self.ui_data["ThemeModal"]["pagination"]["label_template"].format(
                current=self.current_page, total=self.total_pages
            ),
        )
        self.page_label.pack(side=LEFT, padx=5)
        self.next_button = CTkButton(
            pagination_frame,
            text=self.ui_data["ThemeModal"]["buttons"]["pagination"]["next_button"][
                "text"
            ],
            command=self.next_page,
            width=self.ui_data["ThemeModal"]["buttons"]["pagination"]["next_button"][
                "width"
            ],
            fg_color=self.ui_data["ThemeModal"]["buttons"]["pagination"]["next_button"][
                "fg_color"
            ],
            hover_color=self.ui_data["ThemeModal"]["buttons"]["pagination"][
                "next_button"
            ]["hover_color"],
            text_color=self.ui_data["ThemeModal"]["buttons"]["pagination"][
                "next_button"
            ]["text_color"],
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
            tags_frame, text=self.ui_data["ThemeModal"]["tags"]["text"]
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
            self.select_button.configure(text="Retrying")
            self.theme_manager = ThemeManager(
                path.join(
                    self.cache_dir, self.ui_data["ThemeModal"]["themes"]["data_path"]
                ),
                self.ui_data["ThemeModal"]["themes"]["data_url"],
            )
            self.update_treeview()  # Update the treeview after retrying
            if self.theme_manager.get_all_themes():
                self.populate_tags()
                self.select_button.configure(
                    text=self.ui_data["ThemeModal"]["buttons"]["select_button"]["text"],
                    fg_color=self.ui_data["ThemeModal"]["buttons"]["select_button"][
                        "fg_color"
                    ],
                    hover_color=self.ui_data["ThemeModal"]["buttons"]["select_button"][
                        "hover_color"
                    ],
                    command=self.select_theme,  # Set the original command
                    width=75,
                    state=DISABLED,  # Initially disable until a theme is selected
                )
        except Exception as e:
            self.display_error_message(f"Retry failed: {e}")
        finally:
            self.enable_buttons()

    def load_themes(self):
        self.disable_buttons()
        self.thread_manager.start_thread(target=self.retry_loading_themes)

        self.check_loading_thread()

    def check_loading_thread(self):
        if self.thread_manager.are_threads_alive():
            self.after(100, self.check_loading_thread)
        else:
            # Re-enable buttons after loading is done
            self.enable_buttons()

    def disable_buttons(self):
        self.select_button.configure(state=DISABLED)
        self.prev_button.configure(state=DISABLED)
        self.next_button.configure(state=DISABLED)

    def enable_buttons(self):
        self.update_pagination_controls()

    def update_treeview(self):
        search_query = self.search_entry.get().lower()
        selected_tag = self.tag_combobox.get()

        # Check if theme_manager is empty
        if not self.theme_manager.get_all_themes():
            self.display_error_message(
                "No themes available. Please check your theme source or internet connection."
            )
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
            text="Retry",
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
            key=lambda t: getattr(t, self.sort_column.lower()),
            reverse=self.sort_order == "desc",
        )
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = min(start_index + self.items_per_page, len(sorted_themes))

        for index, theme in enumerate(
            sorted_themes[start_index:end_index], start=start_index
        ):
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
            text=f"Page {self.current_page} of {self.total_pages}"
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

    def center_window(self):
        """Center the modal window on the screen."""
        self.update_idletasks()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry("+{}+{}".format(x, y))
