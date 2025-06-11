import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import json
from memobook import Memobook
from struktur_data import SinglyLinkedList, Node

class MemobookGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Memobook SDA - GUI Version")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Data
        self.memobooks = {}
        self.data_file = "memobook_data.json"
        self.current_memobook = None
        
        # Muat data
        self.load_data_dari_json()
        if not self.memobooks:
            self._inisialisasi_default_memobooks()
        
        # Buat GUI
        self.buat_widget()
        self.perbarui_daftar_memobook()
    
    def _inisialisasi_default_memobooks(self):
        """Inisialisasi memobook default jika belum ada."""
        default_subjects = ["Aljabar Abstrak", "Persamaan Diferensial", "Analisis Real", "Struktur Data dan Algoritma"]
        for subject in default_subjects:
            if subject.lower() not in self.memobooks:
                self.memobooks[subject.lower()] = Memobook(subject)
        self.simpan_data_ke_json()
    
    def buat_widget(self):
        """Membuat semua widget GUI."""
        # Frame utama
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Judul aplikasi
        title_label = ttk.Label(main_frame, text="Aplikasi Memobook SDA", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Panel kiri - Daftar Memobook
        left_frame = ttk.LabelFrame(main_frame, text="Daftar Memobook", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Listbox memobook
        self.memobook_listbox = tk.Listbox(left_frame, height=15, width=25)
        self.memobook_listbox.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.memobook_listbox.bind('<<ListboxSelect>>', self.saat_memobook_dipilih)
        
        # Tombol memobook
        ttk.Button(left_frame, text="Tambah Memobook", 
                  command=self.tambah_memobook).grid(row=1, column=0, pady=(10, 5), sticky=tk.W+tk.E)
        ttk.Button(left_frame, text="Hapus Memobook", 
                  command=self.hapus_memobook).grid(row=1, column=1, pady=(10, 5), sticky=tk.W+tk.E)
        
        # Panel tengah - Daftar Memo
        middle_frame = ttk.LabelFrame(main_frame, text="Daftar Memo", padding="10")
        middle_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Treeview memo
        self.memos_tree = ttk.Treeview(middle_frame, columns=('judul', 'tanggal'), 
                                      show='headings', height=15)
        self.memos_tree.heading('judul', text='Judul')
        self.memos_tree.heading('tanggal', text='Tanggal')
        self.memos_tree.column('judul', width=200)
        self.memos_tree.column('tanggal', width=150)
        self.memos_tree.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.memos_tree.bind('<<TreeviewSelect>>', self.saat_memo_dipilih)
        
        # Tombol memo
        memo_button_frame = ttk.Frame(middle_frame)
        memo_button_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0), sticky=tk.W+tk.E)
        
        ttk.Button(memo_button_frame, text="Tambah Memo", 
                  command=self.tambah_memo).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(memo_button_frame, text="Edit Memo", 
                  command=self.edit_memo).pack(side=tk.LEFT, padx=5)
        ttk.Button(memo_button_frame, text="Hapus Memo", 
                  command=self.hapus_memo).pack(side=tk.LEFT, padx=5)
        
        # Tombol Sort
        sort_frame = ttk.Frame(middle_frame)
        sort_frame.grid(row=2, column=0, columnspan=3, pady=(5, 0), sticky=tk.W+tk.E)
        
        ttk.Button(sort_frame, text="Urutkan: Judul", 
                  command=self.urutkan_berdasarkan_judul).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(sort_frame, text="Urutkan: Tanggal", 
                  command=self.urutkan_berdasarkan_tanggal).pack(side=tk.LEFT, padx=5)
        ttk.Button(sort_frame, text="Cari Memo", 
                  command=self.cari_memo).pack(side=tk.LEFT, padx=5)
        ttk.Button(sort_frame, text="Ekspor ke TXT", 
                  command=self.ekspor_memo).pack(side=tk.LEFT, padx=5)
        
        # Panel kanan - Konten Memo
        right_frame = ttk.LabelFrame(main_frame, text="Isi Memo", padding="10")
        right_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Judul memo
        self.memo_judul_var = tk.StringVar()
        ttk.Label(right_frame, text="Judul:").grid(row=0, column=0, sticky=tk.W)
        judul_entry = ttk.Entry(right_frame, textvariable=self.memo_judul_var, 
                               state='readonly', width=40)
        judul_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Tanggal memo
        self.memo_tanggal_var = tk.StringVar()
        ttk.Label(right_frame, text="Tanggal:").grid(row=1, column=0, sticky=tk.W)
        tanggal_entry = ttk.Entry(right_frame, textvariable=self.memo_tanggal_var, 
                              state='readonly', width=40)
        tanggal_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Konten memo
        ttk.Label(right_frame, text="Konten:").grid(row=2, column=0, sticky=tk.W+tk.N)
        self.note_content = scrolledtext.ScrolledText(right_frame, width=50, height=25, 
                                                     state='disabled', wrap=tk.WORD)
        self.note_content.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Konfigurasi bobot grid
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)
        
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_columnconfigure(1, weight=1)
        
        middle_frame.grid_rowconfigure(0, weight=1)
        middle_frame.grid_columnconfigure(0, weight=1)
        
        right_frame.grid_rowconfigure(2, weight=1)
        right_frame.grid_columnconfigure(1, weight=1)
    
    def perbarui_daftar_memobook(self):
        """Memperbarui daftar memobook di listbox."""
        self.memobook_listbox.delete(0, tk.END)
        for memobook in self.memobooks.values():
            self.memobook_listbox.insert(tk.END, memobook.name)
    
    def perbarui_daftar_memo(self):
        """Memperbarui daftar memo di treeview."""
        # Hapus item yang sudah ada
        for item in self.memos_tree.get_children():
            self.memos_tree.delete(item)
        
        if not self.current_memobook or self.current_memobook.memos_list.is_empty():
            return
        
        # Tambahkan memo ke treeview
        current = self.current_memobook.memos_list.head
        while current:
            memo = current.data
            self.memos_tree.insert('', tk.END, values=(memo.judul, memo.created_tanggal))
            current = current.next
    
    def saat_memobook_dipilih(self, event):
        """Handler ketika memobook dipilih."""
        selection = self.memobook_listbox.curselection()
        if selection:
            memobook_name = self.memobook_listbox.get(selection[0])
            # Cari memobook berdasarkan nama
            for memobook in self.memobooks.values():
                if memobook.name == memobook_name:
                    self.current_memobook = memobook
                    break
            self.perbarui_daftar_memo()
            self.bersihkan_tampilan_memo()
    
    def saat_memo_dipilih(self, event):
        """Handler ketika memo dipilih."""
        selection = self.memos_tree.selection()
        if selection and self.current_memobook:
            item = self.memos_tree.item(selection[0])
            memo_judul = item['values'][0]
            
            # Cari memo
            current = self.current_memobook.memos_list.head
            while current:
                if current.data.judul == memo_judul:
                    self.tampilkan_memo(current.data)
                    break
                current = current.next
    
    def tampilkan_memo(self, memo):
        """Menampilkan isi memo di panel kanan."""
        self.memo_judul_var.set(memo.judul)
        self.memo_tanggal_var.set(memo.created_tanggal)
        
        self.note_content.config(state='normal')
        self.note_content.delete(1.0, tk.END)
        self.note_content.insert(1.0, memo.content)
        self.note_content.config(state='disabled')
    
    def bersihkan_tampilan_memo(self):
        """Membersihkan tampilan memo."""
        self.memo_judul_var.set("")
        self.memo_tanggal_var.set("")
        self.note_content.config(state='normal')
        self.note_content.delete(1.0, tk.END)
        self.note_content.config(state='disabled')
    
    def tambah_memobook(self):
        """Menambah memobook baru."""
        name = simpledialog.askstring("Tambah Memobook", "Masukkan nama memobook baru:")
        if name:
            if name.lower() in self.memobooks:
                messagebox.showerror("Error", "Memobook dengan nama tersebut sudah ada.")
            else:
                self.memobooks[name.lower()] = Memobook(name)
                self.perbarui_daftar_memobook()
                self.simpan_data_ke_json()
                messagebox.showinfo("Sukses", f"Memobook '{name}' berhasil ditambahkan.")
    
    def hapus_memobook(self):
        """Menghapus memobook yang dipilih."""
        selection = self.memobook_listbox.curselection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih memobook yang akan dihapus.")
            return
        
        memobook_name = self.memobook_listbox.get(selection[0])
        result = messagebox.askyesno("Konfirmasi", 
                                   f"Apakah Anda yakin ingin menghapus memobook '{memobook_name}'?")
        if result:
            # Cari dan hapus memobook
            for key, memobook in list(self.memobooks.items()):
                if memobook.name == memobook_name:
                    del self.memobooks[key]
                    break
            
            self.current_memobook = None
            self.perbarui_daftar_memobook()
            self.perbarui_daftar_memo()
            self.bersihkan_tampilan_memo()
            self.simpan_data_ke_json()
            messagebox.showinfo("Sukses", f"Memobook '{memobook_name}' berhasil dihapus.")
    
    def tambah_memo(self):
        """Menambah memo baru."""
        if not self.current_memobook:
            messagebox.showwarning("Peringatan", "Pilih memobook terlebih dahulu.")
            return
        
        dialog = MemoDialog(self.root, "Tambah Memo Baru")
        if dialog.result:
            judul, content = dialog.result
            
            # Periksa apakah judul sudah ada
            if self.current_memobook.memos_list.cari_node_by_judul(judul):
                messagebox.showerror("Error", "Memo dengan judul tersebut sudah ada.")
                return
            
            # Tambah memo
            from memobook.memo import Memo
            new_memo = Memo(judul, content)
            self.current_memobook.memos_list.appends(new_memo)
            
            self.perbarui_daftar_memo()
            self.simpan_data_ke_json()
            messagebox.showinfo("Sukses", f"Memo '{judul}' berhasil ditambahkan.")
    
    def edit_memo(self):
        """Mengedit memo yang dipilih."""
        selection = self.memos_tree.selection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih memo yang akan diedit.")
            return
        
        item = self.memos_tree.item(selection[0])
        memo_judul = item['values'][0]
        
        # Cari memo
        memo_node = self.current_memobook.memos_list.cari_node_by_judul(memo_judul)

        if memo_node:
            memo_to_edit = memo_node.data
            dialog = MemoDialog(self.root, f"Edit Memo: {memo_judul}", 
                                memo_judul=memo_to_edit.judul, memo_content=memo_to_edit.content)
            if dialog.result:
                new_judul, new_content = dialog.result
                
                # Periksa apakah judul baru bertentangan dengan memo yang ada
                if new_judul != memo_to_edit.judul:
                    existing = self.current_memobook.memos_list.cari_node_by_judul(new_judul)
                    if existing:
                        messagebox.showerror("Error", "Judul sudah digunakan oleh memo lain.")
                        return
                
                # Perbarui memo
                memo_to_edit.update_judul(new_judul)
                memo_to_edit.update_content(new_content)
                
                self.perbarui_daftar_memo()
                self.simpan_data_ke_json()
                messagebox.showinfo("Sukses", "Memo berhasil diupdate.")
    
    def hapus_memo(self):
        """Menghapus memo yang dipilih."""
        selection = self.memos_tree.selection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih memo yang akan dihapus.")
            return
        
        item = self.memos_tree.item(selection[0])
        memo_judul = item['values'][0]
        
        result = messagebox.askyesno("Konfirmasi", 
                                   f"Apakah Anda yakin ingin menghapus memo '{memo_judul}'?")
        if result:
            self.current_memobook.memos_list.delete_node_by_judul(memo_judul)
            self.perbarui_daftar_memo()
            self.bersihkan_tampilan_memo()
            self.simpan_data_ke_json()
            messagebox.showinfo("Sukses", f"Memo '{memo_judul}' berhasil dihapus.")
    
    def urutkan_berdasarkan_judul(self):
        """Mengurutkan memo berdasarkan judul."""
        if not self.current_memobook:
            messagebox.showwarning("Peringatan", "Pilih memobook terlebih dahulu.")
            return
        
        self.current_memobook.sort_memos()
        self.perbarui_daftar_memo()
        self.simpan_data_ke_json()
        messagebox.showinfo("Sukses", "Memo berhasil diurutkan berdasarkan judul.")
    
    def urutkan_berdasarkan_tanggal(self):
        """Mengurutkan memo berdasarkan tanggal."""
        if not self.current_memobook:
            messagebox.showwarning("Peringatan", "Pilih memobook terlebih dahulu.")
            return
        
        self.current_memobook.sort_memos_by_tanggal()
        self.perbarui_daftar_memo()
        self.simpan_data_ke_json()
        messagebox.showinfo("Sukses", "Memo berhasil diurutkan berdasarkan tanggal.")
    
    def cari_memo(self):
        """Mencari memo berdasarkan judul."""
        if not self.current_memobook:
            messagebox.showwarning("Peringatan", "Pilih memobook terlebih dahulu.")
            return
        
        judul = simpledialog.askstring("Cari Memo", "Masukkan judul memo yang dicari:")
        if judul:
            node = self.current_memobook.memos_list.cari_node_by_judul(judul)
            if node:
                # Pilih memo di treeview
                for item in self.memos_tree.get_children():
                    if self.memos_tree.item(item)['values'][0] == node.data.judul:
                        self.memos_tree.selection_set(item)
                        self.memos_tree.focus(item)
                        self.tampilkan_memo(node.data)
                        break
                messagebox.showinfo("Ditemukan", f"Memo '{judul}' ditemukan dan dipilih.")
            else:
                messagebox.showinfo("Tidak Ditemukan", f"Memo '{judul}' tidak ditemukan.")
    
    def ekspor_memo(self):
        """Mengekspor memo ke file TXT."""
        if not self.current_memobook:
            messagebox.showwarning("Peringatan", "Pilih memobook terlebih dahulu.")
            return
        
        try:
            self.current_memobook.export_memos_to_txt()
            messagebox.showinfo("Sukses", "Memo berhasil diekspor ke file TXT.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengekspor memo: {str(e)}")
    
    def simpan_data_ke_json(self):
        """Menyimpan data ke file JSON."""
        data_to_save = {}
        for name_key, memobook_obj in self.memobooks.items():
            data_to_save[name_key] = memobook_obj.to_dict()
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan data: {str(e)}")
    
    def load_data_dari_json(self):
        """Memuat data dari file JSON."""
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                loaded_data = json.load(f)
                self.memobooks = {}
                for name_key, memobook_data_dict in loaded_data.items():
                    self.memobooks[name_key] = Memobook.from_dict(memobook_data_dict)
        except FileNotFoundError:
            self.memobooks = {}
        except json.JSONDecodeError:
            self.memobooks = {}
            messagebox.showerror("Error", "File data memiliki format JSON yang tidak valid.")
        except Exception as e:
            self.memobooks = {}
            messagebox.showerror("Error", f"Terjadi kesalahan saat memuat data: {str(e)}")

class MemoDialog:
    def __init__(self, parent, title, memo_judul="", memo_content=""):
        self.result = None
        
        # Buat dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("600x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Pusatkan dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Buat widget
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Judul
        ttk.Label(main_frame, text="Judul:").pack(anchor=tk.W)
        self.judul_entry = ttk.Entry(main_frame, width=60)
        self.judul_entry.pack(fill=tk.X, pady=(0, 10))
        self.judul_entry.insert(0, memo_judul)
        
        # Konten
        ttk.Label(main_frame, text="Konten:").pack(anchor=tk.W)
        self.content_text = scrolledtext.ScrolledText(main_frame, width=60, height=15, wrap=tk.WORD)
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.content_text.insert(1.0, memo_content)
        
        # Tombol
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Simpan", command=self.simpan).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Batal", command=self.batal).pack(side=tk.RIGHT)
        
        # Fokus pada entry judul
        self.judul_entry.focus()
        
        # Bind tombol Enter untuk simpan
        self.dialog.bind('<Return>', self.saat_enter_ditekan)
        self.dialog.bind('<Escape>', self.saat_escape_ditekan)
        
        # Tunggu dialog ditutup
        self.dialog.wait_window()
    
    def simpan(self):
        judul = self.judul_entry.get().strip()
        content = self.content_text.get(1.0, tk.END).strip()
        
        if not judul:
            messagebox.showerror("Error", "Judul tidak boleh kosong.")
            return
        
        if not content:
            messagebox.showerror("Error", "Konten tidak boleh kosong.")
            return
        
        self.result = (judul, content)
        self.dialog.destroy()
    
    def batal(self):
        self.dialog.destroy()
    
    def saat_enter_ditekan(self, event):
        """Handler untuk tombol Enter - simpan memo."""
        self.simpan()
    
    def saat_escape_ditekan(self, event):
        """Handler untuk tombol Escape - batalkan dialog."""
        self.batal()

def main():
    root = tk.Tk()
    app = MemobookGUI(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
