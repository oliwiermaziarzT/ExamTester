import threading
import difflib

GROQ_MODEL = "llama-3.1-8b-instant"   # szybki i darmowy

# System prompt do wyjaśniania odpowiedzi (zwięzły)
SYSTEM_PROMPT_EXPLAIN = """
Jesteś pomocnym tutorem pomagającym w nauce do egzaminów.

Zasady:
- Odpowiadaj wyłącznie po polsku
- Maksymalnie 60 słów
- Konkretnie i na temat — tylko wyjaśnienie danego pytania
- Nie przedstawiaj się ani nie komentuj swojej roli
- Nie powtarzaj treści pytania

Jeśli odpowiedź poprawna: zacznij od "Dobrze! ..." i wyjaśnij krótko dlaczego.
Jeśli błąd: zacznij od "Błąd. Poprawna odpowiedź to: [odpowiedź]. ..." i wyjaśnij dlaczego.
"""

# System prompt do własnych pytań użytkownika (bardziej rozbudowany)
SYSTEM_PROMPT_CHAT = """
Jesteś pomocnym tutorem pomagającym w nauce do egzaminów.

Zasady:
- Odpowiadaj wyłącznie po polsku
- Maksymalnie 120 słów
- Odpowiadaj bezpośrednio na pytanie użytkownika w kontekście danego zagadnienia
- Używaj prostego, zrozumiałego języka
- Możesz podać przykład jeśli to pomoże w zrozumieniu
- Nie przedstawiaj się ani nie komentuj swojej roli
"""


SYSTEM_PROMPT = SYSTEM_PROMPT_EXPLAIN



def get_api_key():
    """Odczytuje klucz Groq z config.json."""
    import json, os
    config_file = "config.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data.get("groq_api_key", "").strip()
            # config.json to lista testów — szukaj w osobnym pliku
        except Exception:
            pass
    # fallback: osobny plik
    key_file = "groq_api_key.txt"
    if os.path.exists(key_file):
        try:
            with open(key_file, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            pass
    return ""


def save_api_key(key):
    """Zapisuje klucz Groq do groq_api_key.txt (obok config.json z testami)."""
    try:
        with open("groq_api_key.txt", "w", encoding="utf-8") as f:
            f.write(key.strip())
    except Exception:
        pass


def _get_groq_client():
    """Zwraca klienta Groq lub rzuca wyjątek z czytelnym komunikatem."""
    try:
        from groq import Groq
    except ImportError:
        raise RuntimeError(
            "Biblioteka groq nie jest zainstalowana.\n"
            "Uruchom: pip install groq"
        )
    key = get_api_key()
    if not key:
        raise RuntimeError(
            "Brak klucza API Groq.\n"
            "Wpisz klucz w polu 'Groq API Key' w menu głównym.\n"
            "Klucz możesz uzyskać bezpłatnie na console.groq.com"
        )
    return Groq(api_key=key)



def normalizuj(txt):
    return txt.lower().strip()


def czy_poprawne(twoja, poprawna):
    twoja = normalizuj(twoja)
    poprawna = normalizuj(poprawna)
    similarity = difflib.SequenceMatcher(None, twoja, poprawna).ratio()
    return similarity > 0.85



def zapytaj_ollame(prompt, callback_chunk, callback_done, callback_error=None, mode="explain"):

    system = SYSTEM_PROMPT_CHAT if mode == "chat" else SYSTEM_PROMPT_EXPLAIN
    max_tok = 200 if mode == "chat" else 120

    def run():
        try:
            client = _get_groq_client()
            stream = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user",   "content": prompt}
                ],
                max_tokens=max_tok,
                temperature=0.3,
                stream=True
            )
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    callback_chunk(delta.content)
            callback_done()

        except Exception as e:
            if callback_error:
                callback_error(str(e))
            else:
                callback_done()

    threading.Thread(target=run, daemon=True).start()



def zbuduj_prompt_quiz(pytanie, opcje, poprawna, twoja, typ):
    if typ == "otwarte":
        poprawne = czy_poprawne(twoja, poprawna)
        if poprawne:
            return (
                f"Pytanie: {pytanie}\n"
                f"Odpowiedź użytkownika: {twoja}\n"
                f"Wzorcowa odpowiedź: {poprawna}\n\n"
                f"Odpowiedź jest poprawna. "
                f"Wyjaśnij w 1-2 zdaniach co sprawdza to pytanie i dlaczego ta odpowiedź jest prawidłowa."
            )
        else:
            return (
                f"Pytanie: {pytanie}\n"
                f"Odpowiedź użytkownika: {twoja}\n"
                f"Poprawna odpowiedź: {poprawna}\n\n"
                f"Odpowiedź jest błędna. "
                f"Wyjaśnij konkretnie co jest nie tak w odpowiedzi użytkownika "
                f"i dlaczego poprawna odpowiedź to \"{poprawna}\"."
            )
    else:
        opcje_str = ", ".join([f"{k}) {v}" for k, v in opcje.items()])
        poprawna_tresc = opcje.get(poprawna, "")
        twoja_tresc = opcje.get(twoja, twoja)
        poprawne = normalizuj(twoja) == normalizuj(poprawna)

        if poprawne:
            return (
                f"Pytanie: {pytanie}\n"
                f"Opcje: {opcje_str}\n"
                f"Wybrana i poprawna odpowiedź: {poprawna}) {poprawna_tresc}\n\n"
                f"Odpowiedź jest poprawna. "
                f"Wyjaśnij w 1-2 zdaniach dlaczego {poprawna}) jest prawidłową odpowiedzią "
                f"i co odróżnia ją od pozostałych opcji."
            )
        else:
            return (
                f"Pytanie: {pytanie}\n"
                f"Opcje: {opcje_str}\n"
                f"Odpowiedź użytkownika: {twoja}) {twoja_tresc}\n"
                f"Poprawna odpowiedź: {poprawna}) {poprawna_tresc}\n\n"
                f"Odpowiedź jest błędna. "
                f"Wyjaśnij dlaczego {poprawna}) jest poprawna, "
                f"a {twoja}) jest niepoprawna. Bądź konkretny."
            )


def zbuduj_prompt_wytlumacz(pytanie, opcje, poprawna, typ):
    """Prompt gdy użytkownik jeszcze nie odpowiedział — tylko wyjaśnienie zagadnienia."""
    if typ == "otwarte":
        return (
            f"Pytanie: {pytanie}\n"
            f"Wzorcowa odpowiedź: {poprawna}\n\n"
            f"Wyjaśnij o co pyta to pytanie i co jest kluczem do poprawnej odpowiedzi. "
            f"Nie zdradzaj wprost odpowiedzi — pomóż zrozumieć zagadnienie."
        )
    else:
        opcje_str = ", ".join([f"{k}) {v}" for k, v in opcje.items()])
        poprawna_tresc = opcje.get(poprawna, "")
        return (
            f"Pytanie: {pytanie}\n"
            f"Opcje: {opcje_str}\n\n"
            f"Wyjaśnij o co pyta to pytanie i jaką wiedzę sprawdza. "
            f"Możesz wyjaśnić dlaczego poprawna odpowiedź to {poprawna}) {poprawna_tresc}, "
            f"ale zrób to w sposób edukacyjny — wytłumacz zagadnienie, nie tylko podaj odpowiedź."
        )


def zbuduj_prompt_blad(pytanie, twoja, poprawna):
    return (
        f"Pytanie:\n{pytanie}\n\n"
        f"Odpowiedź użytkownika:\n{twoja}\n\n"
        f"Poprawna odpowiedź:\n{poprawna}\n\n"
        f"Użytkownik popełnił błąd. Wyjaśnij krótko dlaczego poprawna odpowiedź to \"{poprawna}\", a nie \"{twoja}\"."
    )


def generuj_pytania_quiz(content, num, images, callback_done, callback_error, callback_progress=None):
    """Generuje pytania zamknięte A/B/C/D przez Groq — streaming z licznikiem postępu."""
    import json as _json

    if images:
        callback_error(
            "Groq API nie obsługuje analizy zdjęć.\n"
            "Przepisz tekst ze zdjęcia ręcznie i użyj zakładki 'Tekst'."
        )
        return

    PROMPT = (
        f"Jesteś generatorem pytań do testu wiedzy.\n"
        f"Na podstawie poniższego materiału wygeneruj dokładnie {num} pytań zamkniętych (A/B/C/D).\n\n"
        f"MATERIAŁ:\n{content}\n\n"
        f"WYMAGANIA:\n"
        f"- Każde pytanie ma dokładnie 4 opcje: A, B, C, D\n"
        f"- Tylko jedna opcja jest poprawna\n"
        f"- Pytania mają być różnorodne i sprawdzać rozumienie materiału\n"
        f"- Odpowiedz WYŁĄCZNIE czystym JSON-em bez markdown i bez żadnego wstępu\n\n"
        f"FORMAT — zwróć tablicę JSON:\n"
        f'[{{"pytanie":"...","opcje":{{"A":"...","B":"...","C":"...","D":"..."}},"poprawna":"A"}}]\n\n'
        f"Zwróć TYLKO tablicę JSON — nic więcej."
    )

    def run():
        try:
            client = _get_groq_client()

            stream = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "Jesteś generatorem pytań quizowych. Odpowiadasz WYŁĄCZNIE w formacie JSON."
                    },
                    {"role": "user", "content": PROMPT}
                ],
                max_tokens=2000,
                temperature=0.4,
                stream=True
            )

            raw = ""
            questions_found = 0
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    raw += delta.content
                    new_count = raw.count('"pytanie"')
                    if callback_progress and new_count != questions_found:
                        questions_found = new_count
                        callback_progress(questions_found, num)

            raw = raw.strip()

            if "```" in raw:
                for part in raw.split("```"):
                    part = part.strip().lstrip("json").strip()
                    if part.startswith("["):
                        raw = part
                        break

            if not raw.startswith("["):
                start = raw.find("[")
                end = raw.rfind("]")
                if start != -1 and end != -1:
                    raw = raw[start:end + 1]

            questions = _json.loads(raw)

            if not isinstance(questions, list):
                raise ValueError("Odpowiedź AI nie jest tablicą JSON.")

            callback_done(questions)

        except _json.JSONDecodeError as e:
            callback_error(f"AI zwróciło nieprawidłowy JSON: {e}")
        except Exception as e:
            callback_error(str(e))

    threading.Thread(target=run, daemon=True).start()