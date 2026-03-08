import customtkinter as ctk
from ollama_helper import zapytaj_ollame, zbuduj_prompt_quiz, zbuduj_prompt_blad
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


class QuizUIQuiz:
    def setup_ui(self, master, buttons_command_closed, button_command_open):
        # UI

        # progressbar
        master.progressbar = ctk.CTkProgressBar(master, orientation="horizontal", width=600, height=14,
                                                progress_color=ACCENT, fg_color=BG_FRAME)
        master.progressbar.set(0)
        master.progressbar.pack(pady=30, side="top")
        # ilosc pytan pod progressbarem
        master.pytania_label = ctk.CTkLabel(master, text="", font=("Arial", 18, "bold"), text_color=ACCENT_WARN)
        master.pytania_label.pack(pady=10)
        # wyswietlanie pytania
        master.pytanie = ctk.CTkLabel(master, text="", font=("Arial", 18, "bold"), wraplength=1000, text_color=TEXT)
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
                                command=lambda l=litera: buttons_command_closed(l),
                                text_color=TEXT,
                                fg_color=BG_CARD,
                                hover_color=ACCENT,
                                border_width=1,
                                border_color=BG_CARD)
            btn.pack(pady=6)
            master.buttons[litera] = btn
        # frame na pytanie otwarte
        master.open_question_frame = ctk.CTkFrame(master, fg_color="transparent")
        # pole na odpowiedz na pytanie otwarte
        master.answer_entry = ctk.CTkEntry(master.open_question_frame,
                                           width=400,
                                           height=50,
                                           font=("Arial", 18),
                                           placeholder_text="Wpisz odpowiedź tutaj...",
                                           fg_color=BG_FRAME,
                                           border_color=ACCENT,
                                           border_width=1,
                                           text_color=TEXT)
        master.answer_entry.pack(pady=10)
        # przycisk na submita odpowiedzi
        master.submit_open_btn = ctk.CTkButton(master.open_question_frame,
                                               text="Sprawdź odpowiedź",
                                               width=200,
                                               height=50,
                                               font=("Arial", 18, "bold"),
                                               fg_color=ACCENT_WARN,
                                               hover_color=BG_CARD,
                                               text_color=TEXT,
                                               command=button_command_open)
        master.submit_open_btn.pack(pady=10)
        # wyswieltanie prawidlowego rezultatu
        master.correct_answer_display = ctk.CTkLabel(master.open_question_frame,
                                                     text="",
                                                     font=("Arial", 18, "bold"),
                                                     text_color=ACCENT_SUCCESS)

        # panel AI pomocnika (ukryty domyslnie, pokazuje sie po udzieleniu odpowiedzi)
        master.ai_frame = ctk.CTkFrame(master, fg_color=BG_FRAME, corner_radius=10,
                                       border_width=1, border_color=ACCENT_AI)

        # naglowek panelu AI
        master.ai_header_frame = ctk.CTkFrame(master.ai_frame, fg_color="transparent")
        master.ai_header_frame.pack(fill="x", padx=14, pady=(10, 4))

        master.ai_label = ctk.CTkLabel(master.ai_header_frame, text="✦ Pomocnik AI",
                                       font=("Arial", 14, "bold"), text_color=ACCENT_AI)
        master.ai_label.pack(side="left")

        # pole na wlasny prompt uzytkownika
        master.ai_prompt_entry = ctk.CTkEntry(master.ai_frame,
                                              height=38,
                                              font=("Arial", 14),
                                              placeholder_text="Wpisz pytanie do AI lub kliknij 'Wyjaśnij'...",
                                              fg_color=BG_CARD,
                                              border_color=ACCENT_AI,
                                              border_width=1,
                                              text_color=TEXT)
        master.ai_prompt_entry.pack(fill="x", padx=14, pady=(0, 6))

        # ramka na przyciski AI
        master.ai_buttons_frame = ctk.CTkFrame(master.ai_frame, fg_color="transparent")
        master.ai_buttons_frame.pack(fill="x", padx=14, pady=(0, 6))

        master.ai_explain_btn = ctk.CTkButton(master.ai_buttons_frame,
                                              text="Wyjaśnij odpowiedź",
                                              font=("Arial", 13, "bold"),
                                              fg_color=BG_CARD,
                                              hover_color=ACCENT_AI,
                                              text_color=ACCENT_AI,
                                              border_width=1,
                                              border_color=ACCENT_AI,
                                              height=34,
                                              width=180,
                                              command=lambda: self.ai_wyjasnij_odpowiedz(master))
        master.ai_explain_btn.pack(side="left", padx=(0, 8))

        master.ai_ask_btn = ctk.CTkButton(master.ai_buttons_frame,
                                          text="Wyślij pytanie",
                                          font=("Arial", 13, "bold"),
                                          fg_color=BG_CARD,
                                          hover_color=ACCENT,
                                          text_color=ACCENT,
                                          border_width=1,
                                          border_color=ACCENT,
                                          height=34,
                                          width=140,
                                          command=lambda: self.ai_wyslij_wlasny_prompt(master))
        master.ai_ask_btn.pack(side="left")

        master.ai_clear_btn = ctk.CTkButton(master.ai_buttons_frame,
                                            text="Wyczyść",
                                            font=("Arial", 13),
                                            fg_color="transparent",
                                            hover_color=BG_CARD,
                                            text_color=TEXT_DIM,
                                            border_width=0,
                                            height=34,
                                            width=80,
                                            command=lambda: self.ai_wyczysc(master))
        master.ai_clear_btn.pack(side="right")

        # pole tekstowe na odpowiedz AI 
        master.ai_response_box = ctk.CTkTextbox(master.ai_frame,
                                                height=120,
                                                font=("Arial", 13),
                                                fg_color=BG_CARD,
                                                text_color=TEXT,
                                                border_width=0,
                                                wrap="word",
                                                state="disabled")
        master.ai_response_box.pack(fill="x", padx=14, pady=(0, 12))

        # statystyki na samym dole
        master.footer_frame = ctk.CTkFrame(master, fg_color=BG_FRAME)
        master.footer_frame.pack(side="bottom", fill="x", pady=20)
        # tworzenie frame grida
        for i in range(5):
            master.footer_frame.grid_columnconfigure(i, weight=1)

        # naglowki
        # label na poprawne odpowiedzi
        master.poprawne_label = ctk.CTkLabel(master.footer_frame, text="Poprawne", font=("Arial", 24, "bold"),
                                             text_color=ACCENT_SUCCESS)
        master.poprawne_label.grid(row=0, column=0, sticky="nsew")
        # label na nauczone pytania
        master.nauczone_label = ctk.CTkLabel(master.footer_frame, text="Nauczone", font=("Arial", 24, "bold"),
                                             text_color=TEXT)
        master.nauczone_label.grid(row=0, column=1, sticky="nsew")
        # label na procenty poprawnych odpowiedzi (poprawne/poprawne+niepoprawne)
        master.procent_label = ctk.CTkLabel(master.footer_frame, text="Procent", font=("Arial", 24, "bold"),
                                            text_color=TEXT)
        master.procent_label.grid(row=0, column=2, sticky="nsew")
        # label na niepoprawne odpowiedzi
        master.niepoprawne_label = ctk.CTkLabel(master.footer_frame, text="Niepoprawne", font=("Arial", 24, "bold"),
                                                text_color=ACCENT_ERROR)
        master.niepoprawne_label.grid(row=0, column=3, sticky="nsew")
        # label na niepoprawne odpowiedzi
        master.nienauczone_label = ctk.CTkLabel(master.footer_frame, text="Nienauczone", font=("Arial", 24, "bold"),
                                                text_color=TEXT)
        master.nienauczone_label.grid(row=0, column=4, sticky="nsew")

        # grid wartosci statystyk
        master.poprawne_label_num = ctk.CTkLabel(master.footer_frame, text="0", font=("Arial", 24, "bold"),
                                                 text_color=TEXT)
        master.poprawne_label_num.grid(row=1, column=0, sticky="nsew")
        # wartosci nauczonych odpowiedzi
        master.nauczone_num = ctk.CTkLabel(master.footer_frame, text="0", font=("Arial", 24, "bold"), text_color=TEXT)
        master.nauczone_num.grid(row=1, column=1, sticky="nsew")
        # wartosci procentowe odpowiedzi poprawnych
        master.procent_label_num = ctk.CTkLabel(master.footer_frame, text="0%", font=("Arial", 24, "bold"),
                                                text_color=ACCENT)
        master.procent_label_num.grid(row=1, column=2, sticky="nsew")
        # wartosc niepoprawnych odpowiedzi
        master.niepoprawne_label_num = ctk.CTkLabel(master.footer_frame, text="0", font=("Arial", 24, "bold"),
                                                    text_color=TEXT)
        master.niepoprawne_label_num.grid(row=1, column=3, sticky="nsew")
        # wartosc nienauczonych odpowiedzi
        master.nienauczone_num = ctk.CTkLabel(master.footer_frame, text="0", font=("Arial", 24, "bold"),
                                              text_color=TEXT)
        master.nienauczone_num.grid(row=1, column=4, sticky="nsew")

        self.setup_restart_buttons(master)

    def setup_restart_buttons(self, master):
        #frame na przyciski restartow
        master.button_restart_frame = ctk.CTkFrame(master, fg_color="transparent")
        master.button_restart_frame.pack(pady=20, side="bottom")
        #przycisk resetujacy statystyki (nauczone, nienauczone)
        master.button_hard_restart = ctk.CTkButton(master.button_restart_frame,
                                                   text="Zresetuj wszystko i zacznij od nowa",
                                                   font=("Arial", 28, "bold"),
                                                   command=master.restart_test_hard,
                                                   fg_color=BG_FRAME,
                                                   hover_color=ACCENT_ERROR,
                                                   text_color=TEXT,
                                                   border_width=1,
                                                   border_color=ACCENT_ERROR)
        master.button_hard_restart.pack(side="bottom", pady=10)
        #przycisk soft resetujacy tylko obecna sesje zachowujac statystyki (nauczone, nienauczone)
        master.button_restart = ctk.CTkButton(master.button_restart_frame,
                                              text="Zacznij od nowa",
                                              font=("Arial", 28, "bold"),
                                              command=master.restart_test,
                                              fg_color=BG_FRAME,
                                              hover_color=ACCENT_WARN,
                                              text_color=TEXT,
                                              border_width=1,
                                              border_color=ACCENT_WARN)
        master.button_restart.pack(side="top", pady=10)

    def back_to_menu(self, master, button_command):
        #frame na przycisk back to menu
        master.button_go_back_to_menu_frame = ctk.CTkFrame(master, fg_color="transparent")
        #przycisk back to menu
        master.button_go_back_to_menu = ctk.CTkButton(master.button_go_back_to_menu_frame,
                                                      text="Wróć do menu",
                                                      font=("Arial", 28, "bold"),
                                                      command=button_command,
                                                      width=300,
                                                      height=60,
                                                      fg_color=BG_FRAME,
                                                      hover_color=ACCENT_SUCCESS,
                                                      text_color=TEXT,
                                                      border_width=1,
                                                      border_color=ACCENT_SUCCESS)
        master.button_go_back_to_menu.pack(side="bottom", pady=30)

    def show_closed_question(self, master):
        master.open_question_frame.pack_forget()
        master.buttons_frame.pack(pady=20)

    def show_open_question(self, master):
        master.buttons_frame.pack_forget()
        master.open_question_frame.pack(pady=20)
        master.correct_answer_display.pack_forget()
        master.answer_entry.configure(state="normal")
        master.answer_entry.delete(0, "end")
        master.answer_entry.configure(fg_color=BG_FRAME, text_color=TEXT)
        master.submit_open_btn.configure(state="normal")
        master.answer_entry.focus_set()

    def show_ai_panel(self, master):
        master.ai_frame.pack(pady=8, padx=60, fill="x")
        master.ai_prompt_entry.bind("<Return>", lambda e: self.ai_wyslij_wlasny_prompt(master))
        master.ai_prompt_entry.bind("<KP_Enter>", lambda e: self.ai_wyslij_wlasny_prompt(master))

    def hide_ai_panel(self, master):
        master.ai_frame.pack_forget()
        self.ai_wyczysc(master)

    def ai_wyczysc(self, master):
        master.ai_response_box.configure(state="normal")
        master.ai_response_box.delete("1.0", "end")
        master.ai_response_box.configure(state="disabled")
        master.ai_prompt_entry.delete(0, "end")

    def ai_ustaw_tekst(self, master, tekst):
        master.ai_response_box.configure(state="normal")
        master.ai_response_box.delete("1.0", "end")
        master.ai_response_box.insert("end", tekst)
        master.ai_response_box.configure(state="disabled")

    def ai_wyjasnij_odpowiedz(self, master):
        if not hasattr(master, 'dane') or master.index >= len(master.dane):
            return
        pytanie_data = master.dane[master.index]
        pytanie = pytanie_data.get("pytanie", "")
        poprawna = pytanie_data.get("poprawna", "")
        twoja = getattr(master, '_ostatnia_odpowiedz', "")
        opcje = pytanie_data.get("opcje", {})
        typ = pytanie_data.get("typ", "zamkniete")

        prompt = zbuduj_prompt_quiz(pytanie, opcje, poprawna, twoja, typ)
        self._ai_uruchom(master, prompt, master.ai_explain_btn, master.ai_ask_btn)

    def ai_wyslij_wlasny_prompt(self, master):
        user_text = master.ai_prompt_entry.get().strip()
        if not user_text:
            return

        if hasattr(master, 'dane') and master.index < len(master.dane):
            pytanie_data = master.dane[master.index]
            kontekst = (
                f"Kontekst pytania egzaminacyjnego: {pytanie_data.get('pytanie', '')}\n"
                f"Poprawna odpowiedź: {pytanie_data.get('poprawna', '')}\n\n"
                f"Pytanie użytkownika: {user_text}\n\n"
                f"Odpowiedz po polsku."
            )
        else:
            kontekst = user_text + "\n\nOdpowiedz po polsku."

        self._ai_uruchom(master, kontekst, master.ai_explain_btn, master.ai_ask_btn)

    def _ai_uruchom(self, master, prompt, *przyciski_do_disable):
        self.ai_ustaw_tekst(master, "⏳ Generowanie odpowiedzi...")
        for btn in przyciski_do_disable:
            btn.configure(state="disabled")

        accumulated = [""]

        def on_chunk(token):
            accumulated[0] += token
            def update():
                master.ai_response_box.configure(state="normal")
                master.ai_response_box.delete("1.0", "end")
                master.ai_response_box.insert("end", accumulated[0])
                master.ai_response_box.see("end")
                master.ai_response_box.configure(state="disabled")
            master.after(0, update)

        def on_done():
            def enable():
                for btn in przyciski_do_disable:
                    btn.configure(state="normal")
            master.after(0, enable)

        def on_error(msg):
            def show_err():
                self.ai_ustaw_tekst(master, f"❌ {msg}")
                for btn in przyciski_do_disable:
                    btn.configure(state="normal")
            master.after(0, show_err)

        zapytaj_ollame(prompt, on_chunk, on_done, on_error)

    def show_koniec_testu(self, master, final_procent):
        master.pytania_label.configure(text="Koniec testu!")
        master.procent_label_num.configure(text=f"{final_procent}%")
        master.pytanie.configure(text="Wybierz opcję na dole ekranu")
        master.buttons_frame.pack_forget()
        master.open_question_frame.pack_forget()
        master.progressbar.set(1)

        if not hasattr(master, 'show_bledy_btn'):
            master.show_bledy_btn = ctk.CTkButton(master, text="Przejrzyj błędy", font=("Arial", 28, "bold"),
                                                  command=lambda: self.show_bledy(master),
                                                  fg_color=BG_FRAME,
                                                  hover_color=ACCENT_ERROR,
                                                  text_color=ACCENT_ERROR,
                                                  border_width=1,
                                                  border_color=ACCENT_ERROR,
                                                  width=300, height=60)

        if len(master.bledy) > 0:
            master.show_bledy_btn.pack(pady=20)

    def show_bledy(self, master):
        self.nothing(master)
        master.footer_frame.pack(side="bottom", fill="x", pady=20)
        master.button_restart_frame.pack(pady=20, side="bottom")
        master.button_go_back_to_menu_frame.pack(side="bottom", pady=30)

        if not hasattr(master, 'bledy_frame'):
            master.bledy_frame = ctk.CTkScrollableFrame(master, fg_color=BG_FRAME,
                                                        scrollbar_button_color=ACCENT,
                                                        scrollbar_button_hover_color=BG_CARD)
        else:
            for widget in master.bledy_frame.winfo_children():
                widget.destroy()

        master.bledy_frame.pack(pady=20, padx=20, fill="both", expand=True)

        for i, blad in enumerate(master.bledy):
            self._renderuj_blad_z_ai(master, master.bledy_frame, i, blad)

    def _renderuj_blad_z_ai(self, master, rodzic_frame, i, blad):
        pojedynczy_blad_frame = ctk.CTkFrame(rodzic_frame, fg_color=BG_CARD, corner_radius=8)
        pojedynczy_blad_frame.pack(pady=6, padx=10, fill="x")

        pytanie_label = ctk.CTkLabel(
            pojedynczy_blad_frame,
            text=f"{i + 1}. {blad['pytanie']}",
            font=("Arial", 18, "bold"),
            text_color=TEXT,
            justify="left",
            anchor="w"
        )
        pytanie_label.pack(anchor="w", padx=14, pady=(10, 2))

        twoja_label = ctk.CTkLabel(
            pojedynczy_blad_frame,
            text=f"Twoja odpowiedź: {blad['twoja']}",
            font=("Arial", 16),
            text_color=ACCENT_ERROR,
            justify="left",
            anchor="w"
        )
        twoja_label.pack(anchor="w", padx=28, pady=2)

        poprawna_label = ctk.CTkLabel(
            pojedynczy_blad_frame,
            text=f"Poprawna odpowiedź: {blad['poprawna']}",
            font=("Arial", 16, "bold"),
            text_color=ACCENT_SUCCESS,
            justify="left",
            anchor="w"
        )
        poprawna_label.pack(anchor="w", padx=28, pady=(2, 6))

        ai_dolny_frame = ctk.CTkFrame(pojedynczy_blad_frame, fg_color="transparent")
        ai_dolny_frame.pack(fill="x", padx=14, pady=(0, 10))

        ai_box = ctk.CTkTextbox(ai_dolny_frame,
                                height=90,
                                font=("Arial", 13),
                                fg_color=BG_FRAME,
                                text_color=TEXT,
                                border_width=1,
                                border_color=ACCENT_AI,
                                wrap="word",
                                state="disabled")
        ai_btn_ref = [None]

        def wyjasnij_blad(b=blad, box=ai_box, btn_lista=ai_btn_ref):
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
                               font=("Arial", 13, "bold"),
                               fg_color="transparent",
                               hover_color=BG_FRAME,
                               text_color=ACCENT_AI,
                               border_width=1,
                               border_color=ACCENT_AI,
                               height=30,
                               width=130,
                               command=wyjasnij_blad)
        ai_btn.pack(side="left")
        ai_btn_ref[0] = ai_btn