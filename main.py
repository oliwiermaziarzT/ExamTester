import customtkinter as ctk
import os
from database import load_data
from gui import QuizUI
from quiz_logic import QuizLogic
from edit_logic import EditLogic
from menu_logic import MenuLogic

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk, QuizLogic, EditLogic, MenuLogic):
    def __init__(self, baza):
        super().__init__()
        self.baza_sciezka = baza

        # okno
        self.configure(fg_color="#1a1a2e")
        self.geometry("1908x1050")
        self.title("Przygotowanie do egzaminu")

        self.dane = load_data(baza)
        self.index = 0
        self.poprawne = 0
        self.niepoprawne = 0
        self.bledy = []
        self.question_answered = False
        self.current_edit_index = None
        self.historia_bledow = {}

        # ui
        self.ui_manager = QuizUI()
        self.ui_manager.setup_ui(self, self.check_answer_closed, self.check_answer_open)
        self.ui_manager.back_to_menu(self, self.main_menu)
        self.ui_manager.scrollable_tests_frame(self)

        # quiz
        self.load_saved_tests()
        self.main_menu()
        self.update_stats()


if __name__ == "__main__":
    nazwa_bazy = "baza.json"
    if not os.path.exists(nazwa_bazy):
        with open(nazwa_bazy, "w", encoding="utf-8") as f:
            f.write("[]")
    app = App(nazwa_bazy)
    app.mainloop()