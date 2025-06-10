from notebook import Notebook
import json
from struktur_data import SinglyLinkedList, Node

class NotebookApplication:
    def __init__(self, data_file="notebook_data.json"):
        # Inisialisasi aplikasi Notebook.
        # self.notebooks adalah dictionary untuk menyimpan objek Notebook, dengan kunci nama notebook (lowercase).
        self.notebooks = {}
        # self.data_file adalah nama file JSON tempat data notebook disimpan.
        self.data_file = data_file
        # Muat data yang ada dari file JSON saat aplikasi dimulai.
        self.load_data_dari_json()
        # Jika tidak ada notebook yang dimuat (misalnya, file tidak ada atau kosong),
        # inisialisasi dengan beberapa notebook default.
        if not self.notebooks:
            self._inisialisasi_default_notebooks()

    def _inisialisasi_default_notebooks(self):
        # Metode privat untuk membuat beberapa notebook default jika belum ada data.
        default_subjects = ["Aljabar Abstrak", "Persamaan Diferensial", "Analisis Real", "Struktur Data dan Algoritma"]
        for subject in default_subjects:
            # Tambahkan notebook hanya jika belum ada dengan nama yang sama (case-insensitive)
            if subject.lower() not in self.notebooks:
                 self.notebooks[subject.lower()] = Notebook(subject)
        print("Notebook default telah diinisialisasi (jika belum ada).")

    def save_data_ke_json(self):
        # Menyimpan semua data notebook (self.notebooks) ke file JSON.
        data_to_save = {}
        # Iterasi melalui semua notebook dan konversi masing-masing menjadi dictionary
        for name_key, notebook_obj in self.notebooks.items():
            data_to_save[name_key] = notebook_obj.to_dict()
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
        # Memuat data notebook dari file JSON.
        try:
            # Buka file dalam mode baca (read) dengan encoding utf-8
            with open(self.data_file, "r", encoding="utf-8") as f:
                loaded_data = json.load(f) # Baca data JSON dari file
                self.notebooks = {} # Kosongkan dictionary notebooks saat ini
                # Iterasi melalui data yang dimuat dan buat kembali objek Notebook
                for name_key, notebook_data_dict in loaded_data.items():
                    # Gunakan staticmethod from_dict dari kelas Notebook untuk membuat instance
                    self.notebooks[name_key] = Notebook.from_dict(notebook_data_dict)
            print(f"Data berhasil dimuat dari '{self.data_file}'.")
        except FileNotFoundError:
            # Jika file tidak ditemukan, tampilkan pesan dan mulai dengan dictionary kosong
            print(f"File data '{self.data_file}' tidak ditemukan. Memulai dengan notebook default.")
            self.notebooks = {}
        except json.JSONDecodeError:
            # Jika file JSON tidak valid, tampilkan pesan dan mulai dengan dictionary kosong
            print(f"Gagal memuat data. File '{self.data_file}' memiliki format JSON yang tidak valid.")
            self.notebooks = {}
        except Exception as e:
            # Tangani error umum lainnya saat memuat data
            print(f"Terjadi kesalahan tak terduga saat memuat data: {e}")
            self.notebooks = {}

    def add_custom_notebook(self):
        # Memungkinkan pengguna untuk menambahkan notebook baru secara manual.
        name = input("Masukkan nama notebook baru: ")
        # Periksa apakah notebook dengan nama yang sama (case-insensitive) sudah ada
        if name.lower() in self.notebooks:
            print("Notebook dengan nama tersebut sudah ada.")
        else:
            # Jika belum ada, buat objek Notebook baru dan tambahkan ke dictionary
            self.notebooks[name.lower()] = Notebook(name)
            print(f"Notebook '{name}' berhasil ditambahkan.")
            # Simpan perubahan ke file JSON
            self.save_data_ke_json()
            
    def display_all_notebooks(self):
        # Menampilkan daftar semua notebook yang tersedia kepada pengguna.
        print("\n--- Daftar Notebook Tersedia ---")
        if not self.notebooks:
            print("Belum ada notebook.")
            return
        # Iterasi melalui kunci (nama lowercase) dari dictionary notebooks dan tampilkan nama aslinya
        for i, name_key in enumerate(self.notebooks.keys()):
            # Ambil nama asli notebook dari objek Notebook
            print(f"{i + 1}. {self.notebooks[name_key].name}") 

    def select_notebook(self):
        # Memungkinkan pengguna untuk memilih notebook dari daftar yang ditampilkan.
        self.display_all_notebooks() # Tampilkan dulu semua notebook yang ada
        if not self.notebooks:
            return None # Tidak ada notebook untuk dipilih
        
        try:
            choice = int(input("Pilih nomor notebook: "))
            # Dapatkan daftar kunci (nama lowercase) dari dictionary notebooks
            notebook_keys = list(self.notebooks.keys())
            # Validasi pilihan pengguna
            if 1 <= choice <= len(notebook_keys):
                selected_key = notebook_keys[choice - 1] # Ambil kunci berdasarkan pilihan (choice - 1 karena list 0-indexed)
                return self.notebooks[selected_key] # Kembalikan objek Notebook yang dipilih
            else:
                print("Pilihan tidak valid.")
                return None        
        except ValueError:
            # Tangani jika input pengguna bukan angka
            print("Input harus berupa angka.")
            return None

    def notebook_menu(self, current_notebook):
        # Menampilkan menu operasi untuk notebook yang sedang dipilih.
        while True:
            print(f"\n--- Menu Notebook: {current_notebook.name} ---")
            print("1. Tambah Catatan Baru")
            print("2. Lihat Semua Catatan")
            print("3. Edit Catatan")
            print("4. Hapus Catatan")
            print("5. Urutkan Catatan (Berdasarkan Judul)")
            print("6. Urutkan Catatan (Berdasarkan Tanggal)")
            print("7. Cari Catatan (Berdasarkan Judul)")
            print("8. Ekspor Catatan ke File Teks (.txt)")
            print("9. Kembali ke Menu Utama")
            choice = input("Pilihan: ")

            # Setiap operasi yang mengubah data (tambah, edit, hapus, urutkan) akan diikuti dengan penyimpanan data.
            if choice == '1':
                current_notebook.add_note()
                self.save_data_ke_json() # Simpan setelah menambah catatan
            elif choice == '2':
                current_notebook.view_notes()
            elif choice == '3':
                current_notebook.edit_note()
                self.save_data_ke_json() # Simpan setelah mengedit catatan
            elif choice == '4':
                current_notebook.delete_note()
                self.save_data_ke_json() # Simpan setelah menghapus catatan
            elif choice == '5':
                current_notebook.sort_notes() # Urutkan berdasarkan judul
                self.save_data_ke_json() # Simpan setelah mengurutkan
            elif choice == '6':
                if current_notebook:
                    current_notebook.sort_notes_by_tanggal() # Urutkan berdasarkan tanggal
                else:
                    print("Tidak ada notebook yang sedang aktif.")
            elif choice == '7':
                current_notebook.search_note()
            elif choice == '8':
                current_notebook.export_notes_to_txt()
            elif choice == '9':
                break # Kembali ke menu utama
            else:
                print("Pilihan tidak valid.")

    def main_loop(self):
        # Loop utama aplikasi yang menampilkan menu utama dan mengarahkan pengguna.
        while True:
            print("\n--- Aplikasi Notebook SDA ---")
            print("1. Pilih Notebook")
            print("2. Tambah Notebook Baru")
            print("3. Tampilkan Semua Notebook")
            print("4. Keluar")
            main_choice = input("Pilihan: ")

            if main_choice == '1':
                # Pengguna memilih untuk masuk ke menu notebook tertentu
                selected_nb = self.select_notebook()
                if selected_nb:
                    self.notebook_menu(selected_nb) # Tampilkan menu untuk notebook yang dipilih
            elif main_choice == '2':
                # Pengguna memilih untuk menambah notebook baru
                self.add_custom_notebook()
            elif main_choice == '3':
                # Pengguna memilih untuk menampilkan semua notebook
                self.display_all_notebooks()
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
    # Membuat instance dari NotebookApplication
    app = NotebookApplication()
    # Memulai loop utama aplikasi
    app.main_loop()