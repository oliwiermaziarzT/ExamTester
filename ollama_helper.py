import ollama
import threading


OLLAMA_MODEL = "llama3:latest"


def zapytaj_ollame(prompt, callback_chunk, callback_done, callback_error):
    def run():
            stream = ollama.chat(
                model=OLLAMA_MODEL,
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
            for chunk in stream:
                token = chunk["message"]["content"]
                callback_chunk(token)
            callback_done()


    thread = threading.Thread(target=run, daemon=True)
    thread.start()


def zbuduj_prompt_quiz(pytanie, opcje, poprawna, twoja, typ):
    if typ == "zamkniete":
        opcje_text = "\n".join([f"  {k}: {v}" for k, v in opcje.items()]) if opcje else ""
        return (
            f"Pytanie egzaminacyjne:\n{pytanie}\n\n"
            f"Opcje odpowiedzi:\n{opcje_text}\n\n"
            f"Poprawna odpowiedź: {poprawna}\n"
            f"Moja odpowiedź: {twoja}\n\n"
            f"""Jesteś ekspertem w języku hiszpańskim, idealnie znasz gramatykę oraz slang i to co się powszechnie używa w języku - 
            Wyjaśnij krótko i cała odpowiedź musi być po polsku dlaczego odpowiedź '{poprawna}' jest prawidłowa."""
        )
    else:
        return (
            f"Pytanie egzaminacyjne:\n{pytanie}\n\n"
            f"Poprawna odpowiedź: {poprawna}\n"
            f"Moja odpowiedź: {twoja}\n\n"
            f"""Jesteś ekspertem w języku hiszpańskim, idealnie znasz gramatykę oraz slang i to co się powszechnie używa w języku - 
            Wyjaśnij krótko i cała odpowiedź musi być po polsku dlaczego to jest poprawna odpowiedź."""
        )


def zbuduj_prompt_blad(pytanie, twoja, poprawna):
    return (
        f"Pytanie egzaminacyjne:\n{pytanie}\n\n"
        f"Poprawna odpowiedź: {poprawna}\n"
        f"Błędna odpowiedź ucznia: {twoja}\n\n"
        f"Wyjaśnij krótko i po polsku dlaczego odpowiedź '{poprawna}' jest prawidłowa, "
        f"a '{twoja}' nie jest poprawna."
    )