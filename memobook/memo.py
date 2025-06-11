from datetime import datetime

class Memo:
    """Mewakili satu memo dengan judul, konten, dan tanggal pembuatan."""
    def __init__(self, judul, content, created_tanggal=None):
        # Inisialisasi objek Memo dengan judul, konten, dan tanggal pembuatan.
        self.judul = judul  # Judul memo
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
        return f"Judul: {self.judul}\nTanggal: {self.created_tanggal}\nKonten:\n{self.content}\n"

    def update_content(self, new_content):
        # Memperbarui konten memo.
        self.content = new_content
        # Bisa ditambahkan logika untuk memperbarui tanggal modifikasi jika perlu

    def update_judul(self, new_judul):
        # Memperbarui judul memo.
        self.judul = new_judul
        # Bisa ditambahkan logika untuk memperbarui tanggal modifikasi jika perlu

    def to_dict(self):
        # Mengkonversi objek Memo menjadi dictionary.
        # Berguna untuk menyimpan data Memo ke format JSON.
        return {
            "judul": self.judul,
            "content": self.content,
            "created_tanggal": self.created_tanggal
        }

    @staticmethod
    def from_dict(data):
        """Membuat objek Memo dari dictionary (data dari JSON)."""
        # Mengambil 'created_tanggal' dari dictionary, default ke None jika tidak ada.
        created_tanggal = data.get("created_tanggal", None)
        # Membuat dan mengembalikan instance Memo baru.
        return Memo(data["judul"], data["content"], created_tanggal)