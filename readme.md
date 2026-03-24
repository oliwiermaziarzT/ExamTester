# Exam Tester

![Demo](https://github.com/oliwiermaziarzT/ExamTester/blob/main/videos/vid2.gif)

Desktopowa aplikacja do nauki i przygotowania do egzaminów. Umożliwia tworzenie własnych testów, rozwiązywanie pytań zamkniętych i otwartych, śledzenie postępów nauki oraz korzystanie z AI (Groq API) do wyjaśniania odpowiedzi i automatycznego generowania testów. Napisana w Pythonie z interfejsem graficznym CustomTkinter.

---

## Funkcje

- **Zarządzanie testami** — tworzenie testów, przypisywanie plików `.json` z pytaniami, usuwanie, grupowanie w kategorie
- **Dwa typy pytań** — zamknięte (A/B/C/D) oraz otwarte (wpisywanie tekstu)
- **Edytor pytań** — dodawanie, edytowanie i usuwanie pytań bezpośrednio z poziomu aplikacji
- **Statystyki w czasie rzeczywistym** — poprawne/niepoprawne odpowiedzi, procent, wykresy kołowe postępu nauki
- **Przegląd błędów** — lista pytań z błędnymi odpowiedziami z ostatniej sesji wraz z poprawnymi odpowiedziami
- **Pomoc AI (Groq)** — wyjaśnienia odpowiedzi i możliwość zadania własnego pytania po każdej odpowiedzi
- **Generator testów przez AI** — automatyczne tworzenie pytań zamkniętych A/B/C/D z czterech źródeł: tematu, tekstu, pliku PDF/TXT lub zdjęcia
- **Podgląd i edycja przed zapisem** — wygenerowane pytania można edytować i usuwać przed zapisaniem testu

---

## Instalacja

### Wymagania

- Python 3.8+
- Klucz API Groq (bezpłatny, do funkcji AI) — uzyskasz go na [console.groq.com](https://console.groq.com)

### Kroki

1. Sklonuj repozytorium:
```bash
git clone https://github.com/oliwiermaziarzT/ExamTester.git
cd ExamTester
```

2. Utwórz i aktywuj wirtualne środowisko:
```bash
python -m venv venv
source venv/bin/activate         
```

3. Zainstaluj zależności:
```bash
pip install customtkinter matplotlib groq pypdf pillow
```

4. Uruchom aplikację:
```bash
python main.py
```

### Konfiguracja AI

1. Zarejestruj się na [console.groq.com](https://console.groq.com) i wygeneruj bezpłatny klucz API.
2. Uruchom aplikację i wpisz klucz w polu **Groq API Key** w menu głównym.
3. Klucz zostanie zapamiętany lokalnie w pliku `groq_api_key.txt`.

---

![Demo](https://github.com/oliwiermaziarzT/ExamTester/blob/main/videos/vid1.gif)

## Pierwsze kroki

1. **Dodaj test** — kliknij „Dodaj test" i podaj nazwę. Zostanie utworzony plik `.json` z przykładowymi pytaniami.
2. **Automatyczne przypisanie pliku** — po utworzeniu testu automatycznie przypisywany jest do niego plik `.json` z taką samą nazwą jak test.
3. **Przypisz plik** — jeżeli masz gotowy plik `.json` z pytaniami, kliknij przycisk 📁 przy teście i wskaż ten plik.
4. **Przypisz kategorię** — kliknij przycisk 🏷 przy teście, aby przypisać go do kategorii. Testy są grupowane nagłówkami kategorii w menu.
5. **Rozpocznij naukę** — kliknij wybrany test, a następnie „Rozpocznij Test".
6. **Odpowiadaj** — wybierz odpowiedź A/B/C/D lub wpisz tekst w pytaniach otwartych.
7. **Śledź postępy** — statystyki na dole ekranu pokazują wynik bieżącej sesji i ogólny postęp nauki.

---

## Generator testów przez AI 
Wszystko związane z tą funkcją zostało stworzone w 100% przez sztuczną inteligencję - ta funkcja powstała, ponieważ ułatwia mi ona naukę, a na mój obecny poziom to zadanie wydawało się zbyt cieżkie żeby samemu ją napisać.
______________________________________________________________________________________________________________________

Kliknij **„Dodaj test przez AI"** w menu głównym, aby automatycznie wygenerować test zamknięty (A/B/C/D).

### Źródła materiału

| Źródło | Opis |
|--------|------|
|  **Temat** | Wpisz temat lub zakres materiału. Możesz dodać opcjonalne wskazówki dla AI. |
|  **Tekst** | Wklej gotowe notatki, definicje lub dowolny tekst — AI wygeneruje pytania na jego podstawie. |
|  **Plik** | Wgraj plik PDF lub TXT. Aplikacja automatycznie odczyta tekst i przekaże go do modelu. |
|  **Zdjęcie** | Dodaj zdjęcia (JPG, PNG) — funkcja eksperymentalna, aktualnie wymaga ręcznego przepisania tekstu ze zdjęcia. |

### Przebieg generowania

1. Wybierz źródło i ustaw liczbę pytań (3–20) za pomocą suwaka.
2. Kliknij **„Generuj pytania"** — postęp generowania jest widoczny na bieżąco.
3. Przejrzyj wygenerowane pytania w **podglądzie** — każde pytanie i każdą odpowiedź możesz edytować lub usunąć.
4. Kliknij **„Zapisz jako nowy test"** i podaj nazwę — test pojawi się od razu w menu głównym.

---

## Pomoc AI

Po udzieleniu odpowiedzi pojawia się panel **Pomocnik AI**. Dostępne opcje:

- **Wyjaśnij odpowiedź** — AI generuje krótkie uzasadnienie, dlaczego dana odpowiedź jest prawidłowa
- **Wyślij pytanie** — zadaj własne pytanie dotyczące bieżącego zagadnienia
- **Wyczyść** — usuwa odpowiedź AI z panelu

Funkcja wymaga zapisanego klucza Groq API. Model: `llama-3.1-8b-instant`.

---

## Technologie

| Biblioteka | Zastosowanie |
|---|---|
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | Interfejs graficzny |
| [Matplotlib](https://matplotlib.org) | Wykresy statystyk |
| [Groq](https://console.groq.com) | API do modelu językowego AI (llama-3.1-8b-instant) |
| [pypdf](https://pypdf.readthedocs.io) | Odczyt plików PDF w generatorze AI |
| [Pillow](https://python-pillow.org) | Podgląd zdjęć w generatorze AI |
| JSON | Format przechowywania pytań i konfiguracji |

---

## Struktura projektu

```
├── main.py               # Punkt wejścia, główna klasa App
├── gui.py                # Łącznik interfejsów
├── gui_menu.py           # Widok menu głównego
├── gui_quiz.py           # Widok rozwiązywania testu + panel AI
├── gui_edit.py           # Widok edytora pytań
├── gui_ai_generator.py   # Widok generatora testów przez AI
├── quiz_logic.py         # Logika rozwiązywania testu
├── edit_logic.py         # Logika edycji pytań
├── menu_logic.py         # Logika zarządzania testami
├── ai_helper.py          # Komunikacja z Groq API
├── database.py           # Operacje na plikach JSON
├── config.json           # Lista zapisanych testów
├── groq_api_key.txt      # Klucz API Groq (tworzony automatycznie)
└── baza.json             # Przykładowa baza pytań
```

---

## 👤 Autor

Stworzone przez **Oliwier Maziarz** jako narzędzie do samodzielnej nauki.

## Dlaczego ten projekt?

Projekt został stworzony, ponieważ na studiach było bardzo wiele przedmiotów z gotową bazą pytań, ale brakowało narzędzia do efektywnej nauki — popularna aplikacja Anki ani jej odpowiedniki mi nie odpowiadały. Chciałem mieć możliwość tworzenia własnych testów, śledzenia postępów i korzystania z pomocy AI, a dostępne rozwiązania były zbyt ograniczone lub skomplikowane. Ten projekt to moja odpowiedź na te potrzeby. Obecnie służy mi głównie do nauki języka hiszpańskiego.

## Dalsze plany rozwoju

Kolejność losowa:

- **Speech recognition** — ćwiczenie poprawnej wymowy i rozumienia ze słuchu (w przypadku nauki języków)
- **Generator pytań otwartych** — rozszerzenie generatora AI o typ pytania otwartego
- **Obsługa zdjęć w generatorze AI** — pełna integracja analizy obrazów po stronie API
- **Zapisywanie postępów w chmurze** — synchronizacja wyników i testów między urządzeniami

---

## Licencja

Projekt udostępniony na licencji [MIT](LICENSE). Możesz go używać, modyfikować i rozpowszechniać dowolnie.
