import json
import os

USERS_FILE = "users.json"

DEFAULT_ADMIN = {
    "username": "admin",
    "password": "akuadminkamusiapa",
    "role": "admin"
}

def load_users():
    if not os.path.exists(USERS_FILE):
        save_users([DEFAULT_ADMIN])
        return [DEFAULT_ADMIN]

    with open(USERS_FILE, "r") as f:
        try:
            users = json.load(f)
            if not any(u["username"] == "admin" for u in users):
                users.append(DEFAULT_ADMIN)
                save_users(users)
            return users
        except json.JSONDecodeError:
            save_users([DEFAULT_ADMIN])
            return [DEFAULT_ADMIN]

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)
        