import customtkinter as ctk
BG_MAIN = "#1a1a2e"
BG_FRAME = "#16213e"
BG_CARD = "#0f3460"
ACCENT = "#4a9eff"
ACCENT_SUCCESS = "#3ddc84"
ACCENT_ERROR = "#ff6b6b"
ACCENT_WARN = "#ffa94d"
TEXT = "#e8e8f0"
TEXT_DIM = "#8888aa"


class QuizUIMenu:
    def setup_menu(self, master, button_command):
        if not hasattr(master, 'menu_button_frame'):
            master.menu_button_frame = ctk.CTkFrame(master, fg_color="transparent")

            master.menu_start_button = ctk.CTkButton(
                master.menu_button_frame,
                text="Rozpocznij Test",
                font=("Arial", 18, "bold"),
                command=button_command,
                width=600,
                height=60,
                fg_color=ACCENT,
                hover_color=BG_CARD,
                text_color=TEXT
            )

        master.signature_label = ctk.CTkLabel(master, fg_color="transparent",
                                              text="Exam tester made by Oliwier Maziarz",
                                              text_color=TEXT_DIM,
                                              font=("Arial", 12))
        master.signature_label.pack(pady=20, side="bottom")

    def add_test_button(self, master, button_command):
        master.add_test_button_frame = ctk.CTkFrame(master, fg_color="transparent")
        master.add_test_button_frame.pack(pady=20, side="top")

        master.add_test_button = ctk.CTkButton(master.add_test_button_frame, text="Dodaj test",
                                               font=("Arial", 18, "bold"), command=button_command, width=600, height=60,
                                               fg_color=BG_CARD,
                                               hover_color=ACCENT,
                                               text_color=TEXT,
                                               border_width=1,
                                               border_color=ACCENT)
        master.add_test_button.pack(pady=20, side="top")

    def scrollable_tests_frame(self, master):
        master.new_test_names = []

        master.new_tests_frame = ctk.CTkScrollableFrame(master, fg_color=BG_FRAME, width=800, height=800,
                                                        scrollbar_button_color=ACCENT,
                                                        scrollbar_button_hover_color=BG_CARD)
        master.new_tests_frame.pack(pady=20, side="top")

        master.new_tests_line_frame = ctk.CTkFrame(master.new_tests_frame, fg_color="transparent")
        master.new_tests_line_frame.pack(pady=20, side="bottom")