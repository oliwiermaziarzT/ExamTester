import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ai_helper import zapytaj_ollame, zbuduj_prompt_blad

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


class QuizUIEdit:
    def nothing(self, master):
        widgets_to_hide = [
            "footer_frame",
            "button_restart_frame",
            "progressbar",
            "pytania_label",
            "pytanie",
            "button_go_back_to_menu_frame",
            "buttons_frame",
            "open_question_frame",
            "new_tests_frame",
            "add_test_button_frame",
            "menu_button_frame",
            "signature_label",
            "action_buttons_frame",
            "go_back_to_edit_menu_btn",
            "add_question_menu_frame",
            "add_question_open_frame",
            "change_question_frame",
            "total_questions_label",
            "show_bledy_btn",
            "bledy_frame",
            "stats_frame",
            "edit_question_menu_frame",
            "edit_question_open_frame",
            "go_back_to_list_btn",
            "last_results_btn",
            "last_results_frame",
            "ai_frame",
            "center_frame",
            "restart_test_bledy",
            "action_buttons_frame2",
            "add_test_through_ai_frame",
            "ai_generator_frame",
            "ai_preview_frame",
            "api_key_frame"
        ]

        for widget_name in widgets_to_hide:
            widget = getattr(master, widget_name, None)
            if widget and widget.winfo_exists():
                widget.pack_forget()
                widget.place_forget()
        if hasattr(master, 'fig_stats'):
            plt.close(master.fig_stats)

    def show_edit_menu(self, master):
        self.nothing(master)

        master.total_questions_label = ctk.CTkLabel(
            master,
            text=f"Suma pytań w tym teście: {len(master.dane)}",
            font=("Arial", 22, "bold"),
            text_color=TEXT
        )
        master.total_questions_label.pack(pady=(20, 0))

        master.action_buttons_frame = ctk.CTkFrame(master, fg_color="transparent")
        master.action_buttons_frame.pack(pady=20, side="top", fill="x", padx=50)

        btn_height = 80
        btn_width = 200

        master.btn_add_closed = ctk.CTkButton(
            master.action_buttons_frame,
            text="Dodaj pytanie zamkniete",
            fg_color=BG_CARD,
            hover_color=ACCENT,
            text_color=TEXT,
            border_width=1,
            border_color=ACCENT,
            font=("Arial", 18, "bold"),
            height=btn_height,
            width=btn_width,
            command=master.start_add_question_closed,
        )
        master.btn_add_closed.pack(side="left", fill="x", expand=True, padx=15)
        master.btn_change = ctk.CTkButton(
            master.action_buttons_frame,
            text="Zmień lub usuń pytanie",
            fg_color=BG_CARD,
            hover_color=ACCENT_WARN,
            text_color=TEXT,
            border_width=1,
            border_color=ACCENT_WARN,
            font=("Arial", 18, "bold"),
            height=btn_height,
            width=btn_width,
            command=master.start_change_question,
        )
        master.btn_change.pack(side="left", fill="x", expand=True, padx=15)
        master.btn_add_open = ctk.CTkButton(
            master.action_buttons_frame,
            text="Dodaj pytanie otwarte",
            fg_color=BG_CARD,
            hover_color=ACCENT,
            text_color=TEXT,
            border_width=1,
            border_color=ACCENT,
            font=("Arial", 18, "bold"),
            height=btn_height,
            width=btn_width,
            command=master.start_add_question_open,
        )
        master.btn_add_open.pack(side="left", fill="x", expand=True, padx=15)
        master.button_go_back_to_menu_frame.pack(side="bottom", pady=20)

        master.action_buttons_frame2 = ctk.CTkFrame(master, fg_color="transparent")
        master.action_buttons_frame2.pack(pady=(0, 10), side="top", fill="x", padx=50)

        master.btn_unlearned = ctk.CTkButton(
            master.action_buttons_frame2,
            text="▶  Testuj nienauczone pytania",
            fg_color=BG_CARD,
            hover_color=ACCENT_SUCCESS,
            text_color=ACCENT_SUCCESS,
            border_width=1,
            border_color=ACCENT_SUCCESS,
            font=("Arial", 18, "bold"),
            height=btn_height,
            width=btn_width,
            command=lambda: (self.nothing(master), master.start_unlearned_test()),
        )
        master.btn_unlearned.pack(side="left", fill="x", expand=True, padx=15)

        master.btn_start_full = ctk.CTkButton(
            master.action_buttons_frame2,
            text="▶  Rozpocznij pełny test",
            fg_color=BG_CARD,
            hover_color=ACCENT,
            text_color=ACCENT,
            border_width=1,
            border_color=ACCENT,
            font=("Arial", 18, "bold"),
            height=btn_height,
            width=btn_width,
            command=lambda: (self.nothing(master), master.restart_test()),
        )
        master.btn_start_full.pack(side="left", fill="x", expand=True, padx=15)

        master.stats_frame = ctk.CTkFrame(master, fg_color="transparent")
        master.stats_frame.pack(pady=10, fill="x", padx=50)

        total = len(master.dane)
        otwarte = sum(1 for q in master.dane if q.get("typ") == "otwarte")
        zamkniete = total - otwarte
        nauczone = sum(1 for q in master.dane if q.get("licznik", 0) > 2)
        nienauczone = total - nauczone

        stats_text = f"Otwarte: {otwarte} | Zamknięte: {zamkniete}   ---   Nauczone: {nauczone} | Nienauczone: {nienauczone}"
        master.stats_label = ctk.CTkLabel(master.stats_frame, text=stats_text, font=("Arial", 18, "bold"),
                                          text_color=ACCENT_SUCCESS)
        master.stats_label.pack(pady=5)

        if total > 0:
            master.fig_stats, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5), facecolor=BG_FRAME,
                                                        constrained_layout=True)
            master.fig_stats.patch.set_facecolor(BG_MAIN)

            ax1.pie([otwarte, zamkniete] if otwarte or zamkniete else [1],
                    labels=['Otwarte', 'Zamknięte'] if otwarte or zamkniete else ['Brak'],
                    autopct='%1.1f%%' if otwarte or zamkniete else '',
                    colors=[ACCENT, ACCENT_ERROR], textprops={'color': TEXT})
            ax1.set_title("Typy pytań", color=TEXT)

            ax2.pie([nauczone, nienauczone] if nauczone or nienauczone else [1],
                    labels=['Nauczone', 'Nienauczone'] if nauczone or nienauczone else ['Brak'],
                    autopct='%1.1f%%' if nauczone or nienauczone else '',
                    colors=[ACCENT_SUCCESS, ACCENT_ERROR], textprops={'color': TEXT})
            ax2.set_title("Postęp nauki", color=TEXT)

            master.canvas = FigureCanvasTkAgg(master.fig_stats, master.stats_frame)
            master.canvas.draw()
            master.canvas.get_tk_widget().pack(pady=10)
            master.last_results_btn = ctk.CTkButton(
                master.stats_frame,
                text="Ostatnie rezultaty i statystyki pytań",
                font=("Arial", 18, "bold"),
                fg_color=BG_CARD,
                hover_color=ACCENT_WARN,
                text_color=TEXT,
                border_width=1,
                border_color=ACCENT_WARN,
                width=300,
                height=45,
                command=master.show_last_results_event
            )
            master.last_results_btn.pack(pady=10)

    def add_question_closed_menu(self, master, save_command):
        self.nothing(master)

        master.total_questions_label = ctk.CTkLabel(
            master,
            text=f"Suma pytań w tym teście: {len(master.dane)}",
            font=("Arial", 22, "bold"),
            text_color=TEXT
        )
        master.total_questions_label.pack(pady=(20, 0))

        self.go_back_to_edit_menu_btn(master)

        master.add_question_menu_frame = ctk.CTkFrame(master, fg_color=BG_FRAME, corner_radius=12)
        master.add_question_menu_frame.pack(pady=50, fill="x", padx=50)

        master.question_label_frame = ctk.CTkFrame(master.add_question_menu_frame, fg_color="transparent",
                                                   corner_radius=20)
        master.question_label_frame.pack(pady=5, side="top", fill="x", padx=50)

        master.question_label = ctk.CTkButton(master.question_label_frame, fg_color=BG_CARD,
                                              font=("Arial", 28, "bold"), text="Wprowadź pytanie zamknięte", width=325,
                                              height=55, text_color_disabled=TEXT_DIM, state="disabled",
                                              text_color=TEXT)
        master.question_label.pack(pady=20, side="top", padx=50)

        master.question_input = ctk.CTkEntry(master.question_label_frame, fg_color=BG_CARD, height=50,
                                             font=("Arial", 28, "bold"), placeholder_text="Wprowadź Pytanie",
                                             border_color=ACCENT, border_width=1, text_color=TEXT)
        master.question_input.pack(pady=10, fill="x", padx=50)

        master.answers_label_frame = ctk.CTkFrame(master.add_question_menu_frame, fg_color="transparent",
                                                  corner_radius=20)
        master.answers_label_frame.pack(pady=5, side="top", padx=50, fill="x")

        master.question_label = ctk.CTkButton(master.answers_label_frame, fg_color=BG_CARD,
                                              font=("Arial", 28, "bold"), text="Wprowadź odpowiedzi", width=325,
                                              height=55, text_color_disabled=TEXT_DIM, state="disabled",
                                              text_color=TEXT)
        master.question_label.pack(pady=10, side="top", padx=50)

        master.option_input1 = ctk.CTkEntry(master.answers_label_frame, fg_color=BG_CARD, height=50,
                                            font=("Arial", 28, "bold"), placeholder_text="Wpisz odpowiedź A:",
                                            border_color=ACCENT, border_width=1, text_color=TEXT)
        master.option_input1.pack(pady=10, fill="x", padx=50)

        master.option_input2 = ctk.CTkEntry(master.answers_label_frame, fg_color=BG_CARD, height=50,
                                            font=("Arial", 28, "bold"), placeholder_text="Wpisz odpowiedź B:",
                                            border_color=ACCENT, border_width=1, text_color=TEXT)
        master.option_input2.pack(pady=10, fill="x", padx=50)

        master.option_input3 = ctk.CTkEntry(master.answers_label_frame, fg_color=BG_CARD, height=50,
                                            font=("Arial", 28, "bold"), placeholder_text="Wpisz odpowiedź C:",
                                            border_color=ACCENT, border_width=1, text_color=TEXT)
        master.option_input3.pack(pady=10, fill="x", padx=50)

        master.option_input4 = ctk.CTkEntry(master.answers_label_frame, fg_color=BG_CARD, height=50,
                                            font=("Arial", 28, "bold"), placeholder_text="Wpisz odpowiedź D:",
                                            border_color=ACCENT, border_width=1, text_color=TEXT)
        master.option_input4.pack(pady=10, fill="x", padx=50)

        master.correct_option_label = ctk.CTkButton(master.answers_label_frame, fg_color=BG_CARD,
                                                    font=("Arial", 28, "bold"), text="Wprowadź poprawną odpowiedź",
                                                    width=325, height=55, text_color_disabled=TEXT_DIM, state="disabled",
                                                    text_color=TEXT)
        master.correct_option_label.pack(pady=10, side="top", padx=50)

        master.correct_option = ctk.CTkEntry(master.answers_label_frame, fg_color=BG_CARD, height=50,
                                             font=("Arial", 28, "bold"),
                                             placeholder_text="Wpisz poprawną odpowiedź czyli: A/B/C/D",
                                             border_color=ACCENT_SUCCESS, border_width=1, text_color=TEXT)
        master.correct_option.pack(pady=10, fill="x", padx=50)

        master.button_submit_addition = ctk.CTkButton(master.answers_label_frame, fg_color=BG_FRAME,
                                                      text="Commit changes", width=325, height=80,
                                                      font=("Arial", 28, "bold"),
                                                      hover_color=ACCENT_SUCCESS,
                                                      text_color=ACCENT_SUCCESS,
                                                      border_width=1,
                                                      border_color=ACCENT_SUCCESS,
                                                      command=lambda: save_command("zamkniete"))
        master.button_submit_addition.pack(pady=30, padx=50)
        master.question_input.focus_set()

    def edit_question_closed_menu(self, master, save_command, data):
        self.nothing(master)

        master.total_questions_label = ctk.CTkLabel(
            master,
            text=f"Edytujesz pytanie z testu ({len(master.dane)} pytań ogółem)",
            font=("Arial", 22, "bold"),
            text_color=TEXT
        )
        master.total_questions_label.pack(pady=(20, 0))

        master.go_back_to_list_btn = ctk.CTkButton(master, text="Powrót do listy pytań", font=("Arial", 18, "bold"),
                                                   command=master.start_change_question, height=50,
                                                   width=200,
                                                   fg_color=BG_FRAME,
                                                   hover_color=ACCENT_SUCCESS,
                                                   text_color=TEXT,
                                                   border_width=1,
                                                   border_color=ACCENT_SUCCESS)
        master.go_back_to_list_btn.pack(pady=40, side="bottom", padx=50)

        master.edit_question_menu_frame = ctk.CTkFrame(master, fg_color=BG_FRAME, corner_radius=12)
        master.edit_question_menu_frame.pack(pady=50, fill="x", padx=50)

        master.question_label_frame = ctk.CTkFrame(master.edit_question_menu_frame, fg_color="transparent",
                                                   corner_radius=20)
        master.question_label_frame.pack(pady=5, side="top", fill="x", padx=50)

        master.question_label = ctk.CTkButton(master.question_label_frame, fg_color=BG_CARD,
                                              font=("Arial", 28, "bold"), text="Edytuj pytanie zamknięte", width=325,
                                              height=55, text_color_disabled=TEXT_DIM, state="disabled",
                                              text_color=ACCENT_WARN)
        master.question_label.pack(pady=20, side="top", padx=50)

        master.question_input = ctk.CTkEntry(master.question_label_frame, fg_color=BG_CARD, height=50,
                                             font=("Arial", 28, "bold"), placeholder_text="Wprowadź Pytanie",
                                             border_color=ACCENT_WARN, border_width=1, text_color=TEXT)
        master.question_input.pack(pady=10, fill="x", padx=50)
        master.question_input.insert(0, data.get("pytanie", ""))

        master.answers_label_frame = ctk.CTkFrame(master.edit_question_menu_frame, fg_color="transparent",
                                                  corner_radius=20)
        master.answers_label_frame.pack(pady=5, side="top", padx=50, fill="x")

        master.question_label = ctk.CTkButton(master.answers_label_frame, fg_color=BG_CARD,
                                              font=("Arial", 28, "bold"), text="Edytuj odpowiedzi", width=325,
                                              height=55, text_color_disabled=TEXT_DIM, state="disabled",
                                              text_color=ACCENT_WARN)
        master.question_label.pack(pady=10, side="top", padx=50)

        master.option_input1 = ctk.CTkEntry(master.answers_label_frame, fg_color=BG_CARD, height=50,
                                            font=("Arial", 28, "bold"), placeholder_text="Wpisz odpowiedź A:",
                                            border_color=ACCENT, border_width=1, text_color=TEXT)
        master.option_input1.pack(pady=10, fill="x", padx=50)
        master.option_input1.insert(0, data.get("opcje", {}).get("A", ""))

        master.option_input2 = ctk.CTkEntry(master.answers_label_frame, fg_color=BG_CARD, height=50,
                                            font=("Arial", 28, "bold"), placeholder_text="Wpisz odpowiedź B:",
                                            border_color=ACCENT, border_width=1, text_color=TEXT)
        master.option_input2.pack(pady=10, fill="x", padx=50)
        master.option_input2.insert(0, data.get("opcje", {}).get("B", ""))

        master.option_input3 = ctk.CTkEntry(master.answers_label_frame, fg_color=BG_CARD, height=50,
                                            font=("Arial", 28, "bold"), placeholder_text="Wpisz odpowiedź C:",
                                            border_color=ACCENT, border_width=1, text_color=TEXT)
        master.option_input3.pack(pady=10, fill="x", padx=50)
        master.option_input3.insert(0, data.get("opcje", {}).get("C", ""))

        master.option_input4 = ctk.CTkEntry(master.answers_label_frame, fg_color=BG_CARD, height=50,
                                            font=("Arial", 28, "bold"), placeholder_text="Wpisz odpowiedź D:",
                                            border_color=ACCENT, border_width=1, text_color=TEXT)
        master.option_input4.pack(pady=10, fill="x", padx=50)
        master.option_input4.insert(0, data.get("opcje", {}).get("D", ""))

        master.correct_option_label = ctk.CTkButton(master.answers_label_frame, fg_color=BG_CARD,
                                                    font=("Arial", 28, "bold"), text="Edytuj poprawną odpowiedź",
                                                    width=325, height=55, text_color_disabled=TEXT_DIM, state="disabled",
                                                    text_color=ACCENT_WARN)
        master.correct_option_label.pack(pady=10, side="top", padx=50)

        master.correct_option = ctk.CTkEntry(master.answers_label_frame, fg_color=BG_CARD, height=50,
                                             font=("Arial", 28, "bold"),
                                             placeholder_text="Wpisz poprawną odpowiedź czyli: A/B/C/D",
                                             border_color=ACCENT_SUCCESS, border_width=1, text_color=TEXT)
        master.correct_option.pack(pady=10, fill="x", padx=50)
        master.correct_option.insert(0, data.get("poprawna", ""))

        master.button_submit_addition = ctk.CTkButton(master.answers_label_frame, fg_color=BG_FRAME,
                                                      text="Zapisz Zmiany", width=325, height=80,
                                                      font=("Arial", 28, "bold"),
                                                      hover_color=ACCENT_WARN,
                                                      text_color=ACCENT_WARN,
                                                      border_width=1,
                                                      border_color=ACCENT_WARN,
                                                      command=lambda: save_command("zamkniete"))
        master.button_submit_addition.pack(pady=30, padx=50)
        master.question_input.focus_set()

    def add_question_open_menu(self, master, save_command):
        self.nothing(master)

        master.total_questions_label = ctk.CTkLabel(
            master,
            text=f"Suma pytań w tym teście: {len(master.dane)}",
            font=("Arial", 22, "bold"),
            text_color=TEXT
        )
        master.total_questions_label.pack(pady=(20, 0))

        self.go_back_to_edit_menu_btn(master)

        master.add_question_open_frame = ctk.CTkFrame(master, fg_color=BG_FRAME, width=1200, height=850,
                                                      corner_radius=12)
        master.add_question_open_frame.pack_propagate(False)
        master.add_question_open_frame.place(relx=0.5, rely=0.4, anchor="center")
        master.add_question_open_frame.pack(pady=60, padx=10)

        master.add_question_closed_label = ctk.CTkButton(master.add_question_open_frame, fg_color=BG_CARD,
                                                         text="Wprowadź pytanie otwarte", width=325, height=50,
                                                         font=("Arial", 28, "bold"),
                                                         state="disabled", text_color_disabled=TEXT_DIM,
                                                         text_color=TEXT)
        master.add_question_closed_label.pack(pady=(150, 20), padx=50, side="top")

        master.input_answer = ctk.CTkEntry(master.add_question_open_frame, fg_color=BG_CARD, height=50,
                                           font=("Arial", 28, "bold"), placeholder_text="Wprowadź tu pytanie",
                                           width=1000, border_color=ACCENT, border_width=1, text_color=TEXT)
        master.input_answer.pack(pady=(1, 50), padx=20)

        master.input_answer_correct_label = ctk.CTkButton(master.add_question_open_frame, fg_color=BG_CARD,
                                                          text="Wprowadź klucz odpowiedzi", width=325, height=50,
                                                          font=("Arial", 28, "bold"),
                                                          state="disabled", text_color_disabled=TEXT_DIM,
                                                          text_color=TEXT)
        master.input_answer_correct_label.pack(pady=(1, 20), padx=50, side="top")

        master.input_answer_correct = ctk.CTkEntry(master.add_question_open_frame, fg_color=BG_CARD, height=50,
                                                   font=("Arial", 28, "bold"),
                                                   placeholder_text="Wprowadź tu klucz odpowiedzi",
                                                   width=1000, border_color=ACCENT_SUCCESS, border_width=1,
                                                   text_color=TEXT)
        master.input_answer_correct.pack(pady=(1, 20), side="top")
        master.submit_button = ctk.CTkButton(master.add_question_open_frame, fg_color=BG_MAIN,
                                             text="Commit changes",
                                             width=325, height=80, font=("Arial", 28, "bold"),
                                             hover_color=ACCENT_SUCCESS,
                                             text_color=ACCENT_SUCCESS,
                                             border_width=1,
                                             border_color=ACCENT_SUCCESS,
                                             command=lambda: save_command("otwarte"))
        master.submit_button.pack(pady=(80, 140), padx=50, side="bottom")
        master.input_answer.focus_set()

    def edit_question_open_menu(self, master, save_command, data):
        self.nothing(master)

        master.total_questions_label = ctk.CTkLabel(
            master,
            text=f"Edytujesz pytanie z testu ({len(master.dane)} pytań ogółem)",
            font=("Arial", 22, "bold"),
            text_color=TEXT
        )
        master.total_questions_label.pack(pady=(20, 0))

        master.go_back_to_list_btn = ctk.CTkButton(master, text="Powrót do listy pytań", font=("Arial", 18, "bold"),
                                                   command=master.start_change_question, height=50,
                                                   width=200,
                                                   fg_color=BG_FRAME,
                                                   hover_color=ACCENT_SUCCESS,
                                                   text_color=TEXT,
                                                   border_width=1,
                                                   border_color=ACCENT_SUCCESS)
        master.go_back_to_list_btn.pack(pady=40, side="bottom", padx=50)

        master.edit_question_open_frame = ctk.CTkFrame(master, fg_color=BG_FRAME, width=1200, height=850,
                                                       corner_radius=12)
        master.edit_question_open_frame.pack_propagate(False)
        master.edit_question_open_frame.place(relx=0.5, rely=0.4, anchor="center")
        master.edit_question_open_frame.pack(pady=60, padx=10)

        master.add_question_closed_label = ctk.CTkButton(master.edit_question_open_frame, fg_color=BG_CARD,
                                                         text="Edytuj pytanie otwarte", width=325, height=50,
                                                         font=("Arial", 28, "bold"),
                                                         state="disabled", text_color_disabled=TEXT_DIM,
                                                         text_color=ACCENT_WARN)
        master.add_question_closed_label.pack(pady=(150, 20), padx=50, side="top")

        master.input_answer = ctk.CTkEntry(master.edit_question_open_frame, fg_color=BG_CARD, height=50,
                                           font=("Arial", 28, "bold"), placeholder_text="Wprowadź tu pytanie",
                                           width=1000, border_color=ACCENT_WARN, border_width=1, text_color=TEXT)
        master.input_answer.pack(pady=(1, 50), padx=20)
        master.input_answer.insert(0, data.get("pytanie", ""))

        master.input_answer_correct_label = ctk.CTkButton(master.edit_question_open_frame, fg_color=BG_CARD,
                                                          text="Edytuj klucz odpowiedzi", width=325, height=50,
                                                          font=("Arial", 28, "bold"),
                                                          state="disabled", text_color_disabled=TEXT_DIM,
                                                          text_color=ACCENT_WARN)
        master.input_answer_correct_label.pack(pady=(1, 20), padx=50, side="top")

        master.input_answer_correct = ctk.CTkEntry(master.edit_question_open_frame, fg_color=BG_CARD, height=50,
                                                   font=("Arial", 28, "bold"),
                                                   placeholder_text="Wprowadź tu klucz odpowiedzi",
                                                   width=1000, border_color=ACCENT_SUCCESS, border_width=1,
                                                   text_color=TEXT)
        master.input_answer_correct.pack(pady=(1, 20), side="top")
        master.input_answer_correct.insert(0, data.get("poprawna", ""))

        master.submit_button = ctk.CTkButton(master.edit_question_open_frame, fg_color=BG_MAIN,
                                             text="Zapisz Zmiany",
                                             width=325, height=80, font=("Arial", 28, "bold"),
                                             hover_color=ACCENT_WARN,
                                             text_color=ACCENT_WARN,
                                             border_width=1,
                                             border_color=ACCENT_WARN,
                                             command=lambda: save_command("otwarte"))
        master.submit_button.pack(pady=(80, 140), padx=50, side="bottom")
        master.input_answer.focus_set()

    def change_question_menu(self, master):
        self.nothing(master)

        master.total_questions_label = ctk.CTkLabel(
            master,
            text=f"Suma pytań w tym teście: {len(master.dane)}",
            font=("Arial", 22, "bold"),
            text_color=TEXT
        )
        master.total_questions_label.pack(pady=(20, 0))

        self.go_back_to_edit_menu_btn(master)

        master.change_question_frame = ctk.CTkFrame(master, fg_color=BG_FRAME, width=1200, height=700,
                                                    corner_radius=12)
        master.change_question_frame.pack(pady=20, padx=20, fill="both", expand=True)

        master.change_question_button_label = ctk.CTkLabel(
            master.change_question_frame,
            text="Lista pytań (Zmień lub usuń):",
            font=("Arial", 20, "bold"),
            text_color=TEXT
        )
        master.change_question_button_label.pack(pady=10)

        master.search_question_entry = ctk.CTkEntry(master.change_question_frame, fg_color=BG_CARD,
                                                    width=500,
                                                    placeholder_text="Wyszukaj pytania",
                                                    placeholder_text_color=TEXT_DIM,
                                                    font=("Arial", 20, "bold"), text_color=TEXT,
                                                    border_color=ACCENT, border_width=1)
        master.search_question_entry.pack(pady=10, padx=10)

        master.change_question_scrollable_frame = ctk.CTkScrollableFrame(
            master.change_question_frame,
            fg_color="transparent",
            width=1100,
            height=500,
            scrollbar_button_color=ACCENT,
            scrollbar_button_hover_color=BG_CARD
        )
        master.change_question_scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

    def delete_or_change_question_menu(self, master):
        self.nothing(master)
        self.go_back_to_edit_menu_btn(master)

        self.delete_or_change_frame = ctk.CTkFrame(master, fg_color="transparent", width=1200, height=700)
        self.delete_or_change_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def go_back_to_edit_menu_btn(self, master):
        master.go_back_to_edit_menu_btn = ctk.CTkButton(master, text="Powrót", font=("Arial", 18, "bold"),
                                                        command=lambda: self.show_edit_menu(master), height=50,
                                                        width=200,
                                                        fg_color=BG_FRAME,
                                                        hover_color=ACCENT_SUCCESS,
                                                        text_color=TEXT,
                                                        border_width=1,
                                                        border_color=ACCENT_SUCCESS)
        master.go_back_to_edit_menu_btn.pack(pady=40, side="bottom", padx=50)

    def show_last_results_menu(self, master, najgorsze, najlepsze):
        self.nothing(master)
        master.total_questions_label = ctk.CTkLabel(
            master,
            text="Podsumowanie wyników i postępów w nauce",
            font=("Arial", 28, "bold"),
            text_color=TEXT
        )
        master.total_questions_label.pack(pady=(20, 0))
        self.go_back_to_edit_menu_btn(master)
        master.last_results_frame = ctk.CTkScrollableFrame(master, fg_color=BG_FRAME, width=1200, height=750,
                                                           scrollbar_button_color=ACCENT,
                                                           scrollbar_button_hover_color=BG_CARD)
        master.last_results_frame.pack(pady=20, padx=20, fill="both", expand=True)
        lbl_bledy = ctk.CTkLabel(master.last_results_frame, text="Błędy z ostatniego podejścia w tej sesji:",
                                 font=("Arial", 22, "bold"), text_color=ACCENT_ERROR)
        lbl_bledy.pack(pady=(10, 5), anchor="w", padx=20)
        if not master.bledy:
            brak = ctk.CTkLabel(master.last_results_frame,
                                text="Albo jeszcze żeś nie zrobił testu alboś jest niesamowity i wszystko dobrze masz",
                                font=("Arial", 16), text_color=TEXT_DIM)
            brak.pack(pady=10, anchor="w", padx=40)
        else:
            for i, blad in enumerate(master.bledy):
                ramka = ctk.CTkFrame(master.last_results_frame, fg_color=BG_CARD, corner_radius=8)
                ramka.pack(pady=5, padx=20, fill="x")
                pyt = ctk.CTkLabel(ramka, text=f"{i + 1}. {blad['pytanie']}", font=("Arial", 16, "bold"),
                                   justify="left", wraplength=1000, text_color=TEXT)
                pyt.pack(anchor="w", padx=10, pady=(5, 2))
                tw = ctk.CTkLabel(ramka, text=f"Twoja odpowiedź: {blad['twoja']}", font=("Arial", 14),
                                  text_color=ACCENT_ERROR)
                tw.pack(anchor="w", padx=20)
                po = ctk.CTkLabel(ramka, text=f"Poprawna odpowiedź: {blad['poprawna']}", font=("Arial", 14, "bold"),
                                  text_color=ACCENT_SUCCESS)
                po.pack(anchor="w", padx=20, pady=(0, 5))
                self._renderuj_ai_przy_bledzie(master, ramka, blad)
        sep1 = ctk.CTkFrame(master.last_results_frame, height=2, fg_color=BG_CARD)
        sep1.pack(fill="x", padx=40, pady=30)
        lbl_najgorsze = ctk.CTkLabel(master.last_results_frame, text="Najgorzej opanowane pytania:",
                                     font=("Arial", 22, "bold"), text_color=ACCENT_ERROR)
        lbl_najgorsze.pack(pady=(10, 5), anchor="w", padx=20)
        if not najgorsze:
            ctk.CTkLabel(master.last_results_frame, text="Baza pytań jest pusta.",
                         text_color=TEXT_DIM).pack(anchor="w", padx=40)
        else:
            for q in najgorsze:
                tresc = q.get("pytanie", "Brak treści")
                licznik = q.get("licznik", 0)
                lbl = ctk.CTkLabel(master.last_results_frame, text=f"• [Postęp: {licznik}] {tresc}",
                                   font=("Arial", 16), justify="left", wraplength=1000, text_color=TEXT)
                lbl.pack(anchor="w", padx=40, pady=2)
        sep2 = ctk.CTkFrame(master.last_results_frame, height=2, fg_color=BG_CARD)
        sep2.pack(fill="x", padx=40, pady=30)
        lbl_najlepsze = ctk.CTkLabel(master.last_results_frame, text="Najlepiej opanowane pytania:",
                                     font=("Arial", 22, "bold"), text_color=ACCENT_SUCCESS)
        lbl_najlepsze.pack(pady=(10, 5), anchor="w", padx=20)
        if not najlepsze:
            ctk.CTkLabel(master.last_results_frame, text="Baza pytań jest pusta.",
                         text_color=TEXT_DIM).pack(anchor="w", padx=40)
        else:
            for q in najlepsze:
                tresc = q.get("pytanie", "Brak treści")
                licznik = q.get("licznik", 0)
                lbl = ctk.CTkLabel(master.last_results_frame, text=f"• [Postęp: {licznik}] {tresc}",
                                   font=("Arial", 16), justify="left", wraplength=1000, text_color=TEXT)
                lbl.pack(anchor="w", padx=40, pady=2)

    def _renderuj_ai_przy_bledzie(self, master, rodzic_frame, blad):
        ai_dolny_frame = ctk.CTkFrame(rodzic_frame, fg_color="transparent")
        ai_dolny_frame.pack(fill="x", padx=14, pady=(0, 10))

        ai_box = ctk.CTkTextbox(ai_dolny_frame,
                                height=90,
                                font=("Arial", 16),
                                fg_color=BG_FRAME,
                                text_color=TEXT,
                                border_width=1,
                                border_color=ACCENT_AI,
                                wrap="word",
                                state="disabled")
        ai_btn_ref = [None]

        def wyjasnij(b=blad, box=ai_box, btn_lista=ai_btn_ref):
            prompt = zbuduj_prompt_blad(b['pytanie'], b['twoja'], b['poprawna'])
            box.pack(fill="x", pady=(6, 0))
            btn_lista[0].configure(state="disabled", text="⏳ Generuję...")

            accumulated = [""]

            def on_chunk(token):
                accumulated[0] += token
                def update():
                    box.configure(state="normal")
                    box.delete("1.0", "end")
                    box.insert("end", accumulated[0])
                    box.see("end")
                    box.configure(state="disabled")
                master.after(0, update)

            def on_done():
                def enable():
                    btn_lista[0].configure(state="normal", text="✦ Wyjaśnij AI")
                master.after(0, enable)

            def on_error(msg):
                def show_err():
                    box.configure(state="normal")
                    box.delete("1.0", "end")
                    box.insert("end", f"❌ {msg}")
                    box.configure(state="disabled")
                    btn_lista[0].configure(state="normal", text="✦ Wyjaśnij AI")
                master.after(0, show_err)

            zapytaj_ollame(prompt, on_chunk, on_done, on_error)

        ai_btn = ctk.CTkButton(ai_dolny_frame,
                               text="✦ Wyjaśnij AI",
                               font=("Arial", 16, "bold"),
                               fg_color="transparent",
                               hover_color=BG_FRAME,
                               text_color=ACCENT_AI,
                               border_width=1,
                               border_color=ACCENT_AI,
                               height=30,
                               width=130,
                               command=wyjasnij)
        ai_btn.pack(side="left")
        ai_btn_ref[0] = ai_btn