import customtkinter as ctk
import os
import json
from tkinter import filedialog, messagebox
from database import load_data, save_config, save_config_category, delete_from_config, load_config

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
        self._rebuild_tests_display(saved)

    def _rebuild_tests_display(self, saved=None):
        for widget in self.new_tests_frame.winfo_children():
            widget.destroy()

        if saved is None:
            saved = load_config()

        categories = {}
        for test in saved:
            cat = test.get("category", "").strip() or "Bez kategorii"
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(test)

        sorted_cats = sorted(k for k in categories if k != "Bez kategorii")
        if "Bez kategorii" in categories:
            sorted_cats.append("Bez kategorii")

        show_headers = len(sorted_cats) > 1 or (len(sorted_cats) == 1 and sorted_cats[0] != "Bez kategorii")

        for cat_name in sorted_cats:
            if show_headers:
                header_frame = ctk.CTkFrame(self.new_tests_frame, fg_color=BG_CARD, corner_radius=8)
                header_frame.pack(fill="x", padx=30, pady=(14, 2))
                ctk.CTkLabel(
                    header_frame,
                    text=f"📁  {cat_name}",
                    font=("Arial", 15, "bold"),
                    text_color=ACCENT_WARN,
                    fg_color="transparent"
                ).pack(side="left", padx=14, pady=6)

            for test in categories[cat_name]:
                self.create_tests(test["name"], test["path"], test.get("category", ""))

    def button_add_test_event(self):
        name = ctk.CTkInputDialog(text="Wpisz nazwę testu: ", title="Nowy test").get_input()
        if name:
            folder_path = "database"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            file_path = os.path.join(folder_path, f"{name}.json")

            data = [
                {
                    "licznik": 0,
                    "opcje": {"A": "1", "B": "2", "C": "3", "D": "4"},
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

            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            save_config(name, file_path)
            self._rebuild_tests_display()

    def button_add_test_ai_event(self):
        self.ui_manager.show_ai_generator_menu(self)

    def create_tests(self, name, path, category=""):
        row_frame = ctk.CTkFrame(self.new_tests_frame, fg_color="transparent")
        row_frame.pack(pady=5)

        test_info = {"path": path}

        btn_color = ACCENT_SUCCESS if path else BG_CARD
        test_btn = ctk.CTkButton(
            row_frame,
            text=name,
            text_color=TEXT,
            font=("Arial", 18, "bold"),
            width=410,
            height=60,
            fg_color=btn_color,
            hover_color=ACCENT,
            border_width=1,
            border_color=ACCENT if not path else ACCENT_SUCCESS,
            command=lambda: self.wybor_testu(test_info["path"])
        )
        test_btn.pack(side="left", padx=(5, 1))

        delete_btn = ctk.CTkButton(
            row_frame, text="✕", width=55, height=60,
            fg_color=BG_FRAME,
            hover_color=ACCENT_ERROR,
            text_color=ACCENT_ERROR,
            border_width=1,
            border_color=ACCENT_ERROR,
            command=lambda n=name, f=row_frame: self.delete_test(n, f)
        )
        delete_btn.pack(side="right", padx=(2, 4))

        file_button = ctk.CTkButton(
            row_frame,
            text="📁",
            font=("Arial", 18, "bold"),
            width=55,
            height=60,
            fg_color=BG_FRAME,
            hover_color=BG_CARD,
            text_color=TEXT_DIM,
            border_width=1,
            border_color=TEXT_DIM,
            command=lambda n=name: self.przypisz_plik(n, test_info, test_btn)
        )
        file_button.pack(side="right", padx=(2, 2))

        edit_button = ctk.CTkButton(
            row_frame,
            text="MENU",
            font=("Arial", 15, "bold"),
            width=80,
            height=60,
            fg_color=BG_FRAME,
            hover_color=ACCENT_WARN,
            text_color=TEXT_DIM,
            border_width=1,
            border_color=TEXT_DIM,
            command=lambda: self.prepare_edit(test_info["path"])
        )
        edit_button.pack(side="right", padx=(2, 2))

        cat_label = category.strip() if category.strip() else "🏷"
        cat_btn = ctk.CTkButton(
            row_frame,
            text=cat_label,
            font=("Arial", 13, "bold"),
            width=75,
            height=60,
            fg_color=BG_FRAME,
            hover_color=BG_CARD,
            text_color=ACCENT_WARN if category.strip() else TEXT_DIM,
            border_width=1,
            border_color=ACCENT_WARN if category.strip() else TEXT_DIM,
            command=lambda n=name: self._assign_category_dialog(n)
        )
        cat_btn.pack(side="right", padx=(2, 2))

    def _assign_category_dialog(self, name):
        cat = ctk.CTkInputDialog(
            text=f"Wpisz kategorię dla testu \"{name}\"\n(zostaw puste, aby usunąć kategorię):",
            title="Przypisz kategorię"
        ).get_input()
        if cat is not None:
            save_config_category(name, cat.strip())
            self._rebuild_tests_display()

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
            self.bledy_mode = False
            self.restart_test()
        else:
            messagebox.showwarning("Brak pliku", "Musisz najpierw wybrać plik JSON!")

    def main_menu(self):
        self.unbind("<Alt-Return>")
        self.unbind("<Alt-KP_Enter>")
        self.bledy_mode = False

        self.footer_frame.pack_forget()
        self.button_restart_frame.pack_forget()
        self.progressbar.pack_forget()
        self.pytania_label.pack_forget()
        self.pytanie.pack_forget()
        self.button_go_back_to_menu_frame.pack_forget()
        self.buttons_frame.pack_forget()
        self.open_question_frame.pack_forget()
        if hasattr(self, "center_frame"):
            self.center_frame.pack_forget()
        if hasattr(self, "ai_frame"):
            self.ai_frame.pack_forget()
        if hasattr(self, "ai_generator_frame"):
            self.ai_generator_frame.pack_forget()
        if hasattr(self, "ai_preview_frame"):
            self.ai_preview_frame.pack_forget()
        if hasattr(self, "api_key_frame"):
            self.api_key_frame.pack_forget()


        for w in ["stats_frame", "edit_question_menu_frame", "edit_question_open_frame",
                  "total_questions_label", "action_buttons_frame", "action_buttons_frame2",
                  "go_back_to_edit_menu_btn", "change_question_frame", "add_question_menu_frame",
                  "add_question_open_frame", "last_results_btn", "last_results_frame"]:
            widget = getattr(self, w, None)
            if widget:
                widget.pack_forget()


        if hasattr(self, "show_bledy_btn"):
            self.show_bledy_btn.pack_forget()
        if hasattr(self, "bledy_frame"):
            self.bledy_frame.pack_forget()
        if hasattr(self, "restart_test_bledy"):
            self.restart_test_bledy.pack_forget()


        if not hasattr(self, "add_test_button_frame"):
            self.ui_manager.add_test_button(self, self.button_add_test_event)
        if not hasattr(self, "add_test_through_ai_frame"):
            self.ui_manager.setup_add_test_through_ai(self)


        self.new_tests_frame.pack(pady=20, side="top")
        self.add_test_button_frame.pack(pady=20, side="top")
        self.add_test_through_ai_frame.pack(pady=20, side="top")
        self.api_key_frame.pack(pady=10, side="top")
        self.ui_manager.setup_menu(self, self.show_pytania)