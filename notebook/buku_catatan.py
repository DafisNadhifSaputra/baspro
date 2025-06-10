from struktur_data import SinglyLinkedList, Node
from .catatan import Note


class Notebook:
    """Mewakili satu buku catatan (mata kuliah) yang berisi banyak Note."""    
    def __init__(self, name):
        # Inisialisasi objek Notebook dengan nama dan sebuah SinglyLinkedList kosong untuk menyimpan catatan.
        self.name = name  # Nama buku catatan (misalnya, nama mata kuliah)
        self.notes_list = SinglyLinkedList() # Daftar catatan dalam buku catatan ini

    def add_note(self):
        # Menambahkan catatan baru ke dalam buku catatan.
        judul = input("Masukkan judul catatan: ")
        # Periksa apakah judul sudah ada untuk menghindari duplikasi
        if self.notes_list.find_node_by_judul(judul):
            print("Catatan dengan judul tersebut sudah ada. Gunakan judul lain.")
            return
        
        print("Masukkan isi catatan (tekan Enter dua kali untuk selesai):")
        full_content = ""
        # Membaca input multi-baris untuk konten catatan
        first_line = True
        while True:
            line = input()
            if line == "": # Input selesai jika baris kosong ditekan
                break
            if first_line:
                full_content = line
                first_line = False
            else:
                full_content += "\\n" + line
        
        new_note = Note(judul, full_content) # Buat objek Note baru
        self.notes_list.appends(new_note)    # Tambahkan Note ke linked list
        print(f"Catatan '{judul}' berhasil ditambahkan ke notebook '{self.name}'.")

    def view_notes(self):
        # Menampilkan semua catatan yang ada di dalam buku catatan.
        print(f"\n--- Catatan di Notebook: {self.name} ---")
        self.notes_list.display() # Panggil metode display dari SinglyLinkedList

    def edit_note(self):
        # Mengedit judul atau konten dari catatan yang sudah ada.
        judul_to_edit = input("Masukkan judul catatan yang ingin diedit: ")
        node_to_edit = self.notes_list.find_node_by_judul(judul_to_edit)
        
        if node_to_edit:
            print("Catatan ditemukan. Apa yang ingin Anda edit?")
            print("1. Judul")
            print("2. Konten")
            choice = input("Pilihan (1/2): ")
            
            if choice == '1':
                # Edit judul catatan
                new_judul = input("Masukkan judul baru: ")
                # Periksa apakah judul baru sudah digunakan oleh catatan lain
                ada_new_judul = self.notes_list.find_node_by_judul(new_judul)
                if ada_new_judul and ada_new_judul != node_to_edit:
                    print("Judul baru sudah digunakan oleh catatan lain. Gagal mengedit.")
                else:                    
                    node_to_edit.data.update_judul(new_judul)
                    print("Judul catatan berhasil diupdate.")
            elif choice == '2':
                # Edit konten catatan
                print("Masukkan konten baru (tekan Enter dua kali untuk selesai):")
                new_content = ""
                first_line = True
                while True:
                    line = input()
                    if line == "":
                        break
                    if first_line:
                        new_content = line
                        first_line = False
                    else:
                        new_content += "\\n" + line
                node_to_edit.data.update_content(new_content)
                print("Konten catatan berhasil diupdate.")
            else:
                print("Pilihan tidak valid.")
        else:
            print(f"Catatan '{judul_to_edit}' tidak ditemukan.")

    def delete_note(self):
        # Menghapus catatan dari buku catatan berdasarkan judul.
        judul_to_delete = input("Masukkan judul catatan yang ingin dihapus: ")
        self.notes_list.delete_node_by_judul(judul_to_delete) # Panggil metode delete dari SinglyLinkedList

    def sort_notes(self):
        # Mengurutkan catatan dalam buku catatan berdasarkan judul (A-Z).
        self.notes_list.insertion_sort_by_judul()

    def sort_notes_by_date(self):
        """Mengurutkan catatan berdasarkan tanggal pembuatan (dari yang terlama ke terbaru)."""
        self.notes_list.insertion_sort_by_date()

    def search_note(self):
        # Mencari catatan dalam buku catatan berdasarkan judul.
        judul_to_search = input("Masukkan judul catatan yang ingin dicari: ")
        self.notes_list.linear_search_by_judul(judul_to_search) # Panggil metode search dari SinglyLinkedList

    def to_dict(self):
        # Mengkonversi objek Notebook (termasuk semua catatannya) menjadi dictionary.
        # Berguna untuk menyimpan data Notebook ke format JSON.
        return {
            "name": self.name,
            "notes": self.notes_list.to_list_of_dicts()
        }

    @staticmethod
    def from_dict(data):
        "Membuat objek Notebook dari dictionary (data dari JSON)."
        notebook = Notebook(data["name"]) # Buat instance Notebook baru
        # Muat catatan dari list of dictionaries ke dalam SinglyLinkedList milik notebook
        notebook.notes_list.load_from_list_of_dicts(data["notes"])
        return notebook

    def export_notes_to_txt(self):
        # Mengekspor semua catatan dalam notebook ke sebuah file teks (.txt).
        if self.notes_list.is_empty():
            print(f"Notebook '{self.name}' tidak memiliki catatan untuk diekspor.")
            return
        
        # Membuat nama file yang aman dari nama notebook (mengganti karakter non-alphanumeric dengan '_')
        filename_safe_name = "".join(c if c.isalnum() else "_" for c in self.name)
        filename = f"notebook_{filename_safe_name}_export.txt"
        
        try:
            # Membuka file dalam mode tulis (write) dengan encoding utf-8
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"--- Catatan dari Notebook: {self.name} ---\n\n")
                current = self.notes_list.head
                note_count = 1
                # Iterasi melalui semua catatan dan tulis ke file
                while current:
                    f.write(f"--- Catatan {note_count} ---\n")
                    f.write(f"Judul: {current.data.judul}\n")
                    f.write(f"Tanggal: {current.data.created_date}\n") # Menambahkan tanggal ke ekspor
                    f.write("Konten:\n")
                    f.write(current.data.content)
                    f.write("\n\n--------------------------\n\n")
                    current = current.next
                    note_count +=1
            print(f"Catatan dari notebook '{self.name}' berhasil diekspor ke '{filename}'.")
        except IOError:
            # Menangani kemungkinan error saat operasi file
            print(f"Gagal mengekspor catatan. Terjadi kesalahan saat menulis ke file '{filename}'.")
