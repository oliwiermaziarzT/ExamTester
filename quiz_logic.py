from database import save_data
import random


class QuizLogic:
    def show_pytania(self):
        self.question_answered = False
        self.unbind("<Return>")
        self.unbind("<KP_Enter>")

        self.menu_button_frame.pack_forget()
        self.add_test_button_frame.pack_forget()
        self.new_tests_frame.pack_forget()
        self.signature_label.pack_forget()
        if hasattr(self, "add_test_through_ai_frame"):
            self.add_test_through_ai_frame.pack_forget()
        if hasattr(self, "api_key_frame"):
            self.api_key_frame.pack_forget()
        for w in ["action_buttons_frame", "action_buttons_frame2", "stats_frame",
                  "total_questions_label", "last_results_btn", "go_back_to_edit_menu_btn",
                  "change_question_frame", "add_question_menu_frame", "add_question_open_frame",
                  "edit_question_menu_frame", "edit_question_open_frame", "last_results_frame"]:
            widget = getattr(self, w, None)
            if widget:
                try:
                    widget.pack_forget()
                except Exception:
                    pass
        if hasattr(self, "fig_stats"):
            import matplotlib.pyplot as plt
            plt.close(self.fig_stats)

        if hasattr(self, "show_bledy_btn"):
            self.show_bledy_btn.pack_forget()
        if hasattr(self, "bledy_frame"):
            self.bledy_frame.pack_forget()
        if hasattr(self, "restart_test_bledy"):
            self.restart_test_bledy.pack_forget()

        self.ai_frame.pack_forget()
        self.buttons_frame.pack_forget()
        self.open_question_frame.pack_forget()
        self.center_frame.pack_forget()

        self.progressbar.pack(side="top", padx=20, pady=20)
        self.pytania_label.pack(side="top", pady=10)
        self.pytanie.pack(side="top", pady=20)
        self.center_frame.pack(side="top", fill="x", padx=60)
        self.footer_frame.pack(side="bottom", fill="x")
        self.button_restart_frame.pack(side="bottom", pady=10)
        self.button_go_back_to_menu_frame.pack(side="bottom", pady=10)

        if self.index < len(self.dane):
            pytanie = self.dane[self.index]
            self.pytania_label.configure(text=f"Pytanie {self.index + 1} z {len(self.dane)}")
            self.pytanie.configure(text=f"{pytanie['pytanie']}")
            self.update_stats()
            self.progressbar.set(self.index / len(self.dane))

            is_open_question = 'typ' in pytanie and pytanie['typ'] == 'otwarte'

            if is_open_question:
                self.ui_manager.show_open_question(self)
                self.bind("<Return>", lambda event: self.check_answer_open())
                self.bind("<KP_Enter>", lambda event: self.check_answer_open())
            else:
                self.ui_manager.show_closed_question(self)
                for btn in self.buttons.values():
                    btn.configure(state="normal", fg_color=["#3B8ED0", "#1F6AA5"],
                                  text_color=["#DCE4EE", "white"])
                for litera in ["A", "B", "C", "D"]:
                    o_tekst = pytanie['opcje'].get(litera, "")
                    self.buttons[litera].configure(text=f"{litera}: {o_tekst}")
                self.bind("<a>", lambda event: self.check_answer_closed("A"))
                self.bind("<b>", lambda event: self.check_answer_closed("B"))
                self.bind("<c>", lambda event: self.check_answer_closed("C"))
                self.bind("<d>", lambda event: self.check_answer_closed("D"))

            self.ui_manager.show_ai_panel_always(self, is_open_question)

        else:
            final_procent = int((self.poprawne / len(self.dane)) * 100) if len(self.dane) > 0 else 0
            self.ui_manager.show_koniec_testu(self, final_procent)

    def show_pytania_incorrect(self):
        if not self.bledy:
            return

        seen = set()
        bledy_dane = []
        for blad in self.bledy:
            pytanie_text = blad['pytanie']
            if pytanie_text not in seen:
                seen.add(pytanie_text)
                if 'dane_pytania' in blad:
                    bledy_dane.append(dict(blad['dane_pytania']))

        if not bledy_dane:
            return

        self.dane = bledy_dane
        self.index = 0
        self.poprawne = 0
        self.niepoprawne = 0
        self.bledy = []
        self.bledy_mode = True  

        random.shuffle(self.dane)
        self.show_pytania()

    def start_unlearned_test(self):
        from tkinter import messagebox
        from database import load_data

        full_data = load_data(self.baza_sciezka)
        nienauczone = [q for q in full_data if q.get('licznik', 0) <= 3]

        if not nienauczone:
            messagebox.showinfo("Gratulacje!", "Wszystkie pytania w tym teście zostały już nauczone!")
            return

        self.dane = nienauczone
        self.index = 0
        self.poprawne = 0
        self.niepoprawne = 0
        self.bledy = []
        self.bledy_mode = True 
        if self.baza_sciezka:
            self.historia_bledow[self.baza_sciezka] = []

        random.shuffle(self.dane)
        self.show_pytania()

    def check_answer_closed(self, wybrana):

        if self.question_answered:
            return

        poprawna = self.dane[self.index]['poprawna']
        self._ostatnia_odpowiedz = wybrana

        if wybrana == poprawna:
            self.buttons[wybrana].configure(fg_color="green", text_color="black")
            self.poprawne += 1
            self.dane[self.index]['licznik'] += 1
        else:
            self.buttons[wybrana].configure(fg_color="red", text_color="black")
            self.buttons[poprawna].configure(fg_color="green", text_color="black")
            self.niepoprawne += 1
            self.dane[self.index]['licznik'] -= 1

            self.bledy.append({
                "pytanie": self.dane[self.index]['pytanie'],
                "twoja": wybrana,
                "poprawna": poprawna,
                "dane_pytania": self.dane[self.index] 
            })

        self.unbind("<a>")
        self.unbind("<b>")
        self.unbind("<c>")
        self.unbind("<d>")

        if not getattr(self, 'bledy_mode', False):
            save_data(self.baza_sciezka, self.dane)
        self.update_stats()

        for btn in self.buttons.values():
            btn.configure(state="disabled", text_color_disabled="black")

        self.finalize_question_step()

    def check_answer_open(self):
        if self.question_answered:
            return

        user_answer = self.answer_entry.get().strip()
        correct_answer = str(self.dane[self.index]['poprawna']).strip()
        self._ostatnia_odpowiedz = user_answer

        def normalize(text):
            return "".join(char.lower() for char in text if char.isalnum())

        user_clean = normalize(user_answer)
        correct_clean = normalize(correct_answer)

        if user_clean == "":
            return

        if user_clean == correct_clean:
            self.answer_entry.configure(fg_color="green", text_color="black")
            self.poprawne += 1
            self.dane[self.index]['licznik'] += 1
        else:
            self.answer_entry.configure(fg_color="red", text_color="black")
            self.correct_answer_display.configure(text=f"Poprawna odpowiedź: {correct_answer}")
            self.correct_answer_display.pack(pady=5)
            self.niepoprawne += 1
            self.dane[self.index]['licznik'] -= 1

            self.bledy.append({
                "pytanie": self.dane[self.index]['pytanie'],
                "twoja": user_answer,
                "poprawna": correct_answer,
                "dane_pytania": self.dane[self.index] 
            })

        self.submit_open_btn.configure(state="disabled")
        self.answer_entry.configure(state="disabled")
        self.finalize_question_step()

    def finalize_question_step(self):
        self.question_answered = True
        if self.baza_sciezka and not getattr(self, 'bledy_mode', False):
            self.historia_bledow[self.baza_sciezka] = self.bledy
            save_data(self.baza_sciezka, self.dane)
        self.update_stats()
        self.pytania_label.configure(text="Naciśnij ENTER, aby kontynuować", text_color="yellow")

        self.ui_manager.show_ai_panel(self)

        self.unbind("<Return>")
        self.unbind("<KP_Enter>")
        self.bind("<Return>", lambda event: self.handle_enter())
        self.bind("<KP_Enter>", lambda event: self.handle_enter())

    def update_stats(self):
        nauczone_count = sum(1 for p in self.dane if p.get('licznik', 0) > 3)
        nienauczone_count = len(self.dane) - nauczone_count

        total_answered = self.poprawne + self.niepoprawne
        if total_answered > 0:
            procent = int((self.poprawne / total_answered) * 100)
        else:
            procent = 0

        self.poprawne_label_num.configure(text=str(self.poprawne))
        self.niepoprawne_label_num.configure(text=str(self.niepoprawne))
        self.procent_label_num.configure(text=f"{procent}%")

        self.nauczone_num.configure(text=str(nauczone_count))
        self.nienauczone_num.configure(text=str(nienauczone_count))

    def next_question(self):
        self.index += 1
        self.show_pytania()

    def restart_test(self):
        self.index = 0
        self.poprawne = 0
        self.niepoprawne = 0
        self.bledy = []
        self.bledy_mode = False 
        if self.baza_sciezka:
            self.historia_bledow[self.baza_sciezka] = []

        self.procent_label_num.configure(text="0%")
        random.shuffle(self.dane)
        self.show_pytania()

    def restart_test_hard(self):
        for i in self.dane:
            i['licznik'] = 0
        save_data(self.baza_sciezka, self.dane)
        self.update_stats()
        self.restart_test()

    def handle_enter(self):
        self.unbind("<Return>")
        self.unbind("<KP_Enter>")
        self.next_question()