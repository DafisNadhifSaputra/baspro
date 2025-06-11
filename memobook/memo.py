from datetime import datetime

class Memo:
    """Mewakili satu memo dengan title, konten, dan tanggal pembuatan."""
    def __init__(self, title, content, created_tanggal=None):
        # Inisialisasi objek Memo dengan title, konten, dan tanggal pembuatan.
        self.title = title  # title memo
        self.content = content  # Isi atau konten memo
        
        # Jika tanggal pembuatan (created_tanggal) disediakan, gunakan itu.
        # Jika tidak, catat waktu saat ini sebagai tanggal pembuatan.
        if created_tanggal:
            self.created_tanggal = created_tanggal
        else:
            # Format tanggal dan waktu: YYYY-MM-DD HH:MM:SS
            self.created_tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        # Representasi string dari objek Memo, berguna untuk pencetakan.
        return f"title: {self.title}\nTanggal: {self.created_tanggal}\nKonten:\n{self.content}\n"

    def update_content(self, new_content):
        # Memperbarui konten memo.
        self.content = new_content
        # Bisa ditambahkan logika untuk memperbarui tanggal modifikasi jika perlu

    def update_title(self, new_title):
        # Memperbarui title memo.
        self.title = new_title
        # Bisa ditambahkan logika untuk memperbarui tanggal modifikasi jika perlu

    def to_dict(self):
        # Mengkonversi objek Memo menjadi dictionary.
        # Berguna untuk menyimpan data Memo ke format JSON.
        return {
            "title": self.title,
            "content": self.content,
            "created_tanggal": self.created_tanggal
        }

    @staticmethod
    def from_dict(data):
        """Membuat objek Memo dari dictionary (data dari JSON)."""
        # Mengambil 'created_tanggal' dari dictionary, default ke None jika tidak ada.
        created_tanggal = data.get("created_tanggal", None)
        # Membuat dan mengembalikan instance Memo baru.
        return Memo(data["title"], data["content"], created_tanggal)