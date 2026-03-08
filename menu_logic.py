import customtkinter as ctk
import os
import json
from tkinter import filedialog, messagebox
from database import load_data, save_config, delete_from_config, load_config

# Paleta kolorow
BG_MAIN = "#1a1a2e"
BG_FRAME = "#16213e"
BG_CARD = "#0f3460"
ACCENT = "#4a9eff"
ACCENT_SUCCESS = "#3ddc84"
ACCENT_ERROR = "#ff6b6b"
ACCENT_WARN = "#ffa94d"
TEXT = "#e8e8f0"
TEXT_DIM = "#8888aa"


class MenuLogic:
    def load_saved_tests(self):
        saved = load_config()
        for test in saved:
            self.create_tests(test["name"], test["path"])

    def button_add_test_event(self):
        name = ctk.CTkInputDialog(text="Wpisz nazwę testu: ", title="Nowy test").get_input()
        if name:
            self.create_tests(name, None)

        data = [
            {
                "licznik": 0,
                    "opcje": {
                        "A": "1",
                        "B": "2",
                        "C": "3",
                        "D": "4"
                     },
                "poprawna": "D",
                "pytanie": "2+2="
            },
            {
                "pytanie": "Czy jesteś dobrym człowiekiem? (Tak/Nie)",
                "poprawna": "Tak",
                "licznik": 0,
                "typ": "otwarte"
            },
        ]
        with open(f"{name}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def create_tests(self, name, path):
        row_frame = ctk.CTkFrame(self.new_tests_frame, fg_color="transparent")
        row_frame.pack(pady=5)

        test_info = {"path": path}

        btn_color = ACCENT_SUCCESS if path else BG_CARD
        test_btn = ctk.CTkButton(
            row_frame,
            text=name,
            text_color=TEXT,
            font=("Arial", 18, "bold"),
            width=500,
            height=60,
            fg_color=btn_color,
            hover_color=ACCENT,
            border_width=1,
            border_color=ACCENT if not path else ACCENT_SUCCESS,
            command=lambda: self.wybor_testu(test_info["path"])
        )
        test_btn.pack(side="left", padx=(5, 1))

        delete_btn = ctk.CTkButton(row_frame, text="X", width=80, height=60,
                                   fg_color=BG_FRAME,
                                   hover_color=ACCENT_ERROR,
                                   text_color=ACCENT_ERROR,
                                   border_width=1,
                                   border_color=ACCENT_ERROR,
                                   command=lambda n=name, f=row_frame: self.delete_test(n, f))
        delete_btn.pack(side="right", padx=5)

        file_button = ctk.CTkButton(
            row_frame,
            text="📁 Plik",
            font=("Arial", 18, "bold"),
            width=100,
            height=60,
            fg_color=BG_FRAME,
            hover_color=BG_CARD,
            text_color=TEXT_DIM,
            border_width=1,
            border_color=TEXT_DIM,
            command=lambda n=name: self.przypisz_plik(n, test_info, test_btn)
        )
        file_button.pack(side="right", padx=(0, 2))

        edit_button = ctk.CTkButton(
            row_frame,
            text="EDYTUJ",
            font=("Arial", 18, "bold"),
            width=100,
            height=60,
            fg_color=BG_FRAME,
            hover_color=ACCENT_WARN,
            text_color=TEXT_DIM,
            border_width=1,
            border_color=TEXT_DIM,
            command=lambda: self.prepare_edit(test_info["path"])
        )
        edit_button.pack(side="right", padx=(5, 5))

    def przypisz_plik(self, nazwa, info_dictionary, btn):
        sciezka = filedialog.askopenfilename(filetypes=[("Json Files", "*.json")])
        if sciezka:
            info_dictionary["path"] = sciezka
            btn.configure(fg_color=ACCENT_SUCCESS)
            save_config(nazwa, sciezka)

    def delete_test(self, nazwa, frame):
        if messagebox.askyesno("Usuń", f"Czy na pewno usunąć test: {nazwa}?"):
            delete_from_config(nazwa)
            frame.destroy()

    def wybor_testu(self, sciezka):
        if sciezka and os.path.exists(sciezka):
            self.baza_sciezka = sciezka
            self.dane = load_data(sciezka)
            self.restart_test()
        else:
            messagebox.showwarning("Brak pliku", "Musisz najpierw wybrać plik JSON!")

    def main_menu(self):
        self.footer_frame.pack_forget()
        self.button_restart_frame.pack_forget()
        self.progressbar.pack_forget()
        self.pytania_label.pack_forget()
        self.pytanie.pack_forget()
        self.button_go_back_to_menu_frame.pack_forget()
        self.buttons_frame.pack_forget()
        self.open_question_frame.pack_forget()
        if hasattr(self, "ai_frame"):
            self.ai_frame.pack_forget()

        if hasattr(self, "stats_frame"):
            self.stats_frame.pack_forget()
        if hasattr(self, "edit_question_menu_frame"):
            self.edit_question_menu_frame.pack_forget()
        if hasattr(self, "edit_question_open_frame"):
            self.edit_question_open_frame.pack_forget()

        if hasattr(self, "show_bledy_btn"):
            self.show_bledy_btn.pack_forget()
        if hasattr(self, "bledy_frame"):
            self.bledy_frame.pack_forget()

        if hasattr(self, "total_questions_label"):
            self.total_questions_label.pack_forget()
        if hasattr(self, "action_buttons_frame"):
            self.action_buttons_frame.pack_forget()
        if not hasattr(self, "add_test_button_frame"):
            self.ui_manager.add_test_button(self, self.button_add_test_event)

        self.new_tests_frame.pack(pady=20, side="top")
        self.add_test_button_frame.pack(pady=20, side="top")
        self.ui_manager.setup_menu(self, self.show_pytania)