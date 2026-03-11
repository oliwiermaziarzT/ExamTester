import customtkinter as ctk
import json
import os
from tkinter import filedialog, messagebox

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


class QuizUIAIGenerator:
    def _make_placeholder_textbox(self, parent, placeholder, height=140, border_color=BG_CARD):
        box = ctk.CTkTextbox(
            parent, height=height,
            font=("Arial", 13), fg_color=BG_CARD,
            text_color=TEXT_DIM,
            border_color=border_color, border_width=1,
            wrap="word"
        )
        box._placeholder = placeholder
        box._has_placeholder = True
        box.insert("1.0", placeholder)

        def on_focus_in(event):
            if box._has_placeholder:
                box.delete("1.0", "end")
                box.configure(text_color=TEXT)
                box._has_placeholder = False

        def on_focus_out(event):
            if box.get("1.0", "end").strip() == "":
                box.configure(text_color=TEXT_DIM)
                box.insert("1.0", placeholder)
                box._has_placeholder = True

        box.bind("<FocusIn>", on_focus_in)
        box.bind("<FocusOut>", on_focus_out)
        return box

    def _get_textbox_value(self, box):
        if getattr(box, "_has_placeholder", False):
            return ""
        return box.get("1.0", "end").strip()

    def show_ai_generator_menu(self, master):
        self._hide_all_for_ai(master)

        master.ai_generator_frame = ctk.CTkFrame(master, fg_color="transparent")
        master.ai_generator_frame.pack(fill="both", expand=True, padx=40, pady=20)

        ctk.CTkLabel(
            master.ai_generator_frame,
            text="✦  Generuj test przez AI",
            font=("Arial", 28, "bold"),
            text_color=ACCENT_AI
        ).pack(pady=(10, 2))

        ctk.CTkLabel(
            master.ai_generator_frame,
            text="Wybierz źródło materiału, ustaw liczbę pytań i wygeneruj test zamknięty (A/B/C/D)",
            font=("Arial", 14),
            text_color=TEXT_DIM
        ).pack(pady=(0, 15))

        content_frame = ctk.CTkFrame(master.ai_generator_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)

        left = ctk.CTkFrame(content_frame, fg_color=BG_FRAME, corner_radius=12)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(left, text="Źródło materiału", font=("Arial", 16, "bold"), text_color=TEXT).pack(pady=(15, 8))

        master._ai_source_var = ctk.StringVar(value="temat")
        tabs_frame = ctk.CTkFrame(left, fg_color="transparent")
        tabs_frame.pack(fill="x", padx=15, pady=(0, 10))

        source_options = [
            ("📝 Temat",   "temat"),
            ("📋 Tekst",   "tekst"),
            ("📄 Plik",    "plik"),
            ("🖼️ Zdjęcie", "zdjecie"),
        ]
        master._ai_tab_buttons = {}
        for label, val in source_options:
            btn = ctk.CTkButton(
                tabs_frame, text=label,
                font=("Arial", 13, "bold"),
                width=130, height=38,
                fg_color=ACCENT_AI if val == "temat" else BG_CARD,
                hover_color="#8a5eff",
                text_color=TEXT,
                border_width=1, border_color=ACCENT_AI,
                command=lambda v=val: self._switch_ai_source(master, v)
            )
            btn.pack(side="left", padx=3)
            master._ai_tab_buttons[val] = btn

        master._ai_source_content = ctk.CTkFrame(left, fg_color="transparent")
        master._ai_source_content.pack(fill="both", expand=True, padx=15, pady=10)
        self._show_source_temat(master)

        right = ctk.CTkFrame(content_frame, fg_color=BG_FRAME, corner_radius=12, width=290)
        right.pack(side="right", fill="y", padx=(10, 0))
        right.pack_propagate(False)

        ctk.CTkLabel(right, text="Ustawienia", font=("Arial", 16, "bold"), text_color=TEXT).pack(pady=(15, 10))

        ctk.CTkLabel(right, text="Liczba pytań:", font=("Arial", 14), text_color=TEXT_DIM).pack(anchor="w", padx=20)
        master._ai_num_questions = ctk.CTkSlider(right, from_=3, to=20, number_of_steps=17, width=230)
        master._ai_num_questions.set(10)
        master._ai_num_questions.pack(padx=20, pady=5)
        master._ai_num_label = ctk.CTkLabel(right, text="10 pytań", font=("Arial", 14, "bold"), text_color=ACCENT_AI)
        master._ai_num_label.pack()
        master._ai_num_questions.configure(
            command=lambda v: master._ai_num_label.configure(text=f"{int(v)} pytań")
        )

        ctk.CTkFrame(right, height=1, fg_color=BG_CARD).pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(right, text="Model AI:", font=("Arial", 14), text_color=TEXT_DIM).pack(anchor="w", padx=20)
        master._ai_model_label = ctk.CTkLabel(
            right, text="llama3:latest\n(tekst / temat / plik)",
            font=("Arial", 12), text_color=TEXT_DIM, justify="center"
        )
        master._ai_model_label.pack(padx=20, pady=5)

        ctk.CTkFrame(right, height=1, fg_color=BG_CARD).pack(fill="x", padx=20, pady=15)

        master._ai_generate_btn = ctk.CTkButton(
            right, text="✦  Generuj pytania",
            font=("Arial", 16, "bold"),
            width=230, height=55,
            fg_color=ACCENT_AI, hover_color="#8a5eff",
            text_color=TEXT,
            command=lambda: self._start_generation(master)
        )
        master._ai_generate_btn.pack(padx=20, pady=10)

        master._ai_status_label = ctk.CTkLabel(
            right, text="", font=("Arial", 12),
            text_color=TEXT_DIM, wraplength=230
        )
        master._ai_status_label.pack(padx=20, pady=5)

        ctk.CTkFrame(right, height=1, fg_color=BG_CARD).pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            right, text="← Powrót do menu",
            font=("Arial", 14), width=230, height=40,
            fg_color=BG_CARD, hover_color=BG_FRAME,
            text_color=TEXT_DIM, border_width=1, border_color=TEXT_DIM,
            command=master.main_menu
        ).pack(padx=20, pady=10, side="bottom")


    def _switch_ai_source(self, master, source):
        master._ai_source_var.set(source)
        for val, btn in master._ai_tab_buttons.items():
            btn.configure(fg_color=ACCENT_AI if val == source else BG_CARD)
        for w in master._ai_source_content.winfo_children():
            w.destroy()

        handlers = {
            "temat":   (self._show_source_temat,   "llama3:latest\n(tekst / temat)"),
            "tekst":   (self._show_source_tekst,   "llama3:latest\n(tekst / temat)"),
            "plik":    (self._show_source_plik,    "llama3:latest\n(PDF / TXT)"),
            "zdjecie": (self._show_source_zdjecie, "llava:latest\n(⚠️ wymaga modelu Vision)"),
        }
        fn, model_text = handlers[source]
        fn(master)
        master._ai_model_label.configure(text=model_text)

    def _show_source_temat(self, master):
        ctk.CTkLabel(
            master._ai_source_content,
            text="Wpisz temat lub zakres materiału:",
            font=("Arial", 14), text_color=TEXT_DIM
        ).pack(anchor="w", pady=(5, 5))

        master._ai_topic_entry = ctk.CTkEntry(
            master._ai_source_content,
            placeholder_text="np. Fotosynteza, II Wojna Światowa, Gramatyka angielska...",
            font=("Arial", 14), height=45,
            fg_color=BG_CARD, text_color=TEXT,
            border_color=ACCENT_AI, border_width=1
        )
        master._ai_topic_entry.pack(fill="x", pady=5)

        ctk.CTkLabel(
            master._ai_source_content,
            text="Dodatkowe wskazówki dla AI (opcjonalne):",
            font=("Arial", 13), text_color=TEXT_DIM
        ).pack(anchor="w", pady=(15, 5))

        master._ai_topic_hints = self._make_placeholder_textbox(
            master._ai_source_content,
            placeholder="np. Skup się na datach, pytaj o przyczyny i skutki...",
            height=140
        )
        master._ai_topic_hints.pack(fill="x", pady=5)

    def _show_source_tekst(self, master):
        ctk.CTkLabel(
            master._ai_source_content,
            text="Wklej tekst lub notatki:",
            font=("Arial", 14), text_color=TEXT_DIM
        ).pack(anchor="w", pady=(5, 5))

        master._ai_text_input = self._make_placeholder_textbox(
            master._ai_source_content,
            placeholder="Wklej tutaj tekst, notatki, definicje...",
            height=320,
            border_color=ACCENT_AI
        )
        master._ai_text_input.pack(fill="both", expand=True, pady=5)

    def _show_source_plik(self, master):
        ctk.CTkLabel(
            master._ai_source_content,
            text="Wgraj plik PDF lub TXT:",
            font=("Arial", 14), text_color=TEXT_DIM
        ).pack(anchor="w", pady=(5, 5))

        master._ai_file_path = None

        file_row = ctk.CTkFrame(master._ai_source_content, fg_color="transparent")
        file_row.pack(fill="x", pady=5)

        master._ai_file_label = ctk.CTkLabel(
            file_row, text="Nie wybrano pliku",
            font=("Arial", 13), text_color=TEXT_DIM
        )
        master._ai_file_label.pack(side="left", fill="x", expand=True)

        ctk.CTkButton(
            file_row, text="📁  Wybierz plik",
            font=("Arial", 13, "bold"), width=160, height=40,
            fg_color=BG_CARD, hover_color=ACCENT_AI,
            text_color=TEXT, border_width=1, border_color=ACCENT_AI,
            command=lambda: self._pick_file(master)
        ).pack(side="right", padx=5)

        master._ai_file_preview = ctk.CTkTextbox(
            master._ai_source_content, height=220,
            font=("Arial", 12), fg_color=BG_CARD,
            text_color=TEXT_DIM, border_width=0, state="disabled"
        )
        master._ai_file_preview.pack(fill="both", expand=True, pady=10)

    def _show_source_zdjecie(self, master):
        ctk.CTkLabel(
            master._ai_source_content,
            text="Dodaj zdjęcia (JPG, PNG):",
            font=("Arial", 14), text_color=TEXT_DIM
        ).pack(anchor="w", pady=(5, 5))

        ctk.CTkLabel(
            master._ai_source_content,
            text="⚠️  Wymaga modelu Vision w Ollama\n      ollama pull llava:latest",
            font=("Arial", 12), text_color=ACCENT_WARN,
            fg_color=BG_CARD, corner_radius=8
        ).pack(fill="x", pady=(0, 10))

        master._ai_image_paths = []

        btn_row = ctk.CTkFrame(master._ai_source_content, fg_color="transparent")
        btn_row.pack(fill="x", pady=5)

        ctk.CTkButton(
            btn_row, text="🖼️  Dodaj zdjęcia",
            font=("Arial", 13, "bold"), width=160, height=40,
            fg_color=BG_CARD, hover_color=ACCENT_AI,
            text_color=TEXT, border_width=1, border_color=ACCENT_AI,
            command=lambda: self._pick_images(master)
        ).pack(side="left", padx=(0, 10))

        master._ai_img_count_label = ctk.CTkLabel(
            btn_row, text="Brak zdjęć",
            font=("Arial", 13), text_color=TEXT_DIM
        )
        master._ai_img_count_label.pack(side="left")

        master._ai_img_preview_frame = ctk.CTkScrollableFrame(
            master._ai_source_content,
            fg_color=BG_CARD, height=220,
            orientation="horizontal",
            scrollbar_button_color=ACCENT_AI,
            scrollbar_button_hover_color=BG_CARD
        )
        master._ai_img_preview_frame.pack(fill="both", expand=True, pady=10)


    def _pick_file(self, master):
        path = filedialog.askopenfilename(
            filetypes=[("PDF i TXT", "*.pdf *.txt"), ("PDF", "*.pdf"), ("TXT", "*.txt")]
        )
        if not path:
            return
        master._ai_file_path = path
        master._ai_file_label.configure(text=os.path.basename(path), text_color=ACCENT_SUCCESS)
        text = self._extract_file_text(path)
        preview = text[:2000] + ("..." if len(text) > 2000 else "")
        master._ai_file_preview.configure(state="normal")
        master._ai_file_preview.delete("1.0", "end")
        master._ai_file_preview.insert("1.0", preview)
        master._ai_file_preview.configure(state="disabled")

    def _pick_images(self, master):
        paths = filedialog.askopenfilenames(
            filetypes=[("Obrazy", "*.jpg *.jpeg *.png *.bmp")]
        )
        if not paths:
            return
        master._ai_image_paths = list(paths)
        count = len(paths)
        master._ai_img_count_label.configure(
            text=f"{count} {'zdjęcie' if count == 1 else 'zdjęcia/zdjęć'} załadowane",
            text_color=ACCENT_SUCCESS
        )
        for w in master._ai_img_preview_frame.winfo_children():
            w.destroy()
        master._ai_img_refs = []
        for path in paths[:10]:
            try:
                from PIL import Image as PILImage, ImageTk
                img = PILImage.open(path)
                img.thumbnail((110, 110))
                photo = ImageTk.PhotoImage(img)
                master._ai_img_refs.append(photo)
                card = ctk.CTkFrame(master._ai_img_preview_frame, fg_color=BG_FRAME, corner_radius=6)
                card.pack(side="left", padx=5, pady=5)
                ctk.CTkLabel(card, image=photo, text="").pack(padx=4, pady=4)
                ctk.CTkLabel(card, text=os.path.basename(path)[:16],
                             font=("Arial", 10), text_color=TEXT_DIM).pack(pady=(0, 4))
            except Exception:
                ctk.CTkLabel(master._ai_img_preview_frame,
                             text=os.path.basename(path), text_color=TEXT).pack(side="left", padx=5)

    def _extract_file_text(self, path):
        if path.lower().endswith(".txt"):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                return f"Błąd odczytu: {e}"
        elif path.lower().endswith(".pdf"):
            try:
                import pypdf
                reader = pypdf.PdfReader(path)
                return "".join(p.extract_text() or "" for p in reader.pages)
            except ImportError:
                pass
            try:
                import PyPDF2
                with open(path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    return "".join(p.extract_text() or "" for p in reader.pages)
            except ImportError:
                return "⚠️  Zainstaluj pypdf:\n    pip install pypdf"
            except Exception as e:
                return f"Błąd PDF: {e}"
        return ""

    def _start_generation(self, master):
        source = master._ai_source_var.get()
        num = int(master._ai_num_questions.get())
        content = ""
        images = []

        if source == "temat":
            topic = master._ai_topic_entry.get().strip()
            if not topic:
                messagebox.showwarning("Brak tematu", "Wpisz temat lub zakres materiału!")
                return
            hints = self._get_textbox_value(master._ai_topic_hints)
            content = f"Temat: {topic}"
            if hints:
                content += f"\nWskazówki: {hints}"

        elif source == "tekst":
            content = self._get_textbox_value(master._ai_text_input)
            if not content:
                messagebox.showwarning("Brak tekstu", "Wklej tekst lub notatki!")
                return

        elif source == "plik":
            if not getattr(master, "_ai_file_path", None):
                messagebox.showwarning("Brak pliku", "Wybierz plik PDF lub TXT!")
                return
            content = self._extract_file_text(master._ai_file_path)
            if not content or content.startswith("⚠️") or content.startswith("Błąd"):
                messagebox.showerror("Błąd pliku", content or "Nie udało się odczytać pliku.")
                return

        elif source == "zdjecie":
            if not getattr(master, "_ai_image_paths", []):
                messagebox.showwarning("Brak zdjęć", "Dodaj przynajmniej jedno zdjęcie!")
                return
            images = master._ai_image_paths
            content = f"Wygeneruj {num} pytań na podstawie przesłanych zdjęć."

        master._ai_generate_btn.configure(state="disabled", text="⏳  Generuję...")
        master._ai_status_label.configure(text="⏳ Łączenie z modelem…", text_color=ACCENT_AI)

        def on_progress(found, total):
            master.after(0, lambda f=found, t=total: master._ai_status_label.configure(
                text=f"⚙️  Generuję… {f} / {t} pytań",
                text_color=ACCENT_AI
            ))

        from ai_helper import generuj_pytania_quiz
        generuj_pytania_quiz(
            content=content,
            num=num,
            images=images,
            callback_done=lambda qs: master.after(0, lambda: self._show_preview(master, qs)),
            callback_error=lambda err: master.after(0, lambda: self._on_generation_error(master, err)),
            callback_progress=on_progress
        )

    def _on_generation_error(self, master, error):
        master._ai_generate_btn.configure(state="normal", text="✦  Generuj pytania")
        error_lower = error.lower()
        if "connection" in error_lower or "refused" in error_lower or "connect" in error_lower:
            msg = "❌ Nie można połączyć się z Ollama.\nUpewnij się że serwer działa:\n  ollama serve"
        elif "not found" in error_lower or "model" in error_lower:
            msg = "❌ Model nie znaleziony.\nPobierz go:\n  ollama pull llama3:latest"
        elif "json" in error_lower:
            msg = "❌ AI zwróciło nieprawidłową odpowiedź.\nSpróbuj ponownie."
        else:
            msg = f"❌ {error}"
        master._ai_status_label.configure(text=msg, text_color=ACCENT_ERROR)


    def _show_preview(self, master, questions):
        if not questions:
            self._on_generation_error(master, "AI nie zwróciło pytań. Spróbuj ponownie.")
            return

        master._ai_generate_btn.configure(state="normal", text="✦  Generuj pytania")
        master._ai_status_label.configure(
            text=f"✓ Wygenerowano {len(questions)} pytań!", text_color=ACCENT_SUCCESS
        )

        master.ai_generator_frame.pack_forget()

        master.ai_preview_frame = ctk.CTkFrame(master, fg_color="transparent")
        master.ai_preview_frame.pack(fill="both", expand=True, padx=40, pady=20)

        header = ctk.CTkFrame(master.ai_preview_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            header,
            text=f"✦  Podgląd pytań  ({len(questions)})",
            font=("Arial", 24, "bold"), text_color=ACCENT_AI
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="Możesz edytować każde pytanie przed zapisem",
            font=("Arial", 13), text_color=TEXT_DIM
        ).pack(side="left", padx=20)

        btn_row = ctk.CTkFrame(header, fg_color="transparent")
        btn_row.pack(side="right")

        ctk.CTkButton(
            btn_row, text="← Powrót do generatora",
            font=("Arial", 13), width=210, height=40,
            fg_color=BG_CARD, hover_color=BG_FRAME,
            text_color=TEXT_DIM, border_width=1, border_color=TEXT_DIM,
            command=lambda: self._back_to_generator(master)
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_row, text="💾  Zapisz jako nowy test",
            font=("Arial", 14, "bold"), width=230, height=40,
            fg_color=ACCENT_SUCCESS, hover_color="#2aaa60",
            text_color=BG_MAIN,
            command=lambda: self._save_generated_test(master)
        ).pack(side="left", padx=5)

        scroll = ctk.CTkScrollableFrame(
            master.ai_preview_frame, fg_color=BG_FRAME,
            scrollbar_button_color=ACCENT_AI,
            scrollbar_button_hover_color=BG_CARD
        )
        scroll.pack(fill="both", expand=True)

        master._ai_preview_entries = []
        for i, q in enumerate(questions):
            self._render_question_card(master, scroll, i, q)

    def _render_question_card(self, master, parent, i, q):
        card = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=10)
        card.pack(fill="x", padx=20, pady=8)

        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.pack(fill="x", padx=12, pady=(8, 0))

        ctk.CTkLabel(
            top_row, text=f"Pytanie {i + 1}",
            font=("Arial", 13, "bold"), text_color=ACCENT_AI
        ).pack(side="left")

        ctk.CTkButton(
            top_row, text="✕", width=30, height=30,
            fg_color="transparent", hover_color=ACCENT_ERROR,
            text_color=ACCENT_ERROR, border_width=0,
            command=lambda c=card, idx=i: self._delete_preview_question(master, c, idx)
        ).pack(side="right")

        q_entry = ctk.CTkEntry(
            card, font=("Arial", 14),
            fg_color=BG_FRAME, text_color=TEXT,
            border_color=ACCENT_AI, border_width=1, height=42
        )
        q_entry.pack(fill="x", padx=12, pady=6)
        q_entry.insert(0, q.get("pytanie", ""))

        opts_frame = ctk.CTkFrame(card, fg_color="transparent")
        opts_frame.pack(fill="x", padx=12, pady=4)

        opt_entries = {}
        for litera in ["A", "B", "C", "D"]:
            row = ctk.CTkFrame(opts_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"{litera}:", font=("Arial", 13, "bold"),
                         text_color=TEXT_DIM, width=25).pack(side="left")
            opt_e = ctk.CTkEntry(row, font=("Arial", 13),
                                 fg_color=BG_FRAME, text_color=TEXT,
                                 border_color=BG_FRAME, border_width=1, height=36)
            opt_e.pack(side="left", fill="x", expand=True, padx=5)
            opt_e.insert(0, q.get("opcje", {}).get(litera, ""))
            opt_entries[litera] = opt_e

        correct_row = ctk.CTkFrame(card, fg_color="transparent")
        correct_row.pack(fill="x", padx=12, pady=(4, 12))

        ctk.CTkLabel(correct_row, text="Poprawna:",
                     font=("Arial", 13), text_color=TEXT_DIM).pack(side="left")

        correct_var = ctk.StringVar(value=q.get("poprawna", "A"))
        for litera in ["A", "B", "C", "D"]:
            ctk.CTkRadioButton(
                correct_row, text=litera,
                variable=correct_var, value=litera,
                font=("Arial", 13, "bold"),
                text_color=ACCENT_SUCCESS, fg_color=ACCENT_SUCCESS
            ).pack(side="left", padx=8)

        master._ai_preview_entries.append({
            "card": card,
            "pytanie": q_entry,
            "opcje": opt_entries,
            "poprawna": correct_var,
            "deleted": False,
        })

    def _delete_preview_question(self, master, card, index):
        card.pack_forget()
        if index < len(master._ai_preview_entries):
            master._ai_preview_entries[index]["deleted"] = True

    def _back_to_generator(self, master):
        if hasattr(master, "ai_preview_frame") and master.ai_preview_frame.winfo_exists():
            master.ai_preview_frame.pack_forget()
        master.ai_generator_frame.pack(fill="both", expand=True, padx=40, pady=20)
        master._ai_generate_btn.configure(state="normal", text="✦  Generuj pytania")
        master._ai_status_label.configure(text="")

    def _save_generated_test(self, master):
        final_questions = []
        for entry in master._ai_preview_entries:
            if entry.get("deleted"):
                continue
            pytanie = entry["pytanie"].get().strip()
            opcje = {l: entry["opcje"][l].get().strip() for l in ["A", "B", "C", "D"]}
            poprawna = entry["poprawna"].get()
            if pytanie:
                final_questions.append({
                    "pytanie": pytanie,
                    "opcje": opcje,
                    "poprawna": poprawna,
                    "licznik": 0
                })

        if not final_questions:
            messagebox.showwarning("Puste", "Brak pytań do zapisania!")
            return

        name = ctk.CTkInputDialog(
            text=f"Podaj nazwę nowego testu ({len(final_questions)} pytań):",
            title="Zapisz test"
        ).get_input()

        if not name or not name.strip():
            return

        name = name.strip()
        folder = "database"
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, f"{name}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(final_questions, f, indent=4, ensure_ascii=False)

        from database import save_config
        save_config(name, file_path)

        messagebox.showinfo("Sukces! ✦", f"Test \"{name}\" zapisany z {len(final_questions)} pytaniami!")

        if hasattr(master, "ai_preview_frame") and master.ai_preview_frame.winfo_exists():
            master.ai_preview_frame.pack_forget()

        master.main_menu()
        master._rebuild_tests_display()


    def _hide_all_for_ai(self, master):
        widgets = [
            "footer_frame", "button_restart_frame", "progressbar",
            "pytania_label", "pytanie", "button_go_back_to_menu_frame",
            "buttons_frame", "open_question_frame", "new_tests_frame",
            "add_test_button_frame", "add_test_through_ai_frame",
            "menu_button_frame", "signature_label",
            "action_buttons_frame", "action_buttons_frame2", "stats_frame",
            "total_questions_label", "go_back_to_edit_menu_btn",
            "change_question_frame", "add_question_menu_frame",
            "add_question_open_frame", "edit_question_menu_frame",
            "edit_question_open_frame", "last_results_btn", "last_results_frame",
            "show_bledy_btn", "bledy_frame", "restart_test_bledy",
            "ai_frame", "center_frame",
            "ai_generator_frame", "ai_preview_frame",
        ]
        for name in widgets:
            w = getattr(master, name, None)
            if w:
                try:
                    w.pack_forget()
                except Exception:
                    pass