import os
from time import sleep
from auth import login_user, register_user
import movie_controller as m


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def menu_movie(user):
    if not isinstance(user, dict) or "role" not in user:
        print("Error: data user tidak valid.")
        sleep(1)
        return

    while True:
        clear()
        print("=== MENU FILM ===")
        print("1. Lihat Film")
        print("2. Film yang Ditonton")
        print("3. Rating Film")

        role = user.get("role", "user")

        if role == "admin":
            print("4. Tambah Film")
            print("5. Edit Film")
            print("6. Hapus Film")
            print("7. Lihat Rating Tertinggi")
            print("8. Logout")
        else:
            print("4. Logout")

        pilihan = input("Pilih: ")

        try:
            if pilihan == "1":
                clear()
                m.list_movies()
                input("Tekan Enter...")

            elif pilihan == "2":
                clear()
                m.list_watched(user)
                input("Tekan Enter...")

            elif pilihan == "3":
                clear()
                m.rate_movie(user)
                input("Tekan Enter...")

            elif pilihan == "4" and role == "admin":
                clear()
                m.add_movie(user)
                input("Tekan Enter...")

            elif pilihan == "5" and role == "admin":
                clear()
                m.edit_movie()
                input("Tekan Enter...")

            elif pilihan == "6" and role == "admin":
                clear()
                m.delete_movie()
                input("Tekan Enter...")

            elif pilihan == "7" and role == "admin":
                clear()
                m.top_rated_movies()
                input("Tekan Enter...")

            elif pilihan == "8" and role == "admin":
                print("Logout...")
                sleep(1)
                break

            elif pilihan == "4" and role == "user":
                print("Logout...")
                sleep(1)
                break

            else:
                print("Pilihan tidak valid.")
                sleep(1)

        except Exception as e:
            print("Terjadi error:", e)
            input("Tekan Enter...")
            clear()


def main():
    while True:
        clear()
        print("=== MENU AWAL ===")
        print("1. Login")
        print("2. Register")
        print("3. Keluar")

        p = input("Pilih: ")

        if p == "1":
            user = login_user()

            if user and isinstance(user, dict):
                if "role" not in user:
                    user["role"] = "user"

                menu_movie(user)
            else:
                print("Login gagal.")
                sleep(1)

        elif p == "2":
            register_user()

        elif p == "3":
            print("Keluar...")
            print("Terimakasih Atas Kunjungannya")
            sleep(3)
            clear()
            break

        else:
            print("Pilihan tidak valid.")
            sleep(1)

            
if __name__ == "__main__":
    main()