import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")
LEADERBOARD_PATH = os.path.join(BASE_DIR, "leaderboard.json")


def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def load_settings():
    return load_json(SETTINGS_PATH, {
        "sound": True,
        "car_color": "red",
        "difficulty": "normal"
    })


def save_settings(data):
    save_json(SETTINGS_PATH, data)


def load_leaderboard():
    return load_json(LEADERBOARD_PATH, [])


def save_leaderboard(data):
    save_json(LEADERBOARD_PATH, data)