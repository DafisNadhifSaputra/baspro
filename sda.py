from memobook import Memobook
import json
import os
from struktur_data import SinglyLinkedList, Node

class MemobookApplication:
    def __init__(self, data_file="memobook_data.json"):
        # Inisialisasi aplikasi Memobook.
        # self.memobooks adalah dictionary untuk menyimpan objek Memobook, dengan kunci nama memobook (lowercase).
        self.memobooks = {}
        # self.data_file adalah nama file JSON tempat data memobook disimpan.
        self.data_file = data_file
        # Muat data yang ada dari file JSON saat aplikasi dimulai.
        self.load_data_dari_json()
        # Jika tidak ada memobook yang dimuat (misalnya, file tidak ada atau kosong),
        # inisialisasi dengan beberapa memobook default.
        if not self.memobooks:
            self._inisialisasi_default_memobooks()

    def _inisialisasi_default_memobooks(self):
        # Metode privat untuk membuat beberapa memobook default jika belum ada data.
        default_subjects = ["Aljabar Abstrak", "Persamaan Diferensial", "Analisis Real", "Struktur Data dan Algoritma"]
        for subject in default_subjects:
            # Tambahkan memobook hanya jika belum ada dengan nama yang sama (case-insensitive)
            if subject.lower() not in self.memobooks:
                 self.memobooks[subject.lower()] = Memobook(subject)
        print("Memobook default telah diinisialisasi (jika belum ada).")

    def save_data_ke_json(self):
        # Menyimpan semua data memobook (self.memobooks) ke file JSON.
        data_to_save = {}
        # Iterasi melalui semua memobook dan konversi masing-masing menjadi dictionary
        for name_key, memobook_obj in self.memobooks.items():
            data_to_save[name_key] = memobook_obj.to_dict()
        try:
            # Buka file dalam mode tulis (write) dengan encoding utf-8
            with open(self.data_file, "w", encoding="utf-8") as f:
                # Gunakan json.dump untuk menulis data ke file dengan format yang rapi (indent=4)
                json.dump(data_to_save, f, indent=4)
            print(f"Data berhasil disimpan ke '{self.data_file}'.")
        except IOError:
            # Tangani error jika terjadi masalah saat operasi file (misalnya, permission denied)
            print(f"Gagal menyimpan data. Terjadi kesalahan I/O pada file '{self.data_file}'.")
        except Exception as e:
            # Tangani error umum lainnya
            print(f"Terjadi kesalahan tak terduga saat menyimpan data: {e}")

    def load_data_dari_json(self):
        # Memuat data memobook dari file JSON.
        if not os.path.exists(self.data_file):
            print(f"File data '{self.data_file}' tidak ditemukan. Memulai dengan memobook default.")
            return

        try:
            # Buka file dalam mode baca (read) dengan encoding utf-8
            with open(self.data_file, "r", encoding="utf-8") as f:
                # Periksa apakah file kosong
                if os.path.getsize(self.data_file) == 0:
                    print(f"File data '{self.data_file}' kosong. Memulai dengan memobook default.")
                    self.memobooks = {}
                    return

                loaded_data = json.load(f)  # Baca data JSON dari file
                self.memobooks = {}
                # Iterasi melalui data yang dimuat dan buat kembali objek Memobook
                for name_key, memobook_data_dict in loaded_data.items():
                    # Gunakan staticmethod from_dict dari kelas Memobook untuk membuat instance
                    self.memobooks[name_key] = Memobook.from_dict(memobook_data_dict)
            print(f"Data berhasil dimuat dari '{self.data_file}'.")
        except json.JSONDecodeError:
            # Jika file JSON tidak valid, tampilkan pesan dan mulai dengan dictionary kosong
            print(f"Gagal memuat data. File '{self.data_file}' memiliki format JSON yang tidak valid.")
            self.memobooks = {}
        except Exception as e:
            # Tangani error umum lainnya saat memuat data
            print(f"Terjadi kesalahan tak terduga saat memuat data: {e}")
            self.memobooks = {}

    def add_custom_memobook(self):
        # Meminta pengguna untuk memasukkan nama memobook baru.
        memobook_name = input("Masukkan nama memobook baru: ")
        # Pastikan nama tidak kosong dan belum ada
        if memobook_name and memobook_name.lower() not in self.memobooks:
            self.memobooks[memobook_name.lower()] = Memobook(memobook_name)
            self.save_data_ke_json() # Simpan perubahan
            print(f"Memobook '{memobook_name}' berhasil ditambahkan.")
        else:
            print("Nama memobook tidak valid atau sudah ada.")

    def display_all_memobooks(self):
        # Menampilkan semua nama memobook yang tersedia.
        print("\n--- Daftar Memobook ---")
        if not self.memobooks:
            print("Tidak ada memobook yang tersedia.")
        else:
            # Buat daftar nama memobook untuk ditampilkan dengan nomor
            memobook_names = [mb.name for mb in self.memobooks.values()]
            for i, name in enumerate(memobook_names):
                print(f"{i + 1}. {name}")

    def select_memobook(self):
        # Memungkinkan pengguna untuk memilih memobook dari daftar.
        self.display_all_memobooks()
        if not self.memobooks:
            return None
        try:
            choice = int(input("Pilih nomor memobook: "))
            # Ubah dictionary keys menjadi list untuk memilih berdasarkan indeks
            memobook_keys = list(self.memobooks.keys())
            if 1 <= choice <= len(memobook_keys):
                selected_key = memobook_keys[choice - 1]
                return self.memobooks[selected_key]
            else:
                print("Pilihan tidak valid.")
                return None
        except ValueError:
            # Tangani jika input pengguna bukan angka
            print("Input harus berupa angka.")
            return None

    def memobook_menu(self, current_memobook):
        # Menampilkan menu operasi untuk memobook yang sedang dipilih.
        while True:
            print(f"\n--- Menu Memobook: {current_memobook.name} ---")
            print("1. Tambah Memo Baru")
            print("2. Lihat Semua Memo")
            print("3. Edit Memo")
            print("4. Hapus Memo")
            print("5. Urutkan Memo (Berdasarkan Judul)")
            print("6. Urutkan Memo (Berdasarkan Tanggal)")
            print("7. Cari Memo (Berdasarkan Judul)")
            print("8. Ekspor Memo ke File Teks (.txt)")
            print("9. Kembali ke Menu Utama")
            choice = input("Pilihan: ")

            # Setiap operasi yang mengubah data (tambah, edit, hapus, urutkan) akan diikuti dengan penyimpanan data.
            if choice == '1':
                current_memobook.add_memo()
                self.save_data_ke_json() # Simpan setelah menambah memo
            elif choice == '2':
                current_memobook.view_memos()
            elif choice == '3':
                current_memobook.edit_memo()
                self.save_data_ke_json() # Simpan setelah mengedit memo
            elif choice == '4':
                current_memobook.delete_memo()
                self.save_data_ke_json() # Simpan setelah menghapus memo
            elif choice == '5':
                current_memobook.sort_memos() # Urutkan berdasarkan judul
                self.save_data_ke_json() # Simpan setelah mengurutkan
            elif choice == '6':
                if current_memobook:
                    current_memobook.sort_memos_by_date() # Urutkan berdasarkan tanggal
                    self.save_data_ke_json() # Simpan setelah mengurutkan
                else:
                    print("Tidak ada memobook yang sedang aktif.")
            elif choice == '7':
                current_memobook.search_memo()
            elif choice == '8':
                current_memobook.export_memos_to_txt()
            elif choice == '9':
                break # Kembali ke menu utama
            else:
                print("Pilihan tidak valid.")

    def main_loop(self):
        # Loop utama aplikasi yang menampilkan menu utama dan mengarahkan pengguna.
        while True:
            print("\n--- Aplikasi Memobook SDA ---")
            print("1. Pilih Memobook")
            print("2. Tambah Memobook Baru")
            print("3. Tampilkan Semua Memobook")
            print("4. Keluar")
            main_choice = input("Pilihan: ")

            if main_choice == '1':
                # Pengguna memilih untuk masuk ke menu memobook tertentu
                selected_mb = self.select_memobook()
                if selected_mb:
                    self.memobook_menu(selected_mb) # Tampilkan menu untuk memobook yang dipilih
            elif main_choice == '2':
                # Pengguna memilih untuk menambah memobook baru
                self.add_custom_memobook()
            elif main_choice == '3':
                # Pengguna memilih untuk menampilkan semua memobook
                self.display_all_memobooks()
            elif main_choice == '4':
                # Pengguna memilih untuk keluar aplikasi
                self.save_data_ke_json() # Pastikan data terakhir disimpan sebelum keluar
                print("Terima kasih telah menggunakan aplikasi ini!")
                break # Keluar dari loop utama
            else:
                print("Pilihan tidak valid.")

# --- Menjalankan Aplikasi ---
# Blok ini akan dieksekusi hanya jika file sda.py dijalankan secara langsung (bukan diimpor sebagai modul).
if __name__ == "__main__":
    # Membuat instance dari MemobookApplication
    app = MemobookApplication()
    # Memulai loop utama aplikasi
    app.main_loop()