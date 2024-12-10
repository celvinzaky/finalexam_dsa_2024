import hashlib
import sqlite3

# Fungsi untuk membuat hash dari kata sandi
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Fungsi untuk membuat database dan tabel jika belum ada
def initialize_database():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            site TEXT,
            username TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

# Fungsi untuk registrasi pengguna baru
def register():
    username = input("Masukkan username baru: ")
    password = input("Masukkan password baru: ")
    hashed_password = hash_password(password)

    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("Registrasi berhasil!")
    except sqlite3.IntegrityError:
        print("Username sudah digunakan.")
    conn.close()

# Fungsi untuk login
def login():
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")
    hashed_password = hash_password(password)

    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()

    if user:
        print("Login berhasil!")
        return True
    else:
        print("Username atau password salah.")
        return False

# Fungsi untuk menyimpan kata sandi
def save_password():
    site = input("Masukkan nama situs: ")
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (site, username, password) VALUES (?, ?, ?)", (site, username, password))
    conn.commit()
    conn.close()
    print("Kata sandi berhasil disimpan!")

# Fungsi untuk mencari kata sandi
def search_password():
    site = input("Masukkan nama situs yang ingin dicari: ")

    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM passwords WHERE site = ?", (site,))
    result = cursor.fetchone()
    conn.close()

    if result:
        print(f"Username: {result[0]}")
        print(f"Password: {result[1]}")
    else:
        print("Kata sandi untuk situs tersebut tidak ditemukan.")

# Fungsi utama
def main():
    initialize_database()
    print("Selamat datang di SafePass Lite!")
    while True:
        print("\nPilih menu:")
        print("1. Registrasi")
        print("2. Login")
        print("3. Simpan kata sandi")
        print("4. Cari kata sandi")
        print("5. Keluar")
        choice = input("Masukkan pilihan (1/2/3/4/5): ")

        if choice == "1":
            register()
        elif choice == "2":
            if login():
                print("Anda berhasil login.")
        elif choice == "3":
            save_password()
        elif choice == "4":
            search_password()
        elif choice == "5":
            print("Terima kasih telah menggunakan SafePass Lite. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main()
