# Exam Tester

<img src="https://raw.githubusercontent.com/oliwiermaziarzT/ExamTester/main/videos/vid2.gif" width="600"/>

Desktopowa aplikacja do nauki i przygotowania do egzaminów. Umożliwia tworzenie własnych testów, rozwiązywanie pytań zamkniętych i otwartych, śledzenie postępów nauki oraz korzystanie z lokalnego modelu AI do wyjaśniania odpowiedzi. Napisana w Pythonie z interfejsem graficznym CustomTkinter.

---

## Funkcje

- **Zarządzanie testami** — tworzenie testów, przypisywanie plików `.json` z pytaniami, usuwanie
- **Dwa typy pytań** — zamknięte (A/B/C/D) z losową kolejnością odpowiedzi oraz otwarte (wpisywanie tekstu)
- **Edytor pytań** — dodawanie, edytowanie i usuwanie pytań bezpośrednio z poziomu aplikacji
- **Statystyki w czasie rzeczywistym** — poprawne/niepoprawne odpowiedzi, procent, wykresy kołowe postępu nauki
- **System powtórek** — pytania słabiej opanowane (niski licznik) pojawiają się częściej
- **Przegląd błędów** — lista pytań z błędnymi odpowiedziami z ostatniej sesji wraz z poprawnymi odpowiedziami
- **Integracja z AI (Ollama)** — wyjaśnienia odpowiedzi i możliwość zadania własnego pytania po każdej odpowiedzi
- **Ciemny motyw** — przyjazny dla oczu interfejs

---

## Instalacja

### Wymagania

- Python 3.8+
- [Ollama](https://ollama.com) z pobranym modelem (opcjonalne, tylko do funkcji AI)

### Kroki

1. Sklonuj repozytorium:
```bash
git clone https://github.com/oliwiermaziarzT/ExamTester.git
cd ExamTester
```

2. Utwórz i aktywuj wirtualne środowisko:
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Zainstaluj zależności:
```bash
pip install customtkinter matplotlib ollama
```

4. Uruchom aplikację:
```bash
python main.py
```

### Konfiguracja AI (opcjonalne)

Jeśli chcesz korzystać z pomocy AI, uruchom Ollama i pobierz model:
```bash
ollama serve
ollama pull llama3:latest
```

---

<img src="https://raw.githubusercontent.com/oliwiermaziarzT/ExamTester/main/videos/vid1.gif" width="600"/>

## Pierwsze kroki

1. **Dodaj test** — kliknij „Dodaj test" i podaj nazwę. Zostanie utworzony plik `.json` z przykładowymi pytaniami.
2. **Automatyczne przypisanie pliku** — po utworzeniu testu automatycznie przypisywany jest do niego plik `.json` z taką samą nazwą jak test.
3. **Przypisz plik** — jeżeli masz gotowy plik `.json` z pytaniami, kliknij przycisk 📁 przy teście i wskaż ten plik.
4. **Rozpocznij naukę** — kliknij wybrany test, a następnie „Rozpocznij Test".
5. **Odpowiadaj** — wybierz odpowiedź A/B/C/D lub wpisz tekst w pytaniach otwartych.
6. **Śledź postępy** — statystyki na dole ekranu pokazują wynik bieżącej sesji i ogólny postęp nauki.

---

## Pomoc AI

Po udzieleniu odpowiedzi pojawia się panel **Pomocnik AI**. Dostępne opcje:

- **Wyjaśnij odpowiedź** — AI generuje krótkie uzasadnienie dlaczego dana odpowiedź jest prawidłowa
- **Wyślij pytanie** — zadaj własne pytanie dotyczące bieżącego zagadnienia
- **Wyczyść** — usuwa odpowiedź AI z panelu

Funkcja wymaga uruchomionego serwisu Ollama z pobranym modelem.

---

## Technologie

| Biblioteka | Zastosowanie |
|---|---|
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | Interfejs graficzny |
| [Matplotlib](https://matplotlib.org) | Wykresy statystyk |
| [Ollama](https://ollama.com) | Lokalny model językowy AI |
| JSON | Format przechowywania pytań i konfiguracji |

---

## Struktura projektu

```
├── main.py           # Punkt wejścia, główna klasa App
├── gui.py            # Łącznik interfejsów 
├── gui_menu.py       # Widok menu głównego
├── gui_quiz.py       # Widok rozwiązywania testu + panel AI
├── gui_edit.py       # Widok edytora pytań
├── quiz_logic.py     # Logika rozwiązywania testu
├── edit_logic.py     # Logika edycji pytań
├── menu_logic.py     # Logika zarządzania testami
├── database.py       # Operacje na plikach JSON
├── ollama_helper.py  # Komunikacja z Ollama
├── config.json       # Lista zapisanych testów
└── baza.json         # Przykładowa baza pytań
```

---

## 👤 Autor

Stworzone przez **Oliwier Maziarz** jako narzędzie do samodzielnej nauki.

## Dlaczego ten projekt?

Projekt został stworzony, ponieważ na studiach było bardzo wiele przedmiotów z gotową bazą pytań, ale brakowało narzędzia do efektywnej nauki - popularna aplikacja Anki mi nie odpowiadała. Chciałem mieć możliwość tworzenia własnych testów, śledzenia postępów i korzystania z pomocy AI, a dostępne rozwiązania były zbyt ograniczone lub skomplikowane. Chciałem stworzyć coś co jest bardzo proste w obsłudze oraz przyjemne dla oka. Ten projekt to moja odpowiedź na te potrzeby. Obecnie służy mi głównie do nauki języka hiszpańskiego.

## Dalsze plany rozwoju
Kolejność losowa:

- **Tryb tylko nienauczone** — możliwość rozwiązywania tylko pytań z niskim licznikiem
- **Tryb powtórka błędów** — rozwiązywanie tylko pytań z ostatniej sesji, które zostały źle odpowiedziane
- **Eksport wyników** — możliwość eksportowania statystyk do pliku CSV/PDF
- **Więcej typów pytań** —  pytania z wieloma poprawnymi odpowiedziami, pytania z obrazkami
- **Wykres postępów w czasie** — linie pokazujące jak procent poprawnych odpowiedzi zmienia się w kolejnych sesjach
- **Generowanie testów po przez AI** — możliwość wygenerowania testu na podstawie podanego tematu/zakresu materiału/pliku z pytaniami
- **Zapisywanie postępów w chmurze** — synchronizacja wyników i testów między urządzeniami (np. Google Drive, Dropbox)
- **API AI** - usunięcie lokalnego AI
- **Speech recognition** - ćwiczenie poprawnej wymowy ( to specyficzna funkcjonalność dla mnie do jęyzka hiszpańskiego )
-- **Aplikacja mobilna** — uproszczona wersja aplikacji na Androida/iOS do nauki w ruchu (w bardzo bardzo odległej przyszłości "😉")

## Licencja

Projekt udostępniony na licencji [MIT](LICENSE). Możesz go używać, modyfikować i rozpowszechniać dowolnie.
