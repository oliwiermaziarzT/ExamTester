import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class QuizUI:
    def setup_ui(self, master, buttons_command_closed, button_command_open):
        # UI

        # progressbar
        master.progressbar = ctk.CTkProgressBar(master, orientation="horizontal", width=600, height=20)
        master.progressbar.set(0)
        master.progressbar.pack(pady=30, side="top")
        # ilosc pytan pod progressbarem
        master.pytania_label = ctk.CTkLabel(master, text="", font=("Arial", 18, "bold"), text_color="yellow")
        master.pytania_label.pack(pady=10)
        # wyswietlanie pytania
        master.pytanie = ctk.CTkLabel(master, text="", font=("Arial", 18, "bold"), wraplength=1000)
        master.pytanie.pack(pady=10)
        # ramka na przyciski
        master.buttons_frame = ctk.CTkFrame(master, fg_color="transparent")
        # przyciski
        master.buttons = {}
        for litera in ["A", "B", "C", "D"]:
            btn = ctk.CTkButton(master.buttons_frame,
                                text=litera,
                                width=400,
                                height=50,
                                font=("Arial", 18, "bold"),
                                command=lambda l=litera: buttons_command_closed(l), text_color="black")
            btn.pack(pady=10)
            master.buttons[litera] = btn
        # frame na pytanie otwarte
        master.open_question_frame = ctk.CTkFrame(master, fg_color="transparent")
        # pole na odpowiedz na pytanie otwarte
        master.answer_entry = ctk.CTkEntry(master.open_question_frame,
                                           width=400,
                                           height=50,
                                           font=("Arial", 18),
                                           placeholder_text="Wpisz odpowiedź tutaj...")
        master.answer_entry.pack(pady=10)
        # przycisk na submita odpowiedzi
        master.submit_open_btn = ctk.CTkButton(master.open_question_frame,
                                               text="Sprawdź odpowiedź",
                                               width=200,
                                               height=50,
                                               font=("Arial", 18, "bold"),
                                               fg_color="orange",
                                               command=button_command_open)
        master.submit_open_btn.pack(pady=10)
        # wyswieltanie prawidlowego rezultatu
        master.correct_answer_display = ctk.CTkLabel(master.open_question_frame,
                                                     text="",
                                                     font=("Arial", 18, "bold"),
                                                     text_color="green")

        # statystyki na samym dole
        master.footer_frame = ctk.CTkFrame(master)
        master.footer_frame.pack(side="bottom", fill="x", pady=20)
        # tworzenie frame grida
        for i in range(5):
            master.footer_frame.grid_columnconfigure(i, weight=1)

        # naglowki
        # label na poprawne odpowiedzi
        master.poprawne_label = ctk.CTkLabel(master.footer_frame, text="Poprawne", font=("Arial", 24, "bold"),
                                             text_color="green")
        master.poprawne_label.grid(row=0, column=0, sticky="nsew")
        # label na nauczone pytania
        master.nauczone_label = ctk.CTkLabel(master.footer_frame, text="Nauczone", font=("Arial", 24, "bold"))
        master.nauczone_label.grid(row=0, column=1, sticky="nsew")
        # label na procenty poprawnych odpowiedzi (poprawne/poprawne+niepoprawne)
        master.procent_label = ctk.CTkLabel(master.footer_frame, text="Procent", font=("Arial", 24, "bold"))
        master.procent_label.grid(row=0, column=2, sticky="nsew")
        # label na niepoprawne odpowiedzi
        master.niepoprawne_label = ctk.CTkLabel(master.footer_frame, text="Niepoprawne", font=("Arial", 24, "bold"),
                                                text_color="red")
        master.niepoprawne_label.grid(row=0, column=3, sticky="nsew")
        # label na niepoprawne odpowiedzi
        master.nienauczone_label = ctk.CTkLabel(master.footer_frame, text="Nienauczone", font=("Arial", 24, "bold"))
        master.nienauczone_label.grid(row=0, column=4, sticky="nsew")

        # grid wartosci statystyk
        master.poprawne_label_num = ctk.CTkLabel(master.footer_frame, text="0", font=("Arial", 24, "bold"))
        master.poprawne_label_num.grid(row=1, column=0, sticky="nsew")
        # wartosci nauczonych odpowiedzi
        master.nauczone_num = ctk.CTkLabel(master.footer_frame, text="0", font=("Arial", 24, "bold"))
        master.nauczone_num.grid(row=1, column=1, sticky="nsew")
        # wartosci procentowe odpowiedzi poprawnych
        master.procent_label_num = ctk.CTkLabel(master.footer_frame, text="0%", font=("Arial", 24, "bold"))
        master.procent_label_num.grid(row=1, column=2, sticky="nsew")
        # wartosc niepoprawnych odpowiedzi
        master.niepoprawne_label_num = ctk.CTkLabel(master.footer_frame, text="0", font=("Arial", 24, "bold"))
        master.niepoprawne_label_num.grid(row=1, column=3, sticky="nsew")
        # wartosc nienauczonych odpowiedzi
        master.nienauczone_num = ctk.CTkLabel(master.footer_frame, text="0", font=("Arial", 24, "bold"))
        master.nienauczone_num.grid(row=1, column=4, sticky="nsew")

        self.setup_restart_buttons(master)

    def setup_restart_buttons(self, master):
        master.button_restart_frame = ctk.CTkFrame(master, fg_color="transparent")
        master.button_restart_frame.pack(pady=20, side="bottom")

        master.button_hard_restart = ctk.CTkButton(master.button_restart_frame,
                                                   text="Zresetuj wszystko i zacznij od nowa",
                                                   font=("Arial", 28, "bold"),
                                                   command=master.restart_test_hard,
                                                   fg_color="#1e4469",
                                                   hover_color="#8B0000")
        master.button_hard_restart.pack(side="bottom", pady=10)

        master.button_restart = ctk.CTkButton(master.button_restart_frame,
                                              text="Zacznij od nowa",
                                              font=("Arial", 28, "bold"),
                                              command=master.restart_test,
                                              fg_color="#1e4469",
                                              hover_color="#B8860B",
                                              text_color="white")
        master.button_restart.pack(side="top", pady=10)

    def back_to_menu(self, master, button_command):
        master.button_go_back_to_menu_frame = ctk.CTkFrame(master, fg_color="transparent")

        master.button_go_back_to_menu = ctk.CTkButton(master.button_go_back_to_menu_frame,
                                                      text="Wróć do menu",
                                                      font=("Arial", 28, "bold"),
                                                      command=button_command,
                                                      width=300,
                                                      height=60,
                                                      fg_color="green")
        master.button_go_back_to_menu.pack(side="bottom", pady=30)

    def setup_menu(self, master, button_command):
        if not hasattr(master, 'menu_button_frame'):
            master.menu_button_frame = ctk.CTkFrame(master, fg_color="transparent")

            master.menu_start_button = ctk.CTkButton(
                master.menu_button_frame,
                text="Rozpocznij Test",
                font=("Arial", 18, "bold"),
                command=button_command,
                width=600,
                height=60
            )

        master.signature_label = ctk.CTkLabel(master, fg_color="transparent",
                                              text="Exam tester made by Oliwier Maziarz")
        master.signature_label.pack(pady=20, side="bottom")

    def add_test_button(self, master, button_command):
        master.add_test_button_frame = ctk.CTkFrame(master, fg_color="transparent")
        master.add_test_button_frame.pack(pady=20, side="top")

        master.add_test_button = ctk.CTkButton(master.add_test_button_frame, text="Dodaj test",
                                               font=("Arial", 18, "bold"), command=button_command, width=600, height=60)
        master.add_test_button.pack(pady=20, side="top")

    def scrollable_tests_frame(self, master):
        master.new_test_names = []

        master.new_tests_frame = ctk.CTkScrollableFrame(master, fg_color="#303030", width=800, height=800)
        master.new_tests_frame.pack(pady=20, side="top")

        master.new_tests_line_frame = ctk.CTkFrame(master.new_tests_frame, fg_color="transparent")
        master.new_tests_line_frame.pack(pady=20, side="bottom")

    def show_closed_question(self, master):
        master.open_question_frame.pack_forget()
        master.buttons_frame.pack(pady=20)

    def show_open_question(self, master):
        master.buttons_frame.pack_forget()
        master.open_question_frame.pack(pady=20)
        master.correct_answer_display.pack_forget()
        master.answer_entry.configure(state="normal")
        master.answer_entry.delete(0, "end")
        master.answer_entry.configure(fg_color=["#F9F9FA", "#343638"], text_color=["black", "white"])
        master.submit_open_btn.configure(state="normal")
        master.answer_entry.focus_set()

    def show_koniec_testu(self, master, final_procent):
        master.pytania_label.configure(text="Koniec testu!")
        master.procent_label_num.configure(text=f"{final_procent}%")
        master.pytanie.configure(text="Wybierz opcję na dole ekranu")
        master.buttons_frame.pack_forget()
        master.open_question_frame.pack_forget()
        master.progressbar.set(1)

        if not hasattr(master, 'show_bledy_btn'):
            master.show_bledy_btn = ctk.CTkButton(master, text="Przejrzyj błędy", font=("Arial", 28, "bold"),
                                                  command=lambda: self.show_bledy(master), fg_color="#eb8383",
                                                  width=300, height=60)

        if len(master.bledy) > 0:
            master.show_bledy_btn.pack(pady=20)

    def show_bledy(self, master):
        self.nothing(master)
        master.footer_frame.pack(side="bottom", fill="x", pady=20)
        master.button_restart_frame.pack(pady=20, side="bottom")
        master.button_go_back_to_menu_frame.pack(side="bottom", pady=30)

        if not hasattr(master, 'bledy_frame'):
            master.bledy_frame = ctk.CTkScrollableFrame(master, fg_color="#303030")
        else:
            for widget in master.bledy_frame.winfo_children():
                widget.destroy()

        master.bledy_frame.pack(pady=20, padx=20, fill="both", expand=True)

        for i, blad in enumerate(master.bledy):
            pojedynczy_blad_frame = ctk.CTkFrame(master.bledy_frame, fg_color="transparent")
            pojedynczy_blad_frame.pack(pady=15, padx=10, fill="x")

            pytanie_label = ctk.CTkLabel(
                pojedynczy_blad_frame,
                text=f"{i + 1}. {blad['pytanie']}",
                font=("Arial", 18, "bold"),
                text_color="white",
                justify="left",
                anchor="w"
            )
            pytanie_label.pack(anchor="w")

            twoja_label = ctk.CTkLabel(
                pojedynczy_blad_frame,
                text=f"Twoja odpowiedź: {blad['twoja']}",
                font=("Arial", 16),
                text_color="#eb8383",
                justify="left",
                anchor="w"
            )
            twoja_label.pack(anchor="w", padx=20)

            poprawna_label = ctk.CTkLabel(
                pojedynczy_blad_frame,
                text=f"Poprawna odpowiedź: {blad['poprawna']}",
                font=("Arial", 16, "bold"),
                text_color="#72bd7e",
                justify="left",
                anchor="w"
            )
            poprawna_label.pack(anchor="w", padx=20)

            linia = ctk.CTkFrame(master.bledy_frame, height=2, fg_color="#404040")
            linia.pack(fill="x", padx=50, pady=5)

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
            "last_results_frame"
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
            text_color="white"
        )
        master.total_questions_label.pack(pady=(20, 0))

        master.action_buttons_frame = ctk.CTkFrame(master, fg_color="transparent")
        master.action_buttons_frame.pack(pady=20, side="top", fill="x", padx=50)

        btn_height = 80
        btn_width = 200
        btn_color = "#3c86c3"

        master.btn_add_closed = ctk.CTkButton(
            master.action_buttons_frame,
            text="Dodaj pytanie zamkniete",
            fg_color=btn_color,
            font=("Arial", 18, "bold"),
            height=btn_height,
            width=btn_width,
            command=master.start_add_question_closed,
        )
        master.btn_add_closed.pack(side="left", fill="x", expand=True, padx=15)
        master.btn_change = ctk.CTkButton(
            master.action_buttons_frame,
            text="Zmień lub usuń pytanie",
            fg_color=btn_color,
            font=("Arial", 18, "bold"),
            height=btn_height,
            width=btn_width,
            command=master.start_change_question,
        )
        master.btn_change.pack(side="left", fill="x", expand=True, padx=15)
        master.btn_add_open = ctk.CTkButton(
            master.action_buttons_frame,
            text="Dodaj pytanie otwarte",
            fg_color=btn_color,
            font=("Arial", 18, "bold"),
            height=btn_height,
            width=btn_width,
            command=master.start_add_question_open,

        )
        master.btn_add_open.pack(side="left", fill="x", expand=True, padx=15)
        master.button_go_back_to_menu_frame.pack(side="bottom", pady=20)


        master.stats_frame = ctk.CTkFrame(master, fg_color="transparent")
        master.stats_frame.pack(pady=10, fill="x", padx=50)

        total = len(master.dane)
        otwarte = sum(1 for q in master.dane if q.get("typ") == "otwarte")
        zamkniete = total - otwarte
        nauczone = sum(1 for q in master.dane if q.get("licznik", 0) > 2)
        nienauczone = total - nauczone

        stats_text = f"Otwarte: {otwarte} | Zamknięte: {zamkniete}   ---   Nauczone: {nauczone} | Nienauczone: {nienauczone}"
        master.stats_label = ctk.CTkLabel(master.stats_frame, text=stats_text, font=("Arial", 18, "bold"),
                                          text_color="#2ecc71")
        master.stats_label.pack(pady=5)

        if total > 0:
            master.fig_stats, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5), facecolor='#303030',
                                                        constrained_layout=True)
            master.fig_stats.patch.set_facecolor('#242424')

            ax1.pie([otwarte, zamkniete] if otwarte or zamkniete else [1],
                    labels=['Otwarte', 'Zamknięte'] if otwarte or zamkniete else ['Brak'],
                    autopct='%1.1f%%' if otwarte or zamkniete else '',
                    colors=['#3B8ED0', '#eb8383'], textprops={'color': "white"})
            ax1.set_title("Typy pytań", color="white")

            ax2.pie([nauczone, nienauczone] if nauczone or nienauczone else [1],
                    labels=['Nauczone', 'Nienauczone'] if nauczone or nienauczone else ['Brak'],
                    autopct='%1.1f%%' if nauczone or nienauczone else '',
                    colors=['#2ecc71', '#e74c3c'], textprops={'color': "white"})
            ax2.set_title("Postęp nauki", color="white")

            master.canvas = FigureCanvasTkAgg(master.fig_stats, master.stats_frame)
            master.canvas.draw()
            master.canvas.get_tk_widget().pack(pady=10)
            master.last_results_btn = ctk.CTkButton(
                master.stats_frame,
                text="Ostatnie rezultaty i statystyki pytań",
                font=("Arial", 18, "bold"),
                fg_color="#e67e22",
                hover_color="#d35400",
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
            text_color="white"
        )
        master.total_questions_label.pack(pady=(20, 0))

        self.go_back_to_edit_menu_btn(master)

        master.add_question_menu_frame = ctk.CTkFrame(master, fg_color="#303030")
        master.add_question_menu_frame.pack(pady=50, fill="x", padx=50)

        master.question_label_frame = ctk.CTkFrame(master.add_question_menu_frame, fg_color="transparent",
                                                   corner_radius=20)
        master.question_label_frame.pack(pady=5, side="top", fill="x", padx=50)

        master.question_label = ctk.CTkButton(master.question_label_frame, fg_color="#3c86c3",
                                              font=("Arial", 28, "bold"), text="Wprowadź pytanie zamknięte", width=325,
                                              height=55, text_color_disabled="black", state="disabled")
        master.question_label.pack(pady=20, side="top", padx=50)

        master.question_input = ctk.CTkEntry(master.question_label_frame, fg_color="#6c5d48", height=50,
                                             font=("Arial", 28, "bold"), placeholder_text="Wprowadź Pytanie")
        master.question_input.pack(pady=10, fill="x", padx=50)

        master.answers_label_frame = ctk.CTkFrame(master.add_question_menu_frame, fg_color="transparent",
                                                  corner_radius=20)
        master.answers_label_frame.pack(pady=5, side="top", padx=50, fill="x")

        master.question_label = ctk.CTkButton(master.answers_label_frame, fg_color="#3c86c3",
                                              font=("Arial", 28, "bold"), text="Wprowadź odpowiedzi", width=325,
                                              height=55,
                                              text_color_disabled="black", state="disabled")
        master.question_label.pack(pady=10, side="top", padx=50)

        master.option_input1 = ctk.CTkEntry(master.answers_label_frame, fg_color="#6c5d48", height=50,
                                            font=("Arial", 28, "bold"), placeholder_text="Wpisz odpowiedź A:")
        master.option_input1.pack(pady=10, fill="x", padx=50)

        master.option_input2 = ctk.CTkEntry(master.answers_label_frame, fg_color="#6c5d48", height=50,
                                            font=("Arial", 28, "bold"), placeholder_text="Wpisz odpowiedź B:")
        master.option_input2.pack(pady=10, fill="x", padx=50)

        master.option_input3 = ctk.CTkEntry(master.answers_label_frame, fg_color="#6c5d48", height=50,
                                            font=("Arial", 28, "bold"), placeholder_text="Wpisz odpowiedź C:")
        master.option_input3.pack(pady=10, fill="x", padx=50)

        master.option_input4 = ctk.CTkEntry(master.answers_label_frame, fg_color="#6c5d48", height=50,
                                            font=("Arial", 28, "bold"), placeholder_text="Wpisz odpowiedź D:")
        master.option_input4.pack(pady=10, fill="x", padx=50)

        master.correct_option_label = ctk.CTkButton(master.answers_label_frame, fg_color="#3c86c3",
                                                    font=("Arial", 28, "bold"), text="Wprowadź poprawną odpowiedź",
                                                    width=325, height=55,
                                                    text_color_disabled="black", state="disabled")
        master.correct_option_label.pack(pady=10, side="top", padx=50)

        master.correct_option = ctk.CTkEntry(master.answers_label_frame, fg_color="#6c5d48", height=50,
                                             font=("Arial", 28, "bold"),
                                             placeholder_text="Wpisz poprawną odpowiedź czyli: A/B/C/D")
        master.correct_option.pack(pady=10, fill="x", padx=50)

        master.button_submit_addition = ctk.CTkButton(master.answers_label_frame, fg_color="#eb8383",
                                                      text="Commit changes", width=325, height=80,
                                                      font=("Arial", 28, "bold"),
                                                      command=lambda: save_command("zamkniete"))
        master.button_submit_addition.pack(pady=30, padx=50)
        master.question_input.focus_set()

    def edit_question_closed_menu(self, master, save_command, data):
        self.nothing(master)

        master.total_questions_label = ctk.CTkLabel(
            master,
            text=f"Edytujesz pytanie z testu ({len(master.dane)} pytań ogółem)",
            font=("Arial", 22, "bold"),
            text_color="white"
        )
        master.total_questions_label.pack(pady=(20, 0))

        master.go_back_to_list_btn = ctk.CTkButton(master, text="Powrót do listy pytań", font=("Arial", 18, "bold"),
                                                   command=master.start_change_question, height=50,
                                                   width=200, fg_color="green")
        master.go_back_to_list_btn.pack(pady=40, side="bottom", padx=50)

        master.edit_question_menu_frame = ctk.CTkFrame(master, fg_color="#303030")
        master.edit_question_menu_frame.pack(pady=50, fill="x", padx=50)

        master.question_label_frame = ctk.CTkFrame(master.edit_question_menu_frame, fg_color="transparent",
                                                   corner_radius=20)
        master.question_label_frame.pack(pady=5, side="top", fill="x", padx=50)

        master.question_label = ctk.CTkButton(master.question_label_frame, fg_color="#f39c12",
                                              font=("Arial", 28, "bold"), text="Edytuj pytanie zamknięte", width=325,
                                              height=55, text_color_disabled="black", state="disabled")
        master.question_label.pack(pady=20, side="top", padx=50)

        master.question_input = ctk.CTkEntry(master.question_label_frame, fg_color="#6c5d48", height=50,
                                             font=("Arial", 28, "bold"), placeholder_text="Wprowadź Pytanie")
        master.question_input.pack(pady=10, fill="x", padx=50)
        master.question_input.insert(0, data.get("pytanie", ""))

        master.answers_label_frame = ctk.CTkFrame(master.edit_question_menu_frame, fg_color="transparent",
                                                  corner_radius=20)
        master.answers_label_frame.pack(pady=5, side="top", padx=50, fill="x")

        master.question_label = ctk.CTkButton(master.answers_label_frame, fg_color="#f39c12",
                                              font=("Arial", 28, "bold"), text="Edytuj odpowiedzi", width=325,
                                              height=55, text_color_disabled="black", state="disabled")
        master.question_label.pack(pady=10, side="top", padx=50)

        master.option_input1 = ctk.CTkEntry(master.answers_label_frame, fg_color="#6c5d48", height=50,
                                            font=("Arial", 28, "bold"), placeholder_text="Wpisz odpowiedź A:")
        master.option_input1.pack(pady=10, fill="x", padx=50)
        master.option_input1.insert(0, data.get("opcje", {}).get("A", ""))

        master.option_input2 = ctk.CTkEntry(master.answers_label_frame, fg_color="#6c5d48", height=50,
                                            font=("Arial", 28, "bold"), placeholder_text="Wpisz odpowiedź B:")
        master.option_input2.pack(pady=10, fill="x", padx=50)
        master.option_input2.insert(0, data.get("opcje", {}).get("B", ""))

        master.option_input3 = ctk.CTkEntry(master.answers_label_frame, fg_color="#6c5d48", height=50,
                                            font=("Arial", 28, "bold"), placeholder_text="Wpisz odpowiedź C:")
        master.option_input3.pack(pady=10, fill="x", padx=50)
        master.option_input3.insert(0, data.get("opcje", {}).get("C", ""))

        master.option_input4 = ctk.CTkEntry(master.answers_label_frame, fg_color="#6c5d48", height=50,
                                            font=("Arial", 28, "bold"), placeholder_text="Wpisz odpowiedź D:")
        master.option_input4.pack(pady=10, fill="x", padx=50)
        master.option_input4.insert(0, data.get("opcje", {}).get("D", ""))

        master.correct_option_label = ctk.CTkButton(master.answers_label_frame, fg_color="#f39c12",
                                                    font=("Arial", 28, "bold"), text="Edytuj poprawną odpowiedź",
                                                    width=325, height=55, text_color_disabled="black", state="disabled")
        master.correct_option_label.pack(pady=10, side="top", padx=50)

        master.correct_option = ctk.CTkEntry(master.answers_label_frame, fg_color="#6c5d48", height=50,
                                             font=("Arial", 28, "bold"),
                                             placeholder_text="Wpisz poprawną odpowiedź czyli: A/B/C/D")
        master.correct_option.pack(pady=10, fill="x", padx=50)
        master.correct_option.insert(0, data.get("poprawna", ""))

        master.button_submit_addition = ctk.CTkButton(master.answers_label_frame, fg_color="#eb8383",
                                                      text="Zapisz Zmiany", width=325, height=80,
                                                      font=("Arial", 28, "bold"),
                                                      command=lambda: save_command("zamkniete"))
        master.button_submit_addition.pack(pady=30, padx=50)
        master.question_input.focus_set()

    def add_question_open_menu(self, master, save_command):
        self.nothing(master)

        master.total_questions_label = ctk.CTkLabel(
            master,
            text=f"Suma pytań w tym teście: {len(master.dane)}",
            font=("Arial", 22, "bold"),
            text_color="white"
        )
        master.total_questions_label.pack(pady=(20, 0))

        self.go_back_to_edit_menu_btn(master)

        master.add_question_open_frame = ctk.CTkFrame(master, fg_color="#303030", width=1200, height=850)
        master.add_question_open_frame.pack_propagate(False)
        master.add_question_open_frame.place(relx=0.5, rely=0.4, anchor="center")
        master.add_question_open_frame.pack(pady=60, padx=10)

        master.add_question_closed_label = ctk.CTkButton(master.add_question_open_frame, fg_color="#3c86c3",
                                                         text="Wprowadź pytanie otwarte", width=325, height=50,
                                                         font=("Arial", 28, "bold"),
                                                         state="disabled", text_color_disabled="black")
        master.add_question_closed_label.pack(pady=(150, 20), padx=50, side="top")

        master.input_answer = ctk.CTkEntry(master.add_question_open_frame, fg_color="#6c5d48", height=50,
                                           font=("Arial", 28, "bold"), placeholder_text="Wprowadź tu pytanie",
                                           width=1000)
        master.input_answer.pack(pady=(1, 50), padx=20)

        master.input_answer_correct_label = ctk.CTkButton(master.add_question_open_frame, fg_color="#3c86c3",
                                                          text="Wprowadź klucz odpowiedzi", width=325, height=50,
                                                          font=("Arial", 28, "bold"),
                                                          state="disabled", text_color_disabled="black")
        master.input_answer_correct_label.pack(pady=(1, 20), padx=50, side="top")

        master.input_answer_correct = ctk.CTkEntry(master.add_question_open_frame, fg_color="#6c5d48", height=50,
                                                   font=("Arial", 28, "bold"),
                                                   placeholder_text="Wprowadź tu klucz odpowiedzi", width=1000)
        master.input_answer_correct.pack(pady=(1, 20), side="top")
        master.submit_button = ctk.CTkButton(master.add_question_open_frame, fg_color="#eb8383", text="Commit changes",
                                             width=325, height=80, font=("Arial", 28, "bold"),
                                             command=lambda: save_command("otwarte"))
        master.submit_button.pack(pady=(80, 140), padx=50, side="bottom")
        master.input_answer.focus_set()

    def edit_question_open_menu(self, master, save_command, data):
        self.nothing(master)

        master.total_questions_label = ctk.CTkLabel(
            master,
            text=f"Edytujesz pytanie z testu ({len(master.dane)} pytań ogółem)",
            font=("Arial", 22, "bold"),
            text_color="white"
        )
        master.total_questions_label.pack(pady=(20, 0))

        master.go_back_to_list_btn = ctk.CTkButton(master, text="Powrót do listy pytań", font=("Arial", 18, "bold"),
                                                   command=master.start_change_question, height=50,
                                                   width=200, fg_color="green")
        master.go_back_to_list_btn.pack(pady=40, side="bottom", padx=50)

        master.edit_question_open_frame = ctk.CTkFrame(master, fg_color="#303030", width=1200, height=850)
        master.edit_question_open_frame.pack_propagate(False)
        master.edit_question_open_frame.place(relx=0.5, rely=0.4, anchor="center")
        master.edit_question_open_frame.pack(pady=60, padx=10)

        master.add_question_closed_label = ctk.CTkButton(master.edit_question_open_frame, fg_color="#f39c12",
                                                         text="Edytuj pytanie otwarte", width=325, height=50,
                                                         font=("Arial", 28, "bold"),
                                                         state="disabled", text_color_disabled="black")
        master.add_question_closed_label.pack(pady=(150, 20), padx=50, side="top")

        master.input_answer = ctk.CTkEntry(master.edit_question_open_frame, fg_color="#6c5d48", height=50,
                                           font=("Arial", 28, "bold"), placeholder_text="Wprowadź tu pytanie",
                                           width=1000)
        master.input_answer.pack(pady=(1, 50), padx=20)
        master.input_answer.insert(0, data.get("pytanie", ""))

        master.input_answer_correct_label = ctk.CTkButton(master.edit_question_open_frame, fg_color="#f39c12",
                                                          text="Edytuj klucz odpowiedzi", width=325, height=50,
                                                          font=("Arial", 28, "bold"),
                                                          state="disabled", text_color_disabled="black")
        master.input_answer_correct_label.pack(pady=(1, 20), padx=50, side="top")

        master.input_answer_correct = ctk.CTkEntry(master.edit_question_open_frame, fg_color="#6c5d48", height=50,
                                                   font=("Arial", 28, "bold"),
                                                   placeholder_text="Wprowadź tu klucz odpowiedzi", width=1000)
        master.input_answer_correct.pack(pady=(1, 20), side="top")
        master.input_answer_correct.insert(0, data.get("poprawna", ""))

        master.submit_button = ctk.CTkButton(master.edit_question_open_frame, fg_color="#eb8383", text="Zapisz Zmiany",
                                             width=325, height=80, font=("Arial", 28, "bold"),
                                             command=lambda: save_command("otwarte"))
        master.submit_button.pack(pady=(80, 140), padx=50, side="bottom")
        master.input_answer.focus_set()

    def change_question_menu(self, master):
        self.nothing(master)

        master.total_questions_label = ctk.CTkLabel(
            master,
            text=f"Suma pytań w tym teście: {len(master.dane)}",
            font=("Arial", 22, "bold"),
            text_color="white"
        )
        master.total_questions_label.pack(pady=(20, 0))

        self.go_back_to_edit_menu_btn(master)

        master.change_question_frame = ctk.CTkFrame(master, fg_color="#303030", width=1200, height=700)
        master.change_question_frame.pack(pady=20, padx=20, fill="both", expand=True)

        master.change_question_button_label = ctk.CTkLabel(
            master.change_question_frame,
            text="Lista pytań (Zmień lub usuń):",
            font=("Arial", 20, "bold")
        )
        master.change_question_button_label.pack(pady=10)

        master.search_question_entry = ctk.CTkEntry(master.change_question_frame, fg_color="white",
                                                    width=500,
                                                    placeholder_text="Wyszukaj pytania",
                                                    placeholder_text_color="black",
                                                    font=("Arial", 20, "bold"), text_color="black")
        master.search_question_entry.pack(pady=10, padx=10)

        master.change_question_scrollable_frame = ctk.CTkScrollableFrame(
            master.change_question_frame,
            fg_color="transparent",
            width=1100,
            height=500
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
                                                        width=200, fg_color="green")
        master.go_back_to_edit_menu_btn.pack(pady=40, side="bottom", padx=50)


    def show_last_results_menu(self, master, najgorsze, najlepsze):
        self.nothing(master)
        master.total_questions_label = ctk.CTkLabel(
            master,
            text="Podsumowanie wyników i postępów w nauce",
            font=("Arial", 28, "bold"),
            text_color="white"
        )
        master.total_questions_label.pack(pady=(20, 0))
        self.go_back_to_edit_menu_btn(master)
        master.last_results_frame = ctk.CTkScrollableFrame(master, fg_color="#303030", width=1200, height=750)
        master.last_results_frame.pack(pady=20, padx=20, fill="both", expand=True)
        lbl_bledy = ctk.CTkLabel(master.last_results_frame, text="Błędy z ostatniego podejścia w tej sesji:",
                                 font=("Arial", 22, "bold"), text_color="#eb8383")
        lbl_bledy.pack(pady=(10, 5), anchor="w", padx=20)
        if not master.bledy:
            brak = ctk.CTkLabel(master.last_results_frame,
                                text="Albo jeszcze żeś nie zrobił testu alboś jest niesamowity i wszystko dobrze masz",
                                font=("Arial", 16), text_color="gray")
            brak.pack(pady=10, anchor="w", padx=40)
        else:
            for i, blad in enumerate(master.bledy):
                ramka = ctk.CTkFrame(master.last_results_frame, fg_color="#404040")
                ramka.pack(pady=5, padx=20, fill="x")
                pyt = ctk.CTkLabel(ramka, text=f"{i + 1}. {blad['pytanie']}", font=("Arial", 16, "bold"),
                                   justify="left", wraplength=1000)
                pyt.pack(anchor="w", padx=10, pady=(5, 2))
                tw = ctk.CTkLabel(ramka, text=f"Twoja odpowiedź: {blad['twoja']}", font=("Arial", 14),
                                  text_color="#eb8383")
                tw.pack(anchor="w", padx=20)
                po = ctk.CTkLabel(ramka, text=f"Poprawna odpowiedź: {blad['poprawna']}", font=("Arial", 14, "bold"),
                                  text_color="#2ecc71")
                po.pack(anchor="w", padx=20, pady=(0, 5))
        sep1 = ctk.CTkFrame(master.last_results_frame, height=2, fg_color="#555555")
        sep1.pack(fill="x", padx=40, pady=30)
        lbl_najgorsze = ctk.CTkLabel(master.last_results_frame, text="Najgorzej opanowane pytania:",
                                     font=("Arial", 22, "bold"), text_color="#e74c3c")
        lbl_najgorsze.pack(pady=(10, 5), anchor="w", padx=20)
        if not najgorsze:
            ctk.CTkLabel(master.last_results_frame, text="Baza pytań jest pusta.", text_color="gray").pack(anchor="w",
                                                                                                           padx=40)
        else:
            for q in najgorsze:
                tresc = q.get("pytanie", "Brak treści")
                licznik = q.get("licznik", 0)
                lbl = ctk.CTkLabel(master.last_results_frame, text=f"• [Postęp: {licznik}] {tresc}", font=("Arial", 16),
                                   justify="left", wraplength=1000)
                lbl.pack(anchor="w", padx=40, pady=2)
        sep2 = ctk.CTkFrame(master.last_results_frame, height=2, fg_color="#555555")
        sep2.pack(fill="x", padx=40, pady=30)
        lbl_najlepsze = ctk.CTkLabel(master.last_results_frame, text="Najlepiej opanowane pytania:",
                                     font=("Arial", 22, "bold"), text_color="#2ecc71")
        lbl_najlepsze.pack(pady=(10, 5), anchor="w", padx=20)
        if not najlepsze:
            ctk.CTkLabel(master.last_results_frame, text="Baza pytań jest pusta.", text_color="gray").pack(anchor="w",
                                                                                                           padx=40)
        else:
            for q in najlepsze:
                tresc = q.get("pytanie", "Brak treści")
                licznik = q.get("licznik", 0)
                lbl = ctk.CTkLabel(master.last_results_frame, text=f"• [Postęp: {licznik}] {tresc}", font=("Arial", 16),
                                   justify="left", wraplength=1000)
                lbl.pack(anchor="w", padx=40, pady=2)