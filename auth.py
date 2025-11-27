from auth_storage import load_users, save_users

def register_user():
    users = load_users()

    username = input("Username baru: ").strip()

    if username == "":
        print("Username tidak boleh kosong!")
        input("Tekan Enter")
        return None

    password = input("Password: ").strip()
    if password == "":
        print("Password tidak boleh kosong!")
        input("Tekan Enter")
        return None

    existing = {u["username"] for u in users}

    if username in existing:
        print("Username sudah ada")
        input("Tekan Enter")
        return None

    new_user = {
        "username": username,
        "password": password,
        "role": "user"
    }

    users.append(new_user)
    save_users(users)
    print("Registrasi berhasil!")
    return new_user

def login_user():
    users = load_users()
    username = input("Username: ").strip()
    if username == "":
        print("Username tidak boleh kosong!")
        input("Tekan Enter")
        return None

    password = input("Password: ").strip()
    if password == "":
        print("Password tidak boleh kosong!")
        input("Tekan Enter")
        return None

    for u in users:
        if u["username"] == username and u["password"] == password:
            print(f"Login berhasil! Selamat datang {u['username']}")
            return u

    print("Username atau password salah!")
    return None
