from struktur_data import SinglyLinkedList
from .memo import Memo

class Memobook:
    """Mewakili satu memobook (mata kuliah) yang berisi banyak Memo."""
    def __init__(self, name):
        # Inisialisasi objek Memobook dengan nama dan sebuah SinglyLinkedList kosong untuk menyimpan memo.
        self.name = name  # Nama memobook (misalnya, nama mata kuliah)
        self.memos_list = SinglyLinkedList()  # Daftar memo dalam memobook ini

    def add_memo(self):
        # Menambahkan memo baru ke dalam memobook.
        title = input("Masukkan title memo: ")
        # Periksa apakah title sudah ada untuk menghindari duplikasi
        if self.memos_list.find_node_by_title(title):
            print("Memo dengan title tersebut sudah ada. Gunakan title lain.")
            return

        print("Masukkan isi memo (tekan Enter dua kali untuk selesai):")
        full_content = ""
        # Membaca input multi-baris untuk konten memo
        first_line = True
        while True:
            line = input()
            if line == "":  # Input selesai jika baris kosong ditekan
                break
            if first_line:
                full_content = line
                first_line = False
            else:
                full_content += "\n" + line

        new_memo = Memo(title, full_content)  # Buat objek Memo baru
        self.memos_list.appends(new_memo)  # Tambahkan Memo ke linked list
        print(f"Memo '{title}' berhasil ditambahkan ke memobook '{self.name}'.")

    def view_memos(self):
        # Menampilkan semua memo yang ada di dalam memobook.
        print(f"\n--- Memo di Memobook: {self.name} ---")
        self.memos_list.display()  # Panggil metode display dari SinglyLinkedList

    def edit_memo(self):
        # Mengedit title atau konten dari memo yang sudah ada.
        title_to_edit = input("Masukkan title memo yang ingin diedit: ")
        node_to_edit = self.memos_list.find_node_by_title(title_to_edit)

        if node_to_edit:
            print("Memo ditemukan. Apa yang ingin Anda edit?")
            print("1. title")
            print("2. Konten")
            choice = input("Pilihan (1/2): ")

            if choice == '1':
                # Edit title memo
                new_title = input("Masukkan title baru: ")
                # Periksa apakah title baru sudah digunakan oleh memo lain
                ada_new_title = self.memos_list.find_node_by_title(new_title)
                if ada_new_title and ada_new_title != node_to_edit:
                    print("title baru sudah digunakan oleh memo lain. Gagal mengedit.")
                else:
                    node_to_edit.data.update_title(new_title)
                    print("title memo berhasil diupdate.")
            elif choice == '2':
                # Edit konten memo
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
                        new_content += "\n" + line
                node_to_edit.data.update_content(new_content)
                print("Konten memo berhasil diupdate.")
            else:
                print("Pilihan tidak valid.")
        else:
            print(f"Memo '{title_to_edit}' tidak ditemukan.")

    def delete_memo(self):
        # Menghapus memo dari memobook berdasarkan title.
        title_to_delete = input("Masukkan title memo yang ingin dihapus: ")
        self.memos_list.delete_node_by_title(title_to_delete)  # Panggil metode delete dari SinglyLinkedList

    def sort_memos(self):
        # Mengurutkan memo dalam memobook berdasarkan title (A-Z).
        self.memos_list.insertion_sort_by_title()

    def sort_memos_by_date(self):
        """Mengurutkan memo berdasarkan tanggal pembuatan (dari yang terlama ke terbaru)."""
        self.memos_list.insertion_sort_by_tanggal()

    def search_memo(self):
        # Mencari memo dalam memobook berdasarkan title.
        title_to_search = input("Masukkan title memo yang ingin dicari: ")
        self.memos_list.linear_search_by_title(title_to_search)  # Panggil metode search dari SinglyLinkedList

    def to_dict(self):
        # Mengkonversi objek Memobook (termasuk semua memonya) menjadi dictionary.
        # Berguna untuk menyimpan data Memobook ke format JSON.
        return {
            "name": self.name,
            "memos": self.memos_list.to_list_of_dicts()
        }

    @staticmethod
    def from_dict(data):
        "Membuat objek Memobook dari dictionary (data dari JSON)."
        memobook = Memobook(data["name"])  # Buat instance Memobook baru
        # Muat memo dari list of dictionaries ke dalam SinglyLinkedList milik memobook
        memobook.memos_list.load_from_list_of_dicts(data["memos"])
        return memobook

    def export_memos_to_txt(self):
        # Mengekspor semua memo dalam memobook ke sebuah file teks (.txt).
        if self.memos_list.is_empty():
            print(f"Memobook '{self.name}' tidak memiliki memo untuk diekspor.")
            return

        # Membuat nama file yang aman dari nama memobook (mengganti karakter non-alphanumeric dengan '_')
        filename_safe_name = "".join(c if c.isalnum() else "_" for c in self.name)
        filename = f"memobook_{filename_safe_name}_export.txt"

        try:
            # Membuka file dalam mode tulis (write) dengan encoding utf-8
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"--- Memo dari Memobook: {self.name} ---\n\n")
                current = self.memos_list.head
                memo_count = 1
                # Iterasi melalui semua memo dan tulis ke file
                while current:
                    f.write(f"--- Memo {memo_count} ---\n")
                    f.write(f"title: {current.data.title}\n")
                    f.write(f"Tanggal: {current.data.created_tanggal}\n")  # Menambahkan tanggal ke ekspor
                    f.write("Konten:\n")
                    f.write(current.data.content)
                    f.write("\n\n--------------------------\n\n")
                    current = current.next
                    memo_count += 1
            print(f"Memo dari memobook '{self.name}' berhasil diekspor ke '{filename}'.")
        except IOError:
            # Menangani kemungkinan error saat operasi file
            print(f"Gagal mengekspor memo. Terjadi kesalahan saat menulis ke file '{filename}'.")
