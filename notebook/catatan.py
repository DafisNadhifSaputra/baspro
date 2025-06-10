from datetime import datetime

class Note:
    """Mewakili satu catatan dengan title, konten, dan tanggal pembuatan."""
    def __init__(self, title, content, created_tanggal=None):
        # Inisialisasi objek Note dengan title, konten, dan tanggal pembuatan.
        self.title = title  # title catatan
        self.content = content  # Isi atau konten catatan
        
        # Jika tanggal pembuatan (created_tanggal) disediakan, gunakan itu.
        # Jika tidak, catat waktu saat ini sebagai tanggal pembuatan.
        if created_tanggal:
            self.created_tanggal = created_tanggal
        else:
            # Format tanggal dan waktu: YYYY-MM-DD HH:MM:SS
            self.created_tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        # Representasi string dari objek Note, berguna untuk pencetakan.
        return f"title: {self.title}\nTanggal: {self.created_tanggal}\nKonten:\n{self.content}\n"

    def update_content(self, new_content):
        # Memperbarui konten catatan.
        self.content = new_content
        # Bisa ditambahkan logika untuk memperbarui tanggal modifikasi jika perlu

    def update_title(self, new_title):
        # Memperbarui title catatan.
        self.title = new_title
        # Bisa ditambahkan logika untuk memperbarui tanggal modifikasi jika perlu

    def to_dict(self):
        # Mengkonversi objek Note menjadi dictionary.
        # Berguna untuk menyimpan data Note ke format JSON.
        return {
            "title": self.title,
            "content": self.content,
            "created_tanggal": self.created_tanggal
        }

    @staticmethod
    def from_dict(data):
        """Membuat objek Note dari dictionary (data dari JSON).
        Ini adalah static method karena pembuatannya tidak bergantung pada instance Note tertentu.
        """
        # Mengambil 'created_tanggal' dari dictionary, default ke None jika tidak ada.
        created_tanggal = data.get("created_tanggal", None)
        # Membuat dan mengembalikan instance Note baru.
        return Note(data["title"], data["content"], created_tanggal)