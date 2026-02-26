import customtkinter as ctk
import random
from database import *
from gui import QuizUI
from tkinter import filedialog, messagebox
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self, baza):
        super().__init__()
        self.baza_sciezka = baza

        # okno
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

        btn_color = "#2ecc71" if path else ["#3B8ED0", "#1F6AA5"]
        test_btn = ctk.CTkButton(
            row_frame,
            text=name,
            text_color="black",
            font=("Arial", 18, "bold"),
            width=500,
            height=60,
            fg_color=btn_color,
            command=lambda: self.wybor_testu(test_info["path"])
        )
        test_btn.pack(side="left", padx=(5, 1))

        delete_btn = ctk.CTkButton(row_frame, text="X", width=80, height=60,
                                   fg_color="red",
                                   command=lambda n=name, f=row_frame: self.delete_test(n, f))
        delete_btn.pack(side="right", padx=5)

        file_button = ctk.CTkButton(
            row_frame,
            text="📁 Plik",
            font=("Arial", 18, "bold"),
            width=100,
            height=60,
            fg_color="gray",
            command=lambda n=name: self.przypisz_plik(n, test_info, test_btn)
        )
        file_button.pack(side="right", padx=(0, 2))

        edit_button = ctk.CTkButton(
            row_frame,
            text="EDYTUJ",
            font=("Arial", 18, "bold"),
            width=100,
            height=60,
            fg_color="gray",
            command=lambda p=path: self.prepare_edit(p)

        )
        edit_button.pack(side="right", padx=(5, 5))

    def przypisz_plik(self, nazwa, info_dictionary, btn):
        sciezka = filedialog.askopenfilename(filetypes=[("Json Files", "*.json")])
        if sciezka:
            info_dictionary["path"] = sciezka
            btn.configure(fg_color="#2ecc71")
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

    def prepare_edit(self, sciezka):
        if sciezka and os.path.exists(sciezka):
            if self.baza_sciezka:
                self.historia_bledow[self.baza_sciezka] = self.bledy

            self.baza_sciezka = sciezka
            self.dane = load_data(sciezka)

            self.bledy = self.historia_bledow.get(sciezka, [])

            self.edit_menu()
        else:
            messagebox.showwarning("Brak pliku", "Ten test nie ma przypisanego pliku JSON! Użyj przycisku Plik.")

    def edit_menu(self):
        self.unbind("<Return>")
        self.unbind("<KP_Enter>")
        self.ui_manager.show_edit_menu(self)

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
                    btn.configure(state="normal", fg_color=["#3B8ED0", "#1F6AA5"])
                for litera in ["A", "B", "C", "D"]:
                    o_tekst = pytanie['opcje'].get(litera, "")
                    self.buttons[litera].configure(text=f"{litera}: {o_tekst}")

        else:
            final_procent = int((self.poprawne / len(self.dane)) * 100) if len(self.dane) > 0 else 0
            self.ui_manager.show_koniec_testu(self, final_procent)

    def check_answer_closed(self, wybrana):
        poprawna = self.dane[self.index]['poprawna']

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

        def normalize(text):
            return "".join(char.lower() for char in text if char.isalnum())

        user_clean = normalize(user_answer)
        correct_clean = normalize(correct_answer)

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

        self.unbind("<Return>")
        self.unbind("<KP_Enter>")
        self.bind("<Return>", lambda event: self.handle_enter())
        self.bind("<KP_Enter>", lambda event: self.handle_enter())
    def update_stats(self):
        nauczone_count = sum(1 for p in self.dane if p.get('licznik', 0) > 2)
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



if __name__ == "__main__":
    nazwa_bazy = "baza.json"
    if not os.path.exists(nazwa_bazy):
        with open(nazwa_bazy, "w", encoding="utf-8") as f:
            f.write("[]")
    app = App(nazwa_bazy)
    app.mainloop()