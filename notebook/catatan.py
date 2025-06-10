from datetime import datetime

class Note:
    """Mewakili satu catatan."""
    def __init__(self, judul, content, created_date=None):
        # Inisialisasi objek Note dengan judul, konten, dan tanggal pembuatan.
        self.judul = judul  # Judul catatan
        self.content = content  # Isi atau konten catatan
        
        # Jika tanggal pembuatan (created_date) disediakan, gunakan itu.
        # Jika tidak, gunakan tanggal dan waktu saat ini sebagai default.
        if created_date:
            self.created_date = created_date
        else:
            # Format tanggal menjadi YYYY-MM-DD HH:MM:SS
            self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        # Mengembalikan representasi string dari objek Note, cocok untuk dicetak.
        return f"Judul: {self.judul}\nTanggal: {self.created_date}\nKonten:\n{self.content}\n"

    def update_content(self, new_content):
        # Memperbarui konten catatan dengan konten baru.
        self.content = new_content

    def update_judul(self, new_judul):
        # Memperbarui judul catatan dengan judul baru.
        self.judul = new_judul

    def to_dict(self):
        """Mengkonversi objek Note menjadi dictionary.
        Berguna untuk serialisasi data, misalnya saat menyimpan ke file JSON.
        """
        return {
            "judul": self.judul, 
            "content": self.content,
            "created_date": self.created_date
        }

    @staticmethod
    def from_dict(data):
        """Membuat objek Note dari dictionary.
        Ini adalah static method karena tidak bergantung pada instance Note tertentu untuk pembuatannya.
        """
        # Mengambil 'created_date' dari dictionary, default ke None jika tidak ada.
        created_date = data.get("created_date", None)
        # Membuat dan mengembalikan instance Note baru menggunakan data dari dictionary.
        return Note(data["judul"], data["content"], created_date)