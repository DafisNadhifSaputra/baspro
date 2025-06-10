from datetime import datetime

class Note:
    """Mewakili satu catatan dengan judul, konten, dan tanggal pembuatan."""
    def __init__(self, judul, content, created_tanggal=None):
        # Inisialisasi objek Note dengan judul, konten, dan tanggal pembuatan.
        self.judul = judul  # Judul catatan
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
        return f"Judul: {self.judul}\nTanggal: {self.created_tanggal}\nKonten:\n{self.content}\n"

    def update_content(self, new_content):
        # Memperbarui konten catatan.
        self.content = new_content
        # Bisa ditambahkan logika untuk memperbarui tanggal modifikasi jika perlu

    def update_judul(self, new_judul):
        # Memperbarui judul catatan.
        self.judul = new_judul
        # Bisa ditambahkan logika untuk memperbarui tanggal modifikasi jika perlu

    def to_dict(self):
        # Mengkonversi objek Note menjadi dictionary.
        # Berguna untuk menyimpan data Note ke format JSON.
        return {
            "judul": self.judul,
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
        return Note(data["judul"], data["content"], created_tanggal)