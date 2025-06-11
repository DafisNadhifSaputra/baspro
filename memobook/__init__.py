# Mengimpor kelas Memo dari modul memo.py dalam paket yang sama
from .memo import Memo

# Mengimpor kelas Memobook dari modul buku_memo.py dalam paket yang sama
from .buku_memo import Memobook

# Mendefinisikan modul publik yang akan diimpor ketika menggunakan 'from memobook import *'
__all__ = ['Memo', 'Memobook']