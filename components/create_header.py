from customtkinter import CTkLabel

class CreateHeader:
    def __init__(self):
        pass
    
    def create_header(self , home_page_frame, header_title_bg, line_top_img, text):

        header_label = CTkLabel(
            home_page_frame,
            text=text,
            image=header_title_bg,
            text_color="White",
            font=("Inter", 22, "bold"),
        )
        header_label.grid(
            row=0, column=0, columnspan=2, padx=203, pady=(35, 0), sticky="NSEW"
        )

        line_top_label = CTkLabel(
            home_page_frame, text="", image=line_top_img
        )
        line_top_label.grid(
            row=1, column=0, columnspan=2, padx=10, pady=10, sticky="NSEW"
        )
        return header_label, line_top_label