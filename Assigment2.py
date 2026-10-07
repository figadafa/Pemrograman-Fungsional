import datetime

# 1. DATA MOCK
accounts = {
    "USR001": "pass1",
    "USR002": "pass2",
    "USR003": "pass3"
}

# profiles: Nested Dictionary
profiles = {
    "USR001": {
        "nama": "Budi",
        "nomor_telepon": "081234567890",
        "peran": "Mahasiswa"
    },
    "USR002": {
        "nama": "Siti",
        "nomor_telepon": "081111111111",
        "peran": "Mahasiswa"
    },
    "USR003": {
        "nama": "Joko",
        "nomor_telepon": "082222222222",
        "peran": "Mahasiswa"
    }
}

# otw_data
otw_data = [
    {
        "id": 1,
        "owner_id": "USR001",
        "aktivitas": "Kuliah",
        "waktu_otw": "07:30",
        "waktu_tiba": "07:45",
        "durasi_menit": 15,
        "jarak_km": 4.5
    },
    {
        "id": 2,
        "owner_id": "USR001",
        "aktivitas": "Nongkrong",
        "waktu_otw": "19:00",
        "waktu_tiba": "19:20",
        "durasi_menit": 20,
        "jarak_km": 2.0
    },
    {
        "id": 3,
        "owner_id": "USR002",
        "aktivitas": "Rapat",
        "waktu_otw": "09:00",
        "waktu_tiba": "09:25",
        "durasi_menit": 25,
        "jarak_km": 10.2
    }
]

# 2. VARIABEL SESSION
current_user_id = None
next_record_id = max([rec["id"] for rec in otw_data]) + 1 if otw_data else 1

# 3. TUPLE MENU
menu = (
    "Login",
    "Registrasi",
    "Keluar",
    "Catat OTW",
    "Lihat Data",
    "Analisis Data",
    "Logout"
)

# Menggunakan while loop dan try-except untuk validasi
def get_string_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        else:
            print("Input tidak boleh kosong. Mohon coba lagi.")
def get_numeric_input(prompt, type_func=int):
    """Mendapatkan input numerik (int atau float) dari user dengan validasi."""
    while True:
        try:
            value_str = input(prompt).strip()
            value = type_func(value_str)

            if value < 0:
                print("Angka tidak boleh negatif. Mohon coba lagi.")
                continue

            return value

        except ValueError:
            print(
                f"Input tidak valid. Mohon masukkan angka yang benar "
                f"(misal: {type_func.__name__ == 'int' and '123' or '12.3'})."
            )
def get_time_input(prompt):
    """Mendapatkan input waktu (HH:MM) dari user dengan validasi."""
    while True:
        time_str = input(prompt).strip()
        try:
            datetime.datetime.strptime(time_str, "%H:%M")
            return time_str
        except ValueError:
            print(
                "Format waktu tidak valid. Mohon masukkan dalam format "
                "HH:MM (misal: 07:30)."
            )


# 4. FUNGSI TAMPILKAN MENU
def tampilkan_menu_program():
    print("\n" + "=" * 40)
    print(" SISTEM PENCATATAN EKSPERIMEN OTW")
    print("=" * 40)
    if current_user_id:
        print(f"Status: User Login ({current_user_id})")
        opsi_menu_saat_ini = menu[3:]
    else:
        print("Status: Guest")
        opsi_menu_saat_ini = menu[:3]
    for i, option in enumerate(opsi_menu_saat_ini, start=1):
        print(f"{i}. {option}")
    print("-" * 40)
    return len(opsi_menu_saat_ini)

# 5. FUNGSI REGISTRASI
def registrasi():
    print("\n--- Registrasi User Baru ---")

    while True:
        new_id = get_string_input("Masukkan ID baru: ").upper()

        if new_id in accounts:
            print("ID sudah terdaftar. Mohon gunakan ID lain.")
        else:
            break

    password = get_string_input("Masukkan password: ")
    nama = get_string_input("Masukkan nama lengkap: ")
    nomor_telepon = get_string_input("Masukkan nomor telepon: ")
    peran = get_string_input("Masukkan peran (misal: Mahasiswa, Dosen): ")
    accounts[new_id] = password
    profiles[new_id] = {
        "nama": nama,
        "nomor_telepon": nomor_telepon,
        "peran": peran
    }
    print(f"Registrasi berhasil! User ID: {new_id}")


# 6. FUNGSI LOGIN
def login():
    global current_user_id
    print("\n--- Login User ---")
    for _ in range(3):
        input_id = get_string_input("Masukkan User ID: ").upper()
        input_password = get_string_input("Masukkan Password: ")
        if input_id in accounts and accounts[input_id] == input_password:
            current_user_id = input_id
            print(
                f"Login berhasil! Selamat datang, "
                f"{profiles[current_user_id]['nama']}!"
            )
            return True
        else:
            print("ID atau password salah. Mohon coba lagi.")
    print("Anda telah gagal login beberapa kali. Kembali ke menu utama.")
    return False


# FUNGSI MANIPULASI DATA OTW
def _hitung_durasi_menit(waktu_otw_str, waktu_tiba_str):
    format_waktu = "%H:%M"
    waktu_otw = datetime.datetime.strptime(waktu_otw_str, format_waktu)
    waktu_tiba = datetime.datetime.strptime(waktu_tiba_str, format_waktu)
    durasi = waktu_tiba - waktu_otw
    return int(durasi.total_seconds() / 60)
def catat_otw():
    global next_record_id

    if not current_user_id:
        print("Anda harus login untuk mencatat OTW.")
        return
    print("\n--- Catat Pernyataan OTW Baru ---")
    aktivitas = get_string_input("Aktivitas (misal: Kuliah, Rapat): ")
    waktu_otw_str = get_time_input(
        "Waktu mengatakan OTW (HH:MM, misal: 07:30): "
    )
    waktu_tiba_str = get_time_input(
        "Waktu tiba di tujuan (HH:MM, misal: 07:47): "
    )
    jarak_km = get_numeric_input(
        "Jarak (dalam KM, misal: 4.5): ",
        type_func=float
    )
    durasi_menit = _hitung_durasi_menit(
        waktu_otw_str,
        waktu_tiba_str
    )
    new_record = {
        "id": next_record_id,
        "owner_id": current_user_id,
        "aktivitas": aktivitas,
        "waktu_otw": waktu_otw_str,
        "waktu_tiba": waktu_tiba_str,
        "durasi_menit": durasi_menit,
        "jarak_km": jarak_km
    }
    otw_data.append(new_record)
    print(
        f"Catatan OTW dengan ID {next_record_id} berhasil ditambahkan!"
    )
    print(f"Durasi perjalanan: {durasi_menit} menit")
    next_record_id += 1
def lihat_data():
    if not current_user_id:
        print("Anda harus login untuk melihat data OTW.")
        return
    print("\n--- Riwayat OTW Saya ---")
    user_records = [
        rec for rec in otw_data
        if rec["owner_id"] == current_user_id
    ]
    if not user_records:
        print("Anda belum memiliki catatan OTW.")
        return
    for rec in user_records:
        print(f"ID Catatan     : {rec['id']}")
        print(f"Aktivitas      : {rec['aktivitas']}")
        print(f"Waktu OTW      : {rec['waktu_otw']}")
        print(f"Waktu Tiba     : {rec['waktu_tiba']}")
        print(f"Durasi         : {rec['durasi_menit']} menit")
        print(f"Jarak          : {rec['jarak_km']} KM")
        print("-" * 30)


# 9. FUNGSI ANALISIS SEDERHANA
def analisis_data():
    """Melakukan analisis sederhana durasi OTW user yang sedang login."""
    if not current_user_id:
        print("Anda harus login untuk melihat analisis OTW.")
        return
    print("\n=== ANALISIS OTW SAYA ===")
    user_records = [
        rec for rec in otw_data
        if rec["owner_id"] == current_user_id
    ]
    if not user_records:
        print("Anda belum memiliki catatan OTW untuk dianalisis.")
        return
    total_catatan = len(user_records)
    total_durasi = sum(
        rec["durasi_menit"]
        for rec in user_records
    )
    rata_rata_durasi = total_durasi / total_catatan
    durasi_tercepat = min(
        rec["durasi_menit"]
        for rec in user_records
    )
    durasi_terlama = max(
        rec["durasi_menit"]
        for rec in user_records
    )
    print(f"Total catatan OTW    : {total_catatan}")
    print(f"Total durasi         : {total_durasi} menit")
    print(f"Rata-rata durasi     : {rata_rata_durasi:.1f} menit")
    print(f"Durasi tercepat      : {durasi_tercepat} menit")
    print(f"Durasi terlama       : {durasi_terlama} menit")
    print("=" * 25)

# 10. FUNGSI LOGOUT
def logout():
    """Fungsi logout user, mereset session."""
    global current_user_id
    if current_user_id:
        print(
            f"Logout berhasil! Sampai jumpa, "
            f"{profiles[current_user_id]['nama']}."
        )
        current_user_id = None
    else:
        print("Anda belum login.")


# 11. MAIN LOOP PROGRAM
def main():
    while True:
        num_options = tampilkan_menu_program()

        pilihan = get_numeric_input(
            f"Pilih menu (1-{num_options}): "
        )
        if current_user_id:
            if pilihan == 1:
                catat_otw()
            elif pilihan == 2:
                lihat_data()
            elif pilihan == 3:
                analisis_data()
            elif pilihan == 4:
                logout()
            else:
                print("Pilihan tidak valid. Mohon coba lagi.")
        else:
            if pilihan == 1:
                login()

            elif pilihan == 2:
                registrasi()
            elif pilihan == 3:
                print(
                    "Terima kasih telah menggunakan sistem ini. "
                    "Sampai jumpa!"
                )
                break
            else:
                print("Pilihan tidak valid. Mohon coba lagi.")
        input("\nTekan ENTER untuk melanjutkan...")
if __name__ == "__main__":
    main()
