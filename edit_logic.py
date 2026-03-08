import customtkinter as ctk
from tkinter import messagebox
from database import save_data


class EditLogic:
    def edit_menu(self):
        self.unbind("<Return>")
        self.unbind("<KP_Enter>")
        self.ui_manager.show_edit_menu(self)

    def prepare_edit(self, sciezka):
        import os
        if sciezka and os.path.exists(sciezka):
            if self.baza_sciezka:
                self.historia_bledow[self.baza_sciezka] = self.bledy

            self.baza_sciezka = sciezka
            from database import load_data
            self.dane = load_data(sciezka)

            self.bledy = self.historia_bledow.get(sciezka, [])

            self.edit_menu()
        else:
            messagebox.showwarning("Brak pliku", "Ten test nie ma przypisanego pliku JSON! Użyj przycisku Plik.")

    def start_add_question_closed(self):
        self.ui_manager.add_question_closed_menu(self, self.save_question_event)
        self.bind("<Return>", lambda event: self.save_question_event("zamkniete"))
        self.bind("<KP_Enter>", lambda event: self.save_question_event("zamkniete"))

    def start_add_question_open(self):
        self.ui_manager.add_question_open_menu(self, self.save_question_event)
        self.bind("<Return>", lambda event: self.save_question_event("otwarte"))
        self.bind("<KP_Enter>", lambda event: self.save_question_event("otwarte"))

    def start_change_question(self):
        self.ui_manager.change_question_menu(self)
        self.search_question_entry.bind("<KeyRelease>", self.filter_questions)
        self.filter_questions()

    def refresh_questions_count(self):
        if hasattr(self, "total_questions_label") and self.total_questions_label.winfo_exists():
            self.total_questions_label.configure(text=f"Suma pytań w tym teście: {len(self.dane)}")

    def filter_questions(self, event=None):
        search_text = self.search_question_entry.get().lower()

        if event and event.keysym == "BackSpace" and not search_text:
            return
        for widget in self.change_question_scrollable_frame.winfo_children():
            widget.destroy()

        for i, pytanie_data in enumerate(self.dane):
            tresc = pytanie_data.get("pytanie", "Brak treści")
            typ = pytanie_data.get("typ", "zamkniete")

            if search_text in tresc.lower():
                tresc_btn = (tresc[:50] + "...") if len(tresc) > 50 else tresc

                row_frame = ctk.CTkFrame(self.change_question_scrollable_frame, fg_color="transparent")
                row_frame.pack(side="top", fill="x", padx=10, pady=2)

                if typ == "otwarte":
                    tag_text = "OTWARTE"
                    tag_color = "#3498db"
                else:
                    tag_text = "ZAMKNIĘTE"
                    tag_color = "#9b59b6"

                type_tag = ctk.CTkLabel(
                    row_frame,
                    text=tag_text,
                    font=("Arial", 10, "bold"),
                    fg_color=tag_color,
                    text_color="white",
                    width=80,
                    corner_radius=5
                )
                type_tag.pack(side="left", padx=(0, 10))

                lbl = ctk.CTkLabel(row_frame, text=f"{i + 1}. {tresc_btn}", font=("Arial", 16), anchor="w",
                                   justify="left")
                lbl.pack(side="left", fill="x", expand=True)

                btn_edit = ctk.CTkButton(
                    row_frame,
                    text="Edytuj",
                    width=80,
                    fg_color="#f39c12",
                    hover_color="#d35400",
                    command=lambda x=i: self.edit_existing_question(x)
                )
                btn_edit.pack(side="right", padx=5)

                btn_del = ctk.CTkButton(
                    row_frame,
                    text="Usuń",
                    width=80,
                    fg_color="#e74c3c",
                    hover_color="#c0392b",
                    command=lambda x=i: self.delete_question(x)
                )
                btn_del.pack(side="right", padx=5)

    def delete_question(self, index):
        pytanie = self.dane[index]
        tresc = pytanie.get("pytanie", "")
        skrocona = (tresc[:50] + "...") if len(tresc) > 50 else tresc

        if messagebox.askyesno("Usuń pytanie", f"Czy na pewno usunąć pytanie:\n\n{skrocona}?"):
            self.dane.pop(index)
            save_data(self.baza_sciezka, self.dane)
            self.filter_questions()
            self.refresh_questions_count()
            messagebox.showinfo("Sukces", "Pytanie zostało usunięte.")

    def edit_existing_question(self, index):
        self.current_edit_index = index
        pytanie_data = self.dane[index]
        typ = pytanie_data.get("typ", "zamkniete")

        if typ == "otwarte":
            self.ui_manager.edit_question_open_menu(self, self.save_edited_question, pytanie_data)
        else:
            self.ui_manager.edit_question_closed_menu(self, self.save_edited_question, pytanie_data)

    def show_last_results_event(self):
        posortowane = sorted(self.dane, key=lambda q: q.get("licznik", 0))
        najgorsze = posortowane[:5]
        najlepsze = posortowane[-5:]
        najlepsze.reverse()
        self.ui_manager.show_last_results_menu(self, najgorsze, najlepsze)

    def save_edited_question(self, typ_pytania):
        index = self.current_edit_index

        if typ_pytania == "otwarte":
            tresc = self.input_answer.get().strip()
            poprawna = self.input_answer_correct.get().strip()

            if not tresc or not poprawna:
                messagebox.showwarning("Puste pola", "Wypełnij pytanie i klucz odpowiedzi!")
                return

            self.dane[index]["pytanie"] = tresc
            self.dane[index]["poprawna"] = poprawna

        elif typ_pytania == "zamkniete":
            tresc = self.question_input.get().strip()
            opcja_a = self.option_input1.get().strip()
            opcja_b = self.option_input2.get().strip()
            opcja_c = self.option_input3.get().strip()
            opcja_d = self.option_input4.get().strip()
            poprawna = self.correct_option.get().strip().upper()

            if not all([tresc, opcja_a, opcja_b, opcja_c, opcja_d, poprawna]):
                messagebox.showwarning("Puste pola", "Wypełnij wszystkie pola dla pytania zamkniętego!")
                return

            self.dane[index]["pytanie"] = tresc
            self.dane[index]["opcje"]["A"] = opcja_a
            self.dane[index]["opcje"]["B"] = opcja_b
            self.dane[index]["opcje"]["C"] = opcja_c
            self.dane[index]["opcje"]["D"] = opcja_d
            self.dane[index]["poprawna"] = poprawna

        save_data(self.baza_sciezka, self.dane)
        messagebox.showinfo("Sukces", "Pytanie zostało zaktualizowane.")
        self.start_change_question()

    def save_question_event(self, typ_pytania):
        import os
        if not self.baza_sciezka or not os.path.exists(self.baza_sciezka):
            messagebox.showerror("Błąd", "Nie wybrano pliku z testem!")
            return

        if typ_pytania == "otwarte":
            tresc = self.input_answer.get().strip()
            poprawna = self.input_answer_correct.get().strip()

            if not tresc or not poprawna:
                messagebox.showwarning("Puste pola", "Wypełnij pytanie i klucz odpowiedzi!")
                return

            new_question = {
                "pytanie": tresc,
                "poprawna": poprawna,
                "licznik": 0,
                "typ": "otwarte"
            }

        elif typ_pytania == "zamkniete":
            tresc = self.question_input.get().strip()
            opcja_a = self.option_input1.get().strip()
            opcja_b = self.option_input2.get().strip()
            opcja_c = self.option_input3.get().strip()
            opcja_d = self.option_input4.get().strip()
            poprawna = self.correct_option.get().strip().upper()

            if not all([tresc, opcja_a, opcja_b, opcja_c, opcja_d, poprawna]):
                messagebox.showwarning("Puste pola", "Wypełnij wszystkie pola dla pytania zamkniętego!")
                return

            new_question = {
                "pytanie": tresc,
                "opcje": {
                    "A": opcja_a,
                    "B": opcja_b,
                    "C": opcja_c,
                    "D": opcja_d
                },
                "poprawna": poprawna,
                "licznik": 0,
                "typ": "zamkniete"
            }

        self.dane.append(new_question)
        save_data(self.baza_sciezka, self.dane)
        self.refresh_questions_count()

        if typ_pytania == "otwarte":
            self.input_answer.delete(0, "end")
            self.input_answer_correct.delete(0, "end")
            self.input_answer.focus_set()
        elif typ_pytania == "zamkniete":
            self.question_input.delete(0, "end")
            self.option_input1.delete(0, "end")
            self.option_input2.delete(0, "end")
            self.option_input3.delete(0, "end")
            self.option_input4.delete(0, "end")
            self.correct_option.delete(0, "end")
            self.question_input.focus_set()