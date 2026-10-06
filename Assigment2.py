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
        "waktu_berangkat": "07:45",
        "selisih_menit": 15,
        "jarak_km": 4.5
    },
    {
        "id": 2,
        "owner_id": "USR001",
        "aktivitas": "Nongkrong",
        "waktu_otw": "19:00",
        "waktu_berangkat": "19:00",
        "selisih_menit": 0,
        "jarak_km": 2.0
    },
    {
        "id": 3,
        "owner_id": "USR002",
        "aktivitas": "Rapat",
        "waktu_otw": "09:00",
        "waktu_berangkat": "09:10",
        "selisih_menit": 10,
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
    """Mendapatkan input string non-kosong dari user."""
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
            if value < 0: # Jarak atau selisih tidak boleh negatif 
                print("Angka tidak boleh negatif. Mohon coba lagi.")
                continue
            return value
        except ValueError:
            print(f"Input tidak valid. Mohon masukkan angka yang benar (misal: {type_func.__name__ == 'int' and '123' or '12.3'}).")

def get_time_input(prompt):
    """Mendapatkan input waktu (HH:MM) dari user dengan validasi."""
    while True:
        time_str = input(prompt).strip()
        try:
            datetime.datetime.strptime(time_str, "%H:%M")
            return time_str
        except ValueError:
            print("Format waktu tidak valid. Mohon masukkan dalam format HH:MM (misal: 07:30).")
            
# 4. FUNGSI TAMPILKAN MENU
def tampilkan_menu_program():
    """Menampilkan menu berdasarkan status login dengan slicing Tuple."""
    print("\n" + "=" * 40)
    print(" SISTEM PENCATATAN EKSPERIMEN OTW")
    print("=" * 40)

    if current_user_id: # User sudah login
        print(f"Status: User Login ({current_user_id})")
        opsi_menu_saat_ini = menu[3:] # Menu lengkap untuk user yang login
    else: # Guest
        print("Status: Guest")
        opsi_menu_saat_ini = menu[:3] # Menu terbatas untuk guest
    
    for i, option in enumerate(opsi_menu_saat_ini, start=1):
        print(f"{i}. {option}")
    print("-" * 40)
    return len(opsi_menu_saat_ini)

# 5. FUNGSI REGISTRASI
def registrasi():
    """Fungsi registrasi user baru ke Dictionary accounts dan Nested Dictionary profiles."""
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
    """Fungsi login user, memvalidasi ID dan password menggunakan Dictionary accounts."""
    global current_user_id
    print("\n--- Login User ---")
    
    for _ in range(3): # Batasi percobaan login
        input_id = get_string_input("Masukkan User ID: ").upper()
        input_password = get_string_input("Masukkan Password: ")

        if input_id in accounts and accounts[input_id] == input_password:
            current_user_id = input_id
            print(f"Login berhasil! Selamat datang, {profiles[current_user_id]['nama']}!")
            return True
        else:
            print("ID atau password salah. Mohon coba lagi.")
    print("Anda telah gagal login beberapa kali. Kembali ke menu utama.")
    return False

# FUNGSI MANIPULASI DATA OTW
# (Menggunakan List of Dictionaries dan Strict Session Lock)
def _hitung_selisih_menit(waktu_otw_str, waktu_berangkat_str):
    """Menghitung selisih menit antar dua waktu HH:MM sederhana."""
    format_waktu = "%H:%M"
    waktu_otw = datetime.datetime.strptime(waktu_otw_str, format_waktu)
    waktu_berangkat = datetime.datetime.strptime(waktu_berangkat_str, format_waktu)

    selisih = waktu_berangkat - waktu_otw
    return int(selisih.total_seconds() / 60)

def catat_otw():
    """Mencatat eksperimen OTW baru untuk user yang sedang login."""
    global next_record_id
    if not current_user_id:
        print("Anda harus login untuk mencatat OTW.")
        return

    print("\n--- Catat Pernyataan OTW Baru ---")
    aktivitas = get_string_input("Aktivitas (misal: Kuliah, Rapat): ")
    waktu_otw_str = get_time_input("Waktu OTW (HH:MM, misal: 07:30): ")
    waktu_berangkat_str = get_time_input("Waktu Keberangkatan Aktual (HH:MM, misal: 07:47): ")
    jarak_km = get_numeric_input("Jarak (dalam KM, misal: 4.5): ", type_func=float)

    selisih_menit = _hitung_selisih_menit(waktu_otw_str, waktu_berangkat_str)

    new_record = {
        "id": next_record_id,
        "owner_id": current_user_id,
        "aktivitas": aktivitas,
        "waktu_otw": waktu_otw_str,
        "waktu_berangkat": waktu_berangkat_str,
        "selisih_menit": selisih_menit,
        "jarak_km": jarak_km
    }
    otw_data.append(new_record)
    print(f"Catatan OTW dengan ID {next_record_id} berhasil ditambahkan!")
    next_record_id += 1

def lihat_data():
    """Melihat riwayat OTW user yang sedang login (Strict Session Lock)."""
    if not current_user_id:
        print("Anda harus login untuk melihat data OTW.")
        return

    print("\n--- Riwayat OTW Saya ---")
    user_records = [rec for rec in otw_data if rec["owner_id"] == current_user_id]

    if not user_records:
        print("Anda belum memiliki catatan OTW.")
        return

    for rec in user_records:
        status = "Tepat waktu" if rec["selisih_menit"] <= 0 else "Terlambat"
        print(f"ID Catatan    : {rec['id']}")
        print(f"Aktivitas     : {rec['aktivitas']}")
        print(f"Waktu OTW     : {rec['waktu_otw']}")
        print(f"Waktu Berangkat : {rec['waktu_berangkat']}")
        print(f"Selisih       : {rec['selisih_menit']} menit ({status})")
        print(f"Jarak         : {rec['jarak_km']} KM")
        print("-" * 30)
        
# 9. FUNGSI ANALISIS SEDERHANA
def analisis_data():
    """Melakukan analisis sederhana data OTW user yang sedang login (Strict Session Lock)."""
    if not current_user_id:
        print("Anda harus login untuk melihat analisis OTW.")
        return

    print("\n=== ANALISIS OTW SAYA ===")
    user_records = [rec for rec in otw_data if rec["owner_id"] == current_user_id]

    if not user_records:
        print("Anda belum memiliki catatan OTW untuk dianalisis.")
        return
    
    total_catatan = len(user_records)
    jumlah_terlambat = sum(1 for rec in user_records if rec["selisih_menit"] > 0)
    total_selisih_terlambat = sum(rec["selisih_menit"] for rec in user_records if rec["selisih_menit"] > 0)
    
    rata_rata_selisih = total_selisih_terlambat / jumlah_terlambat if jumlah_terlambat > 0 else 0.0

    print(f"Total catatan OTW      : {total_catatan}")
    print(f"Jumlah terlambat       : {jumlah_terlambat}")
    print(f"Rata-rata keterlambatan: {rata_rata_selisih:.1f} menit")
    print("=" * 25)
    
# 10. FUNGSI LOGOUT
def logout():
    """Fungsi logout user, mereset session."""
    global current_user_id
    if current_user_id:
        print(f"Logout berhasil! Sampai jumpa, {profiles[current_user_id]['nama']}.")
        current_user_id = None
    else:
        print("Anda belum login.")
        
# 11. MAIN LOOP PROGRAM
def main():
    while True:
        num_options = tampilkan_menu_program()

        pilihan = get_numeric_input(f"Pilih menu (1-{num_options}): ")

        if current_user_id: # User sudah login
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
        else: # Guest
            if pilihan == 1:
                login()
            elif pilihan == 2:
                registrasi()
            elif pilihan == 3:
                print("Terima kasih telah menggunakan sistem ini. Sampai jumpa!")
                break
            else:
                print("Pilihan tidak valid. Mohon coba lagi.")
        input("\nTekan ENTER untuk melanjutkan...") 

if __name__ == "__main__":
    main()