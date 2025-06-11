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
        
        # Load data
        self.load_data_dari_json()
        if not self.memobooks:
            self._inisialisasi_default_memobooks()
        
        # Create GUI
        self.create_widgets()
        self.refresh_memobook_list()
    
    def _inisialisasi_default_memobooks(self):
        """Inisialisasi notebook default jika belum ada."""
        default_subjects = ["Aljabar Abstrak", "Persamaan Diferensial", "Analisis Real", "Struktur Data dan Algoritma"]
        for subject in default_subjects:
            if subject.lower() not in self.memobooks:
                self.memobooks[subject.lower()] = Memobook(subject)
        self.save_data_ke_json()
    
    def create_widgets(self):
        """Membuat semua widget GUI."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # title
        title_label = ttk.Label(main_frame, text="Aplikasi Memobook SDA", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Left panel - Notebook list
        left_frame = ttk.LabelFrame(main_frame, text="Daftar Memobook", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Notebook listbox
        self.memobook_listbox = tk.Listbox(left_frame, height=15, width=25)
        self.memobook_listbox.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.memobook_listbox.bind('<<ListboxSelect>>', self.on_memobook_select)
        
        # Notebook buttons
        ttk.Button(left_frame, text="Tambah Memobook", 
                  command=self.add_memobook).grid(row=1, column=0, pady=(10, 5), sticky=tk.W+tk.E)
        ttk.Button(left_frame, text="Hapus Memobook", 
                  command=self.delete_memobook).grid(row=1, column=1, pady=(10, 5), sticky=tk.W+tk.E)
        
        # Middle panel - Notes list
        middle_frame = ttk.LabelFrame(main_frame, text="Daftar Memo", padding="10")
        middle_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Notes treeview
        self.memos_tree = ttk.Treeview(middle_frame, columns=('title', 'tanggal'), 
                                      show='headings', height=15)
        self.memos_tree.heading('title', text='title')
        self.memos_tree.heading('tanggal', text='Tanggal')
        self.memos_tree.column('title', width=200)
        self.memos_tree.column('tanggal', width=150)
        self.memos_tree.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.memos_tree.bind('<<TreeviewSelect>>', self.on_memo_select)
        
        # Notes buttons
        notes_button_frame = ttk.Frame(middle_frame)
        notes_button_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0), sticky=tk.W+tk.E)
        
        ttk.Button(notes_button_frame, text="Tambah Memo", 
                  command=self.add_memo).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(notes_button_frame, text="Edit Memo", 
                  command=self.edit_memo).pack(side=tk.LEFT, padx=5)
        ttk.Button(notes_button_frame, text="Hapus Memo", 
                  command=self.delete_memo).pack(side=tk.LEFT, padx=5)
        
        # Sort buttons
        sort_frame = ttk.Frame(middle_frame)
        sort_frame.grid(row=2, column=0, columnspan=3, pady=(5, 0), sticky=tk.W+tk.E)
        
        ttk.Button(sort_frame, text="Urutkan: title", 
                  command=self.sort_by_title).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(sort_frame, text="Urutkan: Tanggal", 
                  command=self.sort_by_tanggal).pack(side=tk.LEFT, padx=5)
        ttk.Button(sort_frame, text="Cari Memo", 
                  command=self.search_memo).pack(side=tk.LEFT, padx=5)
        ttk.Button(sort_frame, text="Ekspor ke TXT", 
                  command=self.export_memos).pack(side=tk.LEFT, padx=5)
        
        # Right panel - Note content
        right_frame = ttk.LabelFrame(main_frame, text="Isi Memo", padding="10")
        right_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Note title
        self.memo_title_var = tk.StringVar()
        ttk.Label(right_frame, text="title:").grid(row=0, column=0, sticky=tk.W)
        title_entry = ttk.Entry(right_frame, textvariable=self.memo_title_var, 
                               state='readonly', width=40)
        title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Note tanggal
        self.memo_tanggal_var = tk.StringVar()
        ttk.Label(right_frame, text="Tanggal:").grid(row=1, column=0, sticky=tk.W)
        tanggal_entry = ttk.Entry(right_frame, textvariable=self.memo_tanggal_var, 
                              state='readonly', width=40)
        tanggal_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Note content
        ttk.Label(right_frame, text="Konten:").grid(row=2, column=0, sticky=tk.W+tk.N)
        self.note_content = scrolledtext.ScrolledText(right_frame, width=50, height=25, 
                                                     state='disabled', wrap=tk.WORD)
        self.note_content.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Configure grid weights
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
    
    def refresh_memobook_list(self):
        """Memperbarui daftar notebook di listbox."""
        self.memobook_listbox.delete(0, tk.END)
        for notebook in self.memobooks.values():
            self.memobook_listbox.insert(tk.END, notebook.name)
    
    def refresh_memos_list(self):
        """Memperbarui daftar memo di treeview."""
        # Clear existing items
        for item in self.memos_tree.get_children():
            self.memos_tree.delete(item)
        
        if not self.current_memobook or self.current_memobook.notes_list.is_empty():
            return
        
        # Add notes to treeview
        current = self.current_memobook.notes_list.head
        while current:
            memo = current.data
            self.memos_tree.insert('', tk.END, values=(memo.title, memo.created_tanggal))
            current = current.next
    
    def on_memobook_select(self, event):
        """Handler ketika notebook dipilih."""
        selection = self.memobook_listbox.curselection()
        if selection:
            memobook_name = self.memobook_listbox.get(selection[0])
            # Find notebook by name
            for notebook in self.memobooks.values():
                if notebook.name == memobook_name:
                    self.current_memobook = notebook
                    break
            self.refresh_memos_list()
            self.clear_memo_display()
    
    def on_memo_select(self, event):
        """Handler ketika memo dipilih."""
        selection = self.memos_tree.selection()
        if selection and self.current_memobook:
            item = self.memos_tree.item(selection[0])
            memo_title = item['values'][0]
            
            # Find the memo
            current = self.current_memobook.notes_list.head
            while current:
                if current.data.title == memo_title:
                    self.display_memo(current.data)
                    break
                current = current.next
    
    def display_memo(self, memo):
        """Menampilkan isi memo di panel kanan."""
        self.note_title_var.set(memo.title)
        self.note_tanggal_var.set(memo.created_tanggal)
        
        self.note_content.config(state='normal')
        self.note_content.delete(1.0, tk.END)
        self.note_content.insert(1.0, memo.content)
        self.note_content.config(state='disabled')
    
    def clear_memo_display(self):
        """Membersihkan tampilan memo."""
        self.memo_title_var.set("")
        self.memo_tanggal_var.set("")
        self.note_content.config(state='normal')
        self.note_content.delete(1.0, tk.END)
        self.note_content.config(state='disabled')
    
    def add_memobook(self):
        """Menambah notebook baru."""
        name = simpledialog.askstring("Tambah Memobook", "Masukkan nama memobook baru:")
        if name:
            if name.lower() in self.memobooks:
                messagebox.showerror("Error", "Memobook dengan nama tersebut sudah ada.")
            else:
                self.memobooks[name.lower()] = Memobook(name)
                self.refresh_memobook_list()
                self.save_data_ke_json()
                messagebox.showinfo("Sukses", f"Memobook '{name}' berhasil ditambahkan.")
    
    def delete_memobook(self):
        """Menghapus notebook yang dipilih."""
        selection = self.memobook_listbox.curselection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih memobook yang akan dihapus.")
            return
        
        memobook_name = self.memobook_listbox.get(selection[0])
        result = messagebox.askyesno("Konfirmasi", 
                                   f"Apakah Anda yakin ingin menghapus memobook '{memobook_name}'?")
        if result:
            # Find and delete notebook
            for key, notebook in list(self.memobooks.items()):
                if notebook.name == memobook_name:
                    del self.memobooks[key]
                    break
            
            self.current_memobook = None
            self.refresh_memobook_list()
            self.refresh_memos_list()
            self.clear_memo_display()
            self.save_data_ke_json()
            messagebox.showinfo("Sukses", f"Memobook '{memobook_name}' berhasil dihapus.")
    
    def add_memo(self):
        """Menambah memo baru."""
        if not self.current_memobook:
            messagebox.showwarning("Peringatan", "Pilih memobook terlebih dahulu.")
            return
        
        dialog = MemoDialog(self.root, "Tambah Memo Baru")
        if dialog.result:
            title, content = dialog.result
            
            # Check if title already exists
            if self.current_memobook.notes_list.find_node_by_title(title):
                messagebox.showerror("Error", "Memo dengan title tersebut sudah ada.")
                return
            
            # Add memo
            from memobook.memo import Memo
            new_memo = Memo(title, content)
            self.current_memobook.notes_list.appends(new_memo)
            
            self.refresh_memos_list()
            self.save_data_ke_json()
            messagebox.showinfo("Sukses", f"Memo '{title}' berhasil ditambahkan.")
    
    def edit_memo(self):
        """Mengedit memo yang dipilih."""
        selection = self.memos_tree.selection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih memo yang akan diedit.")
            return
        
        item = self.memos_tree.item(selection[0])
        memo_title = item['values'][0]
        
        # Find the memo
        memo_node = self.current_memobook.notes_list.find_node_by_title(memo_title)

        if memo_node:
            memo_to_edit = memo_node.data
            dialog = MemoDialog(self.root, f"Edit Memo: {memo_title}", 
                                memo_title=memo_to_edit.title, memo_content=memo_to_edit.content)
            if dialog.result:
                new_title, new_content = dialog.result
                
                # Check if new title conflicts with existing memos
                if new_title != memo_to_edit.title:
                    existing = self.current_memobook.notes_list.find_node_by_title(new_title)
                    if existing:
                        messagebox.showerror("Error", "title sudah digunakan oleh memo lain.")
                        return
                
                # Update memo
                memo_to_edit.update_title(new_title)
                memo_to_edit.update_content(new_content)
                
                self.refresh_memos_list()
                self.save_data_ke_json()
                messagebox.showinfo("Sukses", "Memo berhasil diupdate.")
    
    def delete_memo(self):
        """Menghapus memo yang dipilih."""
        selection = self.memos_tree.selection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih memo yang akan dihapus.")
            return
        
        item = self.memos_tree.item(selection[0])
        memo_title = item['values'][0]
        
        result = messagebox.askyesno("Konfirmasi", 
                                   f"Apakah Anda yakin ingin menghapus memo '{memo_title}'?")
        if result:
            self.current_memobook.notes_list.delete_node_by_title(memo_title)
            self.refresh_memos_list()
            self.clear_memo_display()
            self.save_data_ke_json()
            messagebox.showinfo("Sukses", f"Memo '{memo_title}' berhasil dihapus.")
    
    def sort_by_title(self):
        """Mengurutkan memo berdasarkan title."""
        if not self.current_memobook:
            messagebox.showwarning("Peringatan", "Pilih memobook terlebih dahulu.")
            return
        
        self.current_memobook.sort_memos()
        self.refresh_memos_list()
        self.save_data_ke_json()
        messagebox.showinfo("Sukses", "Memo berhasil diurutkan berdasarkan title.")
    
    def sort_by_tanggal(self):
        """Mengurutkan memo berdasarkan tanggal."""
        if not self.current_memobook:
            messagebox.showwarning("Peringatan", "Pilih memobook terlebih dahulu.")
            return
        
        self.current_memobook.sort_memos_by_tanggal()
        self.refresh_memos_list()
        self.save_data_ke_json()
        messagebox.showinfo("Sukses", "Memo berhasil diurutkan berdasarkan tanggal.")
    
    def search_memo(self):
        """Mencari memo berdasarkan title."""
        if not self.current_memobook:
            messagebox.showwarning("Peringatan", "Pilih memobook terlebih dahulu.")
            return
        
        title = simpledialog.askstring("Cari Memo", "Masukkan title memo yang dicari:")
        if title:
            node = self.current_memobook.notes_list.find_node_by_title(title)
            if node:
                # Select the memo in treeview
                for item in self.memos_tree.get_children():
                    if self.memos_tree.item(item)['values'][0] == node.data.title:
                        self.memos_tree.selection_set(item)
                        self.memos_tree.focus(item)
                        self.display_memo(node.data)
                        break
                messagebox.showinfo("Ditemukan", f"Memo '{title}' ditemukan dan dipilih.")
            else:
                messagebox.showinfo("Tidak Ditemukan", f"Memo '{title}' tidak ditemukan.")
    
    def export_memos(self):
        """Mengekspor memo ke file TXT."""
        if not self.current_memobook:
            messagebox.showwarning("Peringatan", "Pilih memobook terlebih dahulu.")
            return
        
        try:
            self.current_memobook.export_notes_to_txt()
            messagebox.showinfo("Sukses", "Memo berhasil diekspor ke file TXT.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengekspor memo: {str(e)}")
    
    def save_data_ke_json(self):
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
                for name_key, notebook_data_dict in loaded_data.items():
                    self.memobooks[name_key] = Memobook.from_dict(notebook_data_dict)
        except FileNotFoundError:
            self.memobooks = {}
        except json.JSONDecodeError:
            self.memobooks = {}
            messagebox.showerror("Error", "File data memiliki format JSON yang tidak valid.")
        except Exception as e:
            self.memobooks = {}
            messagebox.showerror("Error", f"Terjadi kesalahan saat memuat data: {str(e)}")

class MemoDialog:
    def __init__(self, parent, title, memo_title="", memo_content=""):
        self.result = None
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("600x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Create widgets
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # title
        ttk.Label(main_frame, text="title:").pack(anchor=tk.W)
        self.title_entry = ttk.Entry(main_frame, width=60)
        self.title_entry.pack(fill=tk.X, pady=(0, 10))
        self.title_entry.insert(0, memo_title)
        
        # Content
        ttk.Label(main_frame, text="Konten:").pack(anchor=tk.W)
        self.content_text = scrolledtext.ScrolledText(main_frame, width=60, height=15, wrap=tk.WORD)
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.content_text.insert(1.0, memo_content)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Simpan", command=self.save).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Batal", command=self.cancel).pack(side=tk.RIGHT)
        
        # Focus on title entry
        self.title_entry.focus()
        
        # Bind Enter key to save
        self.dialog.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def save(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get(1.0, tk.END).strip()
        
        if not title:
            messagebox.showerror("Error", "title tidak boleh kosong.")
            return
        
        if not content:
            messagebox.showerror("Error", "Konten tidak boleh kosong.")
            return
        
        self.result = (title, content)
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()

def main():
    root = tk.Tk()
    app = MemobookGUI(root)
    
    # Handle window close
    def on_closing():
        app.save_data_ke_json()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
