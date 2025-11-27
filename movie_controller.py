from movie_storage import load_movies, save_movies
from prettytable import PrettyTable

MENU_FIELDS = ("Judul", "Genre", "Tahun")


def list_movies():
    movies = load_movies()

    if not movies:
        print("Belum ada film.")
        return

    table = PrettyTable(["No", "Judul", "Genre", "Tahun", "Ditambahkan"])

    for i, m in enumerate(movies, 1):
        table.add_row([
            i,
            m.get("judul", "-"),
            m.get("genre", "-"),
            m.get("tahun", "-"),
            m.get("added_by", "-")
        ])
    print(table)


def add_movie(current_user):
    movies = load_movies()

    print("\n=== Daftar Film Saat Ini ===")
    if movies:
        list_movies()
    else:
        print("Belum ada film sama sekali.")

    print("\n--- Tambah Film Baru ---")

    judul = input("Judul film: ").strip()
    if not judul:
        print("Judul tidak boleh kosong!")
        return

    existing_titles = {m["judul"].lower() for m in movies}
    if judul.lower() in existing_titles:
        print("Judul film sudah ada! Tidak boleh duplikat.")
        return

    genre = input("Genre: ").strip()
    if not genre:
        print("Genre tidak boleh kosong!")
        return

    tahun_input = input("Tahun: ").strip()
    if not tahun_input.isdigit():
        print("Tahun harus berupa angka!")
        return

    new_movie = {
        "judul": judul,
        "genre": genre,
        "tahun": tahun_input,
        "added_by": current_user["username"],
        "ratings": {}
    }

    movies.append(new_movie)
    save_movies(movies)
    print("Film berhasil ditambahkan!")


def edit_movie():
    movies = load_movies()
    if not movies:
        print("Belum ada film untuk diubah.")
        return

    list_movies()

    try:
        pil = int(input("Pilih nomor film: ")) - 1
    except ValueError:
        print("Input harus angka!")
        return

    if 0 <= pil < len(movies):
        m = movies[pil]

        yakin = input(f"Anda yakin ingin mengedit film '{m.get('judul')}'? (y/n): ").lower()
        if yakin != "y":
            print("Edit dibatalkan.")
            return

        judul = input(f"Judul baru ({m.get('judul','-')}): ").strip()
        genre = input(f"Genre baru ({m.get('genre','-')}): ").strip()
        tahun = input(f"Tahun baru ({m.get('tahun','-')}): ").strip()

        if tahun and not tahun.isdigit():
            print("Tahun harus angka!")
            return

        if judul and any(f["judul"].lower() == judul.lower() and f != m for f in movies):
            print("Judul baru sudah digunakan film lain!")
            return

        if judul:
            m["judul"] = judul
        if genre:
            m["genre"] = genre
        if tahun:
            m["tahun"] = tahun

        save_movies(movies)
        print("Film diupdate!")
    else:
        print("Nomor tidak valid.")


def delete_movie():
    movies = load_movies()
    if not movies:
        print("Belum ada film untuk dihapus.")
        return

    list_movies()

    try:
        pil = int(input("Pilih nomor film: ")) - 1
    except ValueError:
        print("Input harus angka!")
        return

    if 0 <= pil < len(movies):
        judul = movies[pil].get("judul", "-")

        yakin = input(f"Anda yakin ingin menghapus '{judul}'? (y/n): ").lower()
        if yakin != "y":
            print("Penghapusan dibatalkan.")
            return

        movies.pop(pil)
        save_movies(movies)
        print(f"Film '{judul}' dihapus!")
    else:
        print("Nomor tidak valid.")


def rate_movie(current_user):
    movies = load_movies()
    if not movies:
        print("Belum ada film untuk dirating.")
        return

    list_movies()

    try:
        pil = int(input("Pilih nomor film: ")) - 1
    except ValueError:
        print("Input harus angka!")
        return

    if 0 <= pil < len(movies):
        film = movies[pil]
        user = current_user["username"]

        sudah_rating = user in film.get("ratings", {})

        if sudah_rating:
            lama = film["ratings"][user]
            print(f"\nAnda sudah memberi rating sebelumnya: {lama}")
            konfirmasi = input("Apakah Anda yakin ingin mengubah rating? (y/n): ").lower()

            if konfirmasi != "y":
                print("Perubahan rating dibatalkan.")
                return

        try:
            rating = int(input("Rating (1-10): "))
        except ValueError:
            print("Rating harus angka!")
            return

        if 1 <= rating <= 10:
            film.setdefault("ratings", {})
            film["ratings"][user] = rating
            save_movies(movies)

            if sudah_rating:
                print("Rating berhasil diperbarui!")
            else:
                print("Rating disimpan!")
        else:
            print("Rating harus 1-10!")
    else:
        print("Nomor tidak valid.")


def list_watched(current_user):
    movies = load_movies()
    watched = [m for m in movies if current_user["username"] in m.get("ratings", {})]

    if not watched:
        print("Belum ada film yang dirating.")
        return

    table = PrettyTable(["No", "Judul", "Genre", "Tahun", "Rating Anda"])

    for i, m in enumerate(watched, 1):
        table.add_row([
            i,
            m.get("judul", "-"),
            m.get("genre", "-"),
            m.get("tahun", "-"),
            m.get("ratings", {}).get(current_user["username"], "-")
        ])
    print(table)


def top_rated_movies():
    movies = load_movies()
    rated = []

    for m in movies:
        ratings = m.get("ratings", {})
        if ratings:
            avg = sum(ratings.values()) / len(ratings)
            rated.append((m, avg))

    if not rated:
        print("Belum ada film yang dirating.")
        return

    rated.sort(key=lambda x: x[1], reverse=True)
    table = PrettyTable(["No", "Judul", "Genre", "Tahun", "Rata-rata"])

    for i, (m, avg) in enumerate(rated, 1):
        table.add_row([
            i,
            m.get("judul", "-"),
            m.get("genre", "-"),
            m.get("tahun", "-"),
            round(avg, 2)
        ])
    print (table)