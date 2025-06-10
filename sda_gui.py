import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import json
from notebook import Notebook
from struktur_data import SinglyLinkedList, Node

class NotebookGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Notebook SDA - GUI Version")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Data
        self.notebooks = {}
        self.data_file = "notebook_data.json"
        self.current_notebook = None
        
        # Load data
        self.load_data_dari_json()
        if not self.notebooks:
            self._inisialisasi_default_notebooks()
        
        # Create GUI
        self.create_widgets()
        self.refresh_notebook_list()
    
    def _inisialisasi_default_notebooks(self):
        """Inisialisasi notebook default jika belum ada."""
        default_subjects = ["Aljabar Abstrak", "Persamaan Diferensial", "Analisis Real", "Struktur Data dan Algoritma"]
        for subject in default_subjects:
            if subject.lower() not in self.notebooks:
                self.notebooks[subject.lower()] = Notebook(subject)
        self.save_data_ke_json()
    
    def create_widgets(self):
        """Membuat semua widget GUI."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # title
        title_label = ttk.Label(main_frame, text="Aplikasi Notebook SDA", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Left panel - Notebook list
        left_frame = ttk.LabelFrame(main_frame, text="Daftar Notebook", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Notebook listbox
        self.notebook_listbox = tk.Listbox(left_frame, height=15, width=25)
        self.notebook_listbox.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.notebook_listbox.bind('<<ListboxSelect>>', self.on_notebook_select)
        
        # Notebook buttons
        ttk.Button(left_frame, text="Tambah Notebook", 
                  command=self.add_notebook).grid(row=1, column=0, pady=(10, 5), sticky=tk.W+tk.E)
        ttk.Button(left_frame, text="Hapus Notebook", 
                  command=self.delete_notebook).grid(row=1, column=1, pady=(10, 5), sticky=tk.W+tk.E)
        
        # Middle panel - Notes list
        middle_frame = ttk.LabelFrame(main_frame, text="Daftar Catatan", padding="10")
        middle_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Notes treeview
        self.notes_tree = ttk.Treeview(middle_frame, columns=('title', 'tanggal'), 
                                      show='headings', height=15)
        self.notes_tree.heading('title', text='title')
        self.notes_tree.heading('tanggal', text='Tanggal')
        self.notes_tree.column('title', width=200)
        self.notes_tree.column('tanggal', width=150)
        self.notes_tree.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.notes_tree.bind('<<TreeviewSelect>>', self.on_note_select)
        
        # Notes buttons
        notes_button_frame = ttk.Frame(middle_frame)
        notes_button_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0), sticky=tk.W+tk.E)
        
        ttk.Button(notes_button_frame, text="Tambah Catatan", 
                  command=self.add_note).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(notes_button_frame, text="Edit Catatan", 
                  command=self.edit_note).pack(side=tk.LEFT, padx=5)
        ttk.Button(notes_button_frame, text="Hapus Catatan", 
                  command=self.delete_note).pack(side=tk.LEFT, padx=5)
        
        # Sort buttons
        sort_frame = ttk.Frame(middle_frame)
        sort_frame.grid(row=2, column=0, columnspan=3, pady=(5, 0), sticky=tk.W+tk.E)
        
        ttk.Button(sort_frame, text="Urutkan: title", 
                  command=self.sort_by_title).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(sort_frame, text="Urutkan: Tanggal", 
                  command=self.sort_by_tanggal).pack(side=tk.LEFT, padx=5)
        ttk.Button(sort_frame, text="Cari Catatan", 
                  command=self.search_note).pack(side=tk.LEFT, padx=5)
        ttk.Button(sort_frame, text="Ekspor ke TXT", 
                  command=self.export_notes).pack(side=tk.LEFT, padx=5)
        
        # Right panel - Note content
        right_frame = ttk.LabelFrame(main_frame, text="Isi Catatan", padding="10")
        right_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Note title
        self.note_title_var = tk.StringVar()
        ttk.Label(right_frame, text="title:").grid(row=0, column=0, sticky=tk.W)
        title_entry = ttk.Entry(right_frame, textvariable=self.note_title_var, 
                               state='readonly', width=40)
        title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Note tanggal
        self.note_tanggal_var = tk.StringVar()
        ttk.Label(right_frame, text="Tanggal:").grid(row=1, column=0, sticky=tk.W)
        tanggal_entry = ttk.Entry(right_frame, textvariable=self.note_tanggal_var, 
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
    
    def refresh_notebook_list(self):
        """Memperbarui daftar notebook di listbox."""
        self.notebook_listbox.delete(0, tk.END)
        for notebook in self.notebooks.values():
            self.notebook_listbox.insert(tk.END, notebook.name)
    
    def refresh_notes_list(self):
        """Memperbarui daftar catatan di treeview."""
        # Clear existing items
        for item in self.notes_tree.get_children():
            self.notes_tree.delete(item)
        
        if not self.current_notebook or self.current_notebook.notes_list.is_empty():
            return
        
        # Add notes to treeview
        current = self.current_notebook.notes_list.head
        while current:
            note = current.data
            self.notes_tree.insert('', tk.END, values=(note.title, note.created_tanggal))
            current = current.next
    
    def on_notebook_select(self, event):
        """Handler ketika notebook dipilih."""
        selection = self.notebook_listbox.curselection()
        if selection:
            notebook_name = self.notebook_listbox.get(selection[0])
            # Find notebook by name
            for notebook in self.notebooks.values():
                if notebook.name == notebook_name:
                    self.current_notebook = notebook
                    break
            self.refresh_notes_list()
            self.clear_note_display()
    
    def on_note_select(self, event):
        """Handler ketika catatan dipilih."""
        selection = self.notes_tree.selection()
        if selection and self.current_notebook:
            item = self.notes_tree.item(selection[0])
            note_title = item['values'][0]
            
            # Find the note
            current = self.current_notebook.notes_list.head
            while current:
                if current.data.title == note_title:
                    self.display_note(current.data)
                    break
                current = current.next
    
    def display_note(self, note):
        """Menampilkan isi catatan di panel kanan."""
        self.note_title_var.set(note.title)
        self.note_tanggal_var.set(note.created_tanggal)
        
        self.note_content.config(state='normal')
        self.note_content.delete(1.0, tk.END)
        self.note_content.insert(1.0, note.content)
        self.note_content.config(state='disabled')
    
    def clear_note_display(self):
        """Membersihkan tampilan catatan."""
        self.note_title_var.set("")
        self.note_tanggal_var.set("")
        self.note_content.config(state='normal')
        self.note_content.delete(1.0, tk.END)
        self.note_content.config(state='disabled')
    
    def add_notebook(self):
        """Menambah notebook baru."""
        name = simpledialog.askstring("Tambah Notebook", "Masukkan nama notebook baru:")
        if name:
            if name.lower() in self.notebooks:
                messagebox.showerror("Error", "Notebook dengan nama tersebut sudah ada.")
            else:
                self.notebooks[name.lower()] = Notebook(name)
                self.refresh_notebook_list()
                self.save_data_ke_json()
                messagebox.showinfo("Sukses", f"Notebook '{name}' berhasil ditambahkan.")
    
    def delete_notebook(self):
        """Menghapus notebook yang dipilih."""
        selection = self.notebook_listbox.curselection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih notebook yang akan dihapus.")
            return
        
        notebook_name = self.notebook_listbox.get(selection[0])
        result = messagebox.askyesno("Konfirmasi", 
                                   f"Apakah Anda yakin ingin menghapus notebook '{notebook_name}'?")
        if result:
            # Find and delete notebook
            for key, notebook in list(self.notebooks.items()):
                if notebook.name == notebook_name:
                    del self.notebooks[key]
                    break
            
            self.current_notebook = None
            self.refresh_notebook_list()
            self.refresh_notes_list()
            self.clear_note_display()
            self.save_data_ke_json()
            messagebox.showinfo("Sukses", f"Notebook '{notebook_name}' berhasil dihapus.")
    
    def add_note(self):
        """Menambah catatan baru."""
        if not self.current_notebook:
            messagebox.showwarning("Peringatan", "Pilih notebook terlebih dahulu.")
            return
        
        dialog = NoteDialog(self.root, "Tambah Catatan Baru")
        if dialog.result:
            title, content = dialog.result
            
            # Check if title already exists
            if self.current_notebook.notes_list.find_node_by_title(title):
                messagebox.showerror("Error", "Catatan dengan title tersebut sudah ada.")
                return
            
            # Add note
            from notebook.catatan import Note
            new_note = Note(title, content)
            self.current_notebook.notes_list.appends(new_note)
            
            self.refresh_notes_list()
            self.save_data_ke_json()
            messagebox.showinfo("Sukses", f"Catatan '{title}' berhasil ditambahkan.")
    
    def edit_note(self):
        """Mengedit catatan yang dipilih."""
        selection = self.notes_tree.selection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih catatan yang akan diedit.")
            return
        
        item = self.notes_tree.item(selection[0])
        note_title = item['values'][0]
        
        # Find the note
        current = self.current_notebook.notes_list.head
        while current:
            if current.data.title == note_title:
                dialog = NoteDialog(self.root, "Edit Catatan", 
                                  current.data.title, current.data.content)
                if dialog.result:
                    new_title, new_content = dialog.result
                    
                    # Check if new title conflicts with existing notes
                    if new_title != current.data.title:
                        existing = self.current_notebook.notes_list.find_node_by_title(new_title)
                        if existing:
                            messagebox.showerror("Error", "title sudah digunakan oleh catatan lain.")
                            return
                    
                    # Update note
                    current.data.update_title(new_title)
                    current.data.update_content(new_content)
                    
                    self.refresh_notes_list()
                    self.save_data_ke_json()
                    messagebox.showinfo("Sukses", "Catatan berhasil diupdate.")
                break
            current = current.next
    
    def delete_note(self):
        """Menghapus catatan yang dipilih."""
        selection = self.notes_tree.selection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih catatan yang akan dihapus.")
            return
        
        item = self.notes_tree.item(selection[0])
        note_title = item['values'][0]
        
        result = messagebox.askyesno("Konfirmasi", 
                                   f"Apakah Anda yakin ingin menghapus catatan '{note_title}'?")
        if result:
            self.current_notebook.notes_list.delete_node_by_title(note_title)
            self.refresh_notes_list()
            self.clear_note_display()
            self.save_data_ke_json()
            messagebox.showinfo("Sukses", f"Catatan '{note_title}' berhasil dihapus.")
    
    def sort_by_title(self):
        """Mengurutkan catatan berdasarkan title."""
        if not self.current_notebook:
            messagebox.showwarning("Peringatan", "Pilih notebook terlebih dahulu.")
            return
        
        self.current_notebook.sort_notes()
        self.refresh_notes_list()
        self.save_data_ke_json()
        messagebox.showinfo("Sukses", "Catatan berhasil diurutkan berdasarkan title.")
    
    def sort_by_tanggal(self):
        """Mengurutkan catatan berdasarkan tanggal."""
        if not self.current_notebook:
            messagebox.showwarning("Peringatan", "Pilih notebook terlebih dahulu.")
            return
        
        self.current_notebook.sort_notes_by_tanggal()
        self.refresh_notes_list()
        self.save_data_ke_json()
        messagebox.showinfo("Sukses", "Catatan berhasil diurutkan berdasarkan tanggal.")
    
    def search_note(self):
        """Mencari catatan berdasarkan title."""
        if not self.current_notebook:
            messagebox.showwarning("Peringatan", "Pilih notebook terlebih dahulu.")
            return
        
        title = simpledialog.askstring("Cari Catatan", "Masukkan title catatan yang dicari:")
        if title:
            node = self.current_notebook.notes_list.find_node_by_title(title)
            if node:
                # Select the note in treeview
                for item in self.notes_tree.get_children():
                    if self.notes_tree.item(item)['values'][0] == node.data.title:
                        self.notes_tree.selection_set(item)
                        self.notes_tree.focus(item)
                        self.display_note(node.data)
                        break
                messagebox.showinfo("Ditemukan", f"Catatan '{title}' ditemukan dan dipilih.")
            else:
                messagebox.showinfo("Tidak Ditemukan", f"Catatan '{title}' tidak ditemukan.")
    
    def export_notes(self):
        """Mengekspor catatan ke file TXT."""
        if not self.current_notebook:
            messagebox.showwarning("Peringatan", "Pilih notebook terlebih dahulu.")
            return
        
        try:
            self.current_notebook.export_notes_to_txt()
            messagebox.showinfo("Sukses", "Catatan berhasil diekspor ke file TXT.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengekspor catatan: {str(e)}")
    
    def save_data_ke_json(self):
        """Menyimpan data ke file JSON."""
        data_to_save = {}
        for name_key, notebook_obj in self.notebooks.items():
            data_to_save[name_key] = notebook_obj.to_dict()
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
                self.notebooks = {}
                for name_key, notebook_data_dict in loaded_data.items():
                    self.notebooks[name_key] = Notebook.from_dict(notebook_data_dict)
        except FileNotFoundError:
            self.notebooks = {}
        except json.JSONDecodeError:
            self.notebooks = {}
            messagebox.showerror("Error", "File data memiliki format JSON yang tidak valid.")
        except Exception as e:
            self.notebooks = {}
            messagebox.showerror("Error", f"Terjadi kesalahan saat memuat data: {str(e)}")

class NoteDialog:
    def __init__(self, parent, title, note_title="", note_content=""):
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
        self.title_entry.insert(0, note_title)
        
        # Content
        ttk.Label(main_frame, text="Konten:").pack(anchor=tk.W)
        self.content_text = scrolledtext.ScrolledText(main_frame, width=60, height=15, wrap=tk.WORD)
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.content_text.insert(1.0, note_content)
        
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
    app = NotebookGUI(root)
    
    # Handle window close
    def on_closing():
        app.save_data_ke_json()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
