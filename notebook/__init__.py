# Mengimpor kelas Note dari modul catatan.py dalam paket yang sama
from .catatan import Note

# Mengimpor kelas Notebook dari modul buku_catatan.py dalam paket yang sama
from .buku_catatan import Notebook

# Mendefinisikan modul publik yang akan diimpor ketika menggunakan 'from notebook import *'
__all__ = ['Note', 'Notebook']