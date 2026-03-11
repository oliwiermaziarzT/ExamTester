import json
import os

def load_data(baza):
    with open(baza, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(sciezka, dane):
    with open(sciezka, "w", encoding="utf-8") as f:
        json.dump(dane, f, indent=4, ensure_ascii=False)

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return []
    return []

def save_config(nazwa, sciezka):
    config = load_config()
    updated = False
    for test in config:
        if test["name"] == nazwa:
            test["path"] = sciezka
            updated = True
            break
    if not updated:
        config.append({"name": nazwa, "path": sciezka, "category": ""})
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def save_config_category(nazwa, kategoria):
    config = load_config()
    for test in config:
        if test["name"] == nazwa:
            test["category"] = kategoria
            break
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def delete_from_config(nazwa):
    config = load_config()
    new_config = [test for test in config if test["name"] != nazwa]
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(new_config, f, indent=4, ensure_ascii=False)