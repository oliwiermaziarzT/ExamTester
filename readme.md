Aplikacja do nauki
Aplikacja desktopowa wspomagająca przygotowania do egzaminów – umożliwia tworzenie własnych testów, rozwiązywanie pytań zamkniętych i otwartych, śledzenie postępów oraz korzystanie z pomocy sztucznej inteligencji (AI) do wyjaśniania odpowiedzi. Napisana w Pythonie z wykorzystaniem interfejsu graficznego CustomTkinter.

<video src="videos/vid2.mp4" controls width="600"></video>

✨ Funkcje
✅ Tworzenie i zarządzanie testami – dodawanie własnych testów, przypisywanie plików .json z pytaniami.

✅ Dwa typy pytań – zamknięte (A, B, C, D) oraz otwarte (wpisywanie odpowiedzi).

✅ Edytor pytań – dodawanie, modyfikacja i usuwanie pytań z poziomu aplikacji.

✅ Statystyki w czasie rzeczywistym – liczba poprawnych/niepoprawnych odpowiedzi, postęp nauki (licznik), wykresy kołowe.

✅ System powtórek – pytania z niskim licznikiem są wyświetlane częściej, co wspomaga zapamiętywanie.

✅ Przegląd błędów – lista pytań, na które udzielono złej odpowiedzi w ostatniej sesji.

✅ Integracja z AI (Ollama) – po każdej odpowiedzi możesz poprosić o wyjaśnienie, dlaczego dana odpowiedź jest prawidłowa, lub zadać własne pytanie dotyczące bieżącego zagadnienia.

✅ Ciemny motyw – przyjazny dla oczu interfejs z możliwością personalizacji kolorów.

<video src="videos/vid1.mp4" controls width="600"></video>

🚀 Instalacja i uruchomienie
Wymagania
Python 3.8 lub nowszy

Ollama (jeśli chcesz korzystać z pomocy AI) z pobranym modelem, np. llama3

Kroki
Sklonuj repozytorium:

bash
git clone https://github.com/twoja_nazwa/nazwa_repo.git
cd nazwa_repo
(Zalecane) Utwórz i aktywuj wirtualne środowisko:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Zainstaluj wymagane pakiety:

bash
pip install customtkinter matplotlib ollama
Uwaga: customtkinter i matplotlib to główne biblioteki GUI i wykresów, ollama to klient do komunikacji z lokalnym modelem AI.

Upewnij się, że Ollama działa (jeśli chcesz używać AI):

bash
ollama serve
a następnie pobierz model:

bash
ollama pull llama3:latest
Uruchom aplikację:

bash
python main.py
📖 Pierwsze kroki
Dodaj test – kliknij przycisk „Dodaj test”, podaj nazwę. Zostanie utworzony plik .json z przykładowymi pytaniami.

Przypisz plik – przy każdym teście kliknij ikonę 📁 i wskaż plik .json (możesz go później edytować ręcznie lub przez wbudowany edytor).

Rozpocznij naukę – wybierz test z listy i kliknij „Rozpocznij Test”.

Odpowiadaj na pytania – wybieraj odpowiedzi w pytaniach zamkniętych lub wpisz tekst w otwartych. Po każdej odpowiedzi zobaczysz poprawną wersję oraz możesz poprosić AI o wyjaśnienie.

Edytuj pytania – w menu testu kliknij „Zmień lub usuń pytanie”, aby przeglądać, modyfikować lub usuwać pytania.

Śledź postępy – na dole ekranu znajdują się statystyki: poprawne/niepoprawne, procent, liczba pytań nauczonych (licznik > 2) i nienauczonych.

🧠 Pomoc AI
Po udzieleniu odpowiedzi na pytanie pojawi się panel „Pomocnik AI”. Możesz:

Kliknąć „Wyjaśnij odpowiedź” – AI wygeneruje krótkie uzasadnienie, dlaczego poprawna odpowiedź jest właściwa.

Wpisać własne pytanie w polu tekstowym i kliknąć „Wyślij pytanie” – otrzymasz odpowiedź na pytanie dotyczące bieżącego zagadnienia.

Kliknąć „Wyczyść”, by usunąć odpowiedź AI.

Wymaga to uruchomionego serwisu Ollama z modelem.

🛠️ Technologie
Python – język programowania

CustomTkinter – nowoczesny framework GUI

Matplotlib – wykresy statystyk

JSON – format przechowywania pytań

Ollama – lokalna integracja z modelami językowymi

📁 Struktura projektu
text
├── main.py                # Punkt wejścia, główna klasa App
├── gui.py                 # Połączenie interfejsów
├── gui_menu.py            # Widoki menu
├── gui_quiz.py            # Widoki rozwiązywania testu
├── gui_edit.py            # Widoki edytora pytań
├── quiz_logic.py          # Logika rozwiązywania testu
├── edit_logic.py          # Logika edycji pytań
├── menu_logic.py          # Logika zarządzania testami
├── database.py            # Operacje na plikach JSON
├── ollama_helper.py       # Komunikacja z Ollama
├── config.json            # Lista zapisanych testów
└── baza.json              # Przykładowa baza pytań
👤 Autor
Stworzone przez Oliwier Maziarz.
Aplikacja powstała jako narzędzie do samodzielnej nauki i może być dowolnie rozwijana.

📄 Licencja
Projekt udostępniony na licencji MIT. Możesz go używać, modyfikować i rozpowszechniać zgodnie z jej warunkami.