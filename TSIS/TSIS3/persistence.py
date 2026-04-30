import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEADERBOARD_PATH = os.path.join(BASE_DIR, "leaderboard.json")
SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")


def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return default


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


# ---------------- SETTINGS ----------------
def load_settings():
    return load_json(SETTINGS_PATH, {
        "sound": True,
        "difficulty": "normal",
        "username": "",
        "car_skin": "red"
    })


def save_settings(data):
    save_json(SETTINGS_PATH, data)


# ---------------- LEADERBOARD ----------------
def add_score(name, score, distance):
    data = load_json(LEADERBOARD_PATH, [])

    data.append({
        "name": name,
        "score": score,
        "distance": distance
    })

    data = sorted(data, key=lambda x: (x["score"], x["distance"]), reverse=True)

    save_json(LEADERBOARD_PATH, data[:10])


def load_leaderboard():
    return load_json(LEADERBOARD_PATH, [])