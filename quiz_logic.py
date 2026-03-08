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

        if hasattr(self, "show_bledy_btn"):
            self.show_bledy_btn.pack_forget()
        if hasattr(self, "bledy_frame"):
            self.bledy_frame.pack_forget()

        self.ui_manager.hide_ai_panel(self)
        self.progressbar.pack(side="top", padx=20, pady=20)
        self.pytania_label.pack(side="top", pady=10)
        self.pytanie.pack(side="top", pady=20)
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

        else:
            final_procent = int((self.poprawne / len(self.dane)) * 100) if len(self.dane) > 0 else 0
            self.ui_manager.show_koniec_testu(self, final_procent)

    def check_answer_closed(self, wybrana):
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
                "poprawna": poprawna
            })

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
                "poprawna": correct_answer
            })

        self.submit_open_btn.configure(state="disabled")
        self.answer_entry.configure(state="disabled")
        self.finalize_question_step()

    def finalize_question_step(self):
        self.question_answered = True
        if self.baza_sciezka:
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