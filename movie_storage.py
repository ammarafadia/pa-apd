import json
import os

MOVIES_FILE = "movies.json"

def load_movies():
    if not os.path.exists(MOVIES_FILE):
        return []
    with open(MOVIES_FILE, "r") as f:
        return json.load(f)

def save_movies(movies):
    with open(MOVIES_FILE, "w") as f:
        json.dump(movies,f,indent=4)