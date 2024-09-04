import json
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry
import threading

from functions.get_theme_data import ThemeManager
from modals.theme_detail_modal import ThemeDetailModal


class ThemeModal(tk.Toplevel):
    def __init__(self, parent, base_dir, cache_dir):
        super().__init__(parent)
        self.load_ui_data(base_dir)
        self.configure(bg=self.data["ThemeModal"]["window"]["background_color"])
        self.transient(parent)
        self.resizable(False, False)
        self.wait_visibility()
        self.grab_set()

        self.base_dir = base_dir
        self.cache_dir = cache_dir
        self.theme_manager = ThemeManager(
            os.path.join(self.base_dir, self.data["ThemeModal"]["themes"]["data_path"]),
            self.data["ThemeModal"]["themes"]["data_url"]
        )
        self.cache_dir = os.path.join(self.cache_dir, "image_cache")
        os.makedirs(self.cache_dir, exist_ok=True)

        self.sort_order = "asc"
        self.sort_column = "Title"
        self.current_page = 1
        self.items_per_page = self.data["ThemeModal"]["themes"]["items_per_page"]
        self.total_pages = 1

        self.configure_layout()
        self.set_window_icon()
        self.create_widgets()
        self.populate_tags()
        self.load_themes()

    def load_ui_data(self, base_dir):
        with open(os.path.join(base_dir, "data", "modals", "theme_modal_data.json"), "r") as file:
            self.data = json.load(file)

    def configure_layout(self):
        self.theme_modal_frame = CTkFrame(self, fg_color=self.data["ThemeModal"]["window"]["background_color"])
        self.theme_modal_frame.grid(row=0, column=1, sticky="SW")
        self.theme_modal_frame.columnconfigure(0, weight=1)

    def set_window_icon(self):
        icon_path = os.path.join(self.base_dir, self.data["ThemeModal"]["window"]["icon_path"])
        try:
            if os.name == "nt":
                self.iconbitmap(icon_path)
            else:
                icon = Image.open(icon_path)
                self.iconphoto(True, ImageTk.PhotoImage(icon))
        except Exception as e:
            print(f"Error setting window icon: {e}")

    def create_widgets(self):
        self.create_search_bar()
        self.create_treeview()
        self.create_navigation_buttons()
        self.create_tag_filter()

    def create_search_bar(self):
        self.search_entry = CTkEntry(
            self.theme_modal_frame,
            placeholder_text=self.data["ThemeModal"]["search_bar"]["placeholder_text"]
        )
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="EW")
        self.search_entry.bind("<KeyRelease>", self.update_search)

    def create_treeview(self):
        self.tree = ttk.Treeview(
            self.theme_modal_frame,
            columns=self.data["ThemeModal"]["treeview"]["columns"],
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
        self.tree.column("Description", width=self.data["ThemeModal"]["treeview"]["description_column_width"])
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="NSEW")
        self.tree.tag_configure("oddrow", background=self.data["ThemeModal"]["treeview"]["oddrow_background"])
        self.tree.tag_configure("evenrow", background=self.data["ThemeModal"]["treeview"]["evenrow_background"])

        self.tree.bind("<Double-1>", self.open_theme_detail)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def create_navigation_buttons(self):
        self.select_button = CTkButton(
            self.theme_modal_frame,
            text=self.data["ThemeModal"]["buttons"]["select_button"]["text"],
            command=self.select_theme,
            state=tk.DISABLED,
            width=self.data["ThemeModal"]["buttons"]["select_button"]["width"],
        )
        self.select_button.grid(row=2, column=0, padx=10, pady=10, sticky="")

        pagination_frame = CTkFrame(self.theme_modal_frame)
        pagination_frame.grid(pady=10)
        self.prev_button = CTkButton(
            pagination_frame,
            text=self.data["ThemeModal"]["buttons"]["pagination"]["prev_button"]["text"],
            command=self.prev_page,
            width=self.data["ThemeModal"]["buttons"]["pagination"]["prev_button"]["width"],
            fg_color=self.data["ThemeModal"]["buttons"]["pagination"]["prev_button"]["fg_color"],
            hover_color=self.data["ThemeModal"]["buttons"]["pagination"]["prev_button"]["hover_color"],
            text_color=self.data["ThemeModal"]["buttons"]["pagination"]["prev_button"]["text_color"],
        )
        self.prev_button.pack(side=tk.LEFT, padx=5)
        self.page_label = CTkLabel(
            pagination_frame, text=self.data["ThemeModal"]["pagination"]["label_template"].format(current=self.current_page, total=self.total_pages)
        )
        self.page_label.pack(side=tk.LEFT, padx=5)
        self.next_button = CTkButton(
            pagination_frame,
            text=self.data["ThemeModal"]["buttons"]["pagination"]["next_button"]["text"],
            command=self.next_page,
            width=self.data["ThemeModal"]["buttons"]["pagination"]["next_button"]["width"],
            fg_color=self.data["ThemeModal"]["buttons"]["pagination"]["next_button"]["fg_color"],
            hover_color=self.data["ThemeModal"]["buttons"]["pagination"]["next_button"]["hover_color"],
            text_color=self.data["ThemeModal"]["buttons"]["pagination"]["next_button"]["text_color"],
        )
        self.next_button.pack(side=tk.LEFT, padx=5)

    def create_tag_filter(self):
        tags_frame = CTkFrame(self.theme_modal_frame)
        tags_frame.grid(row=4, column=0, padx=1, pady=10, sticky="")

        self.tag_combobox = ttk.Combobox(tags_frame)
        self.tag_combobox.grid(row=0, column=0, padx=10, pady=10, sticky="EW")
        self.tag_combobox.bind("<KeyRelease>", self.filter_combobox)
        self.tag_combobox.bind("<<ComboboxSelected>>", self.update_search)

        self.tag_info_label = CTkLabel(tags_frame, text=self.data["ThemeModal"]["tags"]["info_label"])
        self.tag_info_label.grid(row=0, column=1, padx=10, pady=10, sticky="W")

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
                os.path.join(self.base_dir, self.data["ThemeModal"]["themes"]["data_path"]),
                self.data["ThemeModal"]["themes"]["data_url"]
            )
            self.update_treeview()  # Update the treeview after retrying
            if self.theme_manager.get_all_themes():
                self.populate_tags()
                self.select_button.configure(
                    text="Select Theme",
                    fg_color="#771D76",  # Reset to the default color
                    hover_color="#b82eb6",
                    command=self.select_theme,  # Set the original command
                    width=75,
                    state=tk.DISABLED,  # Initially disable until a theme is selected
                )
        except Exception as e:
            self.display_error_message(f"Retry failed: {e}")
        finally:
            self.enable_buttons()

    def load_themes(self):
        self.disable_buttons()
        self.loading_thread = threading.Thread(target=self.retry_loading_themes)
        self.loading_thread.start()

        # Check the thread's status and re-enable buttons when done
        self.check_loading_thread()

    def check_loading_thread(self):
        if self.loading_thread.is_alive():
            self.after(100, self.check_loading_thread)
        else:
            # Re-enable buttons after loading is done
            self.enable_buttons()

    def disable_buttons(self):
        self.select_button.configure(state=tk.DISABLED)
        self.prev_button.configure(state=tk.DISABLED)
        self.next_button.configure(state=tk.DISABLED)

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
        self.tree.insert("", tk.END, values=(message,), tags=("errorrow",))
        self.tree.tag_configure("errorrow", background="#FFCCCC", foreground="#D8000C")
        self.select_button.configure(
            text="Retry",
            text_color="#ffffff",
            hover_color="#fc3d47",
            fg_color="#D8000C",
            command=self.load_themes,
            state=tk.NORMAL,
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
                "", tk.END, values=(theme.title, theme.description), tags=(row_tag,)
            )

    def update_pagination_controls(self):
        self.prev_button.configure(
            state=tk.NORMAL if self.current_page > 1 else tk.DISABLED
        )
        self.next_button.configure(
            state=tk.NORMAL if self.current_page < self.total_pages else tk.DISABLED
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
        self.select_button.configure(state=tk.NORMAL if selected_theme else tk.DISABLED)

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
                ThemeDetailModal(self, theme_data, self.cache_dir, base_dir=self.base_dir)

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_treeview()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_treeview()
