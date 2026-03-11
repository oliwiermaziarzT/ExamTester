import customtkinter as ctk
from ai_helper import get_api_key, save_api_key

BG_MAIN = "#1a1a2e"
BG_FRAME = "#16213e"
BG_CARD = "#0f3460"
ACCENT = "#4a9eff"
ACCENT_SUCCESS = "#3ddc84"
ACCENT_ERROR = "#ff6b6b"
ACCENT_WARN = "#ffa94d"
TEXT = "#e8e8f0"
TEXT_DIM = "#8888aa"
ACCENT_AI = "#b47eff"


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
            master.menu_start_button.pack(pady=0)


        master.signature_label = ctk.CTkLabel(master, fg_color="transparent",
                                              text="Exam tester made by Oliwier Maziarz",
                                              text_color=TEXT_DIM,
                                              font=("Arial", 12))
        master.signature_label.pack(pady=0, side="bottom")

    def add_test_button(self, master, button_command):
        master.add_test_button_frame = ctk.CTkFrame(master, fg_color="transparent")
        master.add_test_button_frame.pack(pady=0, side="top")

        master.add_test_button = ctk.CTkButton(
            master.add_test_button_frame,
            text="Dodaj test",
            font=("Arial", 18, "bold"),
            command=button_command,
            width=600,
            height=60,
            fg_color=BG_CARD,
            hover_color=ACCENT,
            text_color=TEXT,
            border_width=1,
            border_color=ACCENT
        )
        master.add_test_button.pack(pady=5, side="top")

    def setup_add_test_through_ai(self, master):
        master.add_test_through_ai_frame = ctk.CTkFrame(master, fg_color="transparent")

        master.add_test_through_ai_btn = ctk.CTkButton(
            master.add_test_through_ai_frame,
            text="Dodaj test przez AI ✦",
            font=("Arial", 18, "bold"),
            command=lambda: master.button_add_test_ai_event(),
            width=600,
            height=60,
            fg_color=BG_CARD,
            hover_color="#5a3e8a",
            text_color=ACCENT_AI,
            border_width=1,
            border_color=ACCENT_AI
        )
        master.add_test_through_ai_btn.pack(pady=5, side="top")

    def setup_api_key_widget(self, master):
        master.api_key_frame = ctk.CTkFrame(master, fg_color=BG_FRAME, corner_radius=10)
        row = ctk.CTkFrame(master.api_key_frame, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=10)

        ctk.CTkLabel(
            row, text="✦ Groq API Key:",
            font=("Arial", 13, "bold"),
            text_color=ACCENT_AI, width=130
        ).pack(side="left", padx=(0, 8))

        master.api_key_entry = ctk.CTkEntry(
            row,
            placeholder_text="gsk_...",
            font=("Arial", 13),
            width=340, height=36,
            fg_color=BG_CARD,
            text_color=TEXT,
            border_color=ACCENT_AI,
            border_width=1,
            show="*"
        )
        master.api_key_entry.pack(side="left", padx=(0, 8))
        saved_key = get_api_key()
        if saved_key:
            master.api_key_entry.insert(0, saved_key)

        master._api_key_status = ctk.CTkLabel(
            row, text="✓ Klucz zapisany" if saved_key else "Brak klucza",
            font=("Arial", 12),
            text_color=ACCENT_SUCCESS if saved_key else TEXT_DIM,
            width=130
        )
        master._api_key_status.pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            row, text="Zapisz",
            font=("Arial", 13, "bold"),
            width=90, height=36,
            fg_color=ACCENT_AI, hover_color="#8a5eff",
            text_color=TEXT,
            command=lambda: self._save_api_key_event(master)
        ).pack(side="left")

    def _save_api_key_event(self, master):
        key = master.api_key_entry.get().strip()
        if key:
            save_api_key(key)
            master._api_key_status.configure(text="✓ Zapisano!", text_color=ACCENT_SUCCESS)
            master.after(2000, lambda: master._api_key_status.configure(
                text="✓ Klucz zapisany", text_color=ACCENT_SUCCESS
            ))
        else:
            master._api_key_status.configure(text="Wpisz klucz!", text_color=ACCENT_ERROR)

    def scrollable_tests_frame(self, master):
        master.new_test_names = []

        master.new_tests_frame = ctk.CTkScrollableFrame(
            master,
            fg_color=BG_FRAME,
            width=800,
            height=650,
            scrollbar_button_color=ACCENT,
            scrollbar_button_hover_color=BG_CARD
        )
        master.new_tests_frame.pack(pady=20, side="top")

        master.new_tests_line_frame = ctk.CTkFrame(master.new_tests_frame, fg_color="transparent")
        master.new_tests_line_frame.pack(pady=20, side="bottom")