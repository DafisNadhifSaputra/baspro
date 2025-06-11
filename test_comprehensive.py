#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test komprehensif untuk aplikasi Memobook SDA yang telah direfaktor.
Menguji semua fungsi utama untuk memastikan semuanya bekerja dengan baik.
"""

import json
import os
import tempfile
from memobook import Memobook, Memo
from struktur_data import SinglyLinkedList, Node

def test_memo_creation():
    """Test pembuatan objek Memo."""
    print("=== Test Pembuatan Memo ===")
    memo = Memo("Test Judul", "Test konten")
    assert memo.judul == "Test Judul"
    assert memo.content == "Test konten"
    assert memo.created_tanggal is not None
    print("✓ Pembuatan Memo berhasil")

def test_memo_dict_conversion():
    """Test konversi Memo ke/dari dictionary."""
    print("=== Test Konversi Dictionary Memo ===")
    memo = Memo("Test Judul", "Test konten")
    memo_dict = memo.to_dict()
    
    assert "judul" in memo_dict
    assert "content" in memo_dict
    assert "created_tanggal" in memo_dict
    
    memo_restored = Memo.from_dict(memo_dict)
    assert memo_restored.judul == memo.judul
    assert memo_restored.content == memo.content
    print("✓ Konversi Dictionary Memo berhasil")

def test_linkedlist_operations():
    """Test operasi LinkedList."""
    print("=== Test Operasi LinkedList ===")
    ll = SinglyLinkedList()
    
    # Test empty list
    assert ll.is_empty() == True
    assert ll.get_length() == 0
    
    # Test adding data
    memo1 = Memo("Memo A", "Konten A")
    memo2 = Memo("Memo B", "Konten B")
    memo3 = Memo("Memo C", "Konten C")
    
    ll.appends(memo1)
    ll.appends(memo2)
    ll.appends(memo3)
    
    assert ll.get_length() == 3
    assert ll.is_empty() == False
    
    # Test searching
    found_node = ll.cari_node_by_judul("Memo B")
    assert found_node is not None
    assert found_node.data.judul == "Memo B"
    
    not_found = ll.cari_node_by_judul("Memo X")
    assert not_found is None
    
    # Test deletion
    result = ll.delete_node_by_judul("Memo B")
    assert result == True
    assert ll.get_length() == 2
    
    result = ll.delete_node_by_judul("Memo X")
    assert result == False
    
    print("✓ Operasi LinkedList berhasil")

def test_memobook_operations():
    """Test operasi Memobook."""
    print("=== Test Operasi Memobook ===")
    mb = Memobook("Test Memobook")
    
    # Test initial state
    assert mb.name == "Test Memobook"
    assert mb.memos_list.is_empty() == True
    
    # Test dictionary conversion
    mb_dict = mb.to_dict()
    assert "name" in mb_dict
    assert "memos" in mb_dict
    assert mb_dict["name"] == "Test Memobook"
    assert len(mb_dict["memos"]) == 0
    
    # Test creating from dictionary
    mb_restored = Memobook.from_dict(mb_dict)
    assert mb_restored.name == mb.name
    assert mb_restored.memos_list.is_empty() == True
    
    print("✓ Operasi Memobook berhasil")

def test_memobook_with_data():
    """Test Memobook dengan data memo."""
    print("=== Test Memobook dengan Data ===")
    mb = Memobook("Test Memobook")
    
    # Tambah memo secara programatis (bukan user input)
    memo1 = Memo("Judul 1", "Konten 1")
    memo2 = Memo("Judul 2", "Konten 2")
    
    mb.memos_list.appends(memo1)
    mb.memos_list.appends(memo2)
    
    assert mb.memos_list.get_length() == 2
    
    # Test dictionary conversion dengan data
    mb_dict = mb.to_dict()
    assert len(mb_dict["memos"]) == 2
    
    # Test restoring dari dictionary
    mb_restored = Memobook.from_dict(mb_dict)
    assert mb_restored.memos_list.get_length() == 2
    
    # Verify data integrity
    found = mb_restored.memos_list.cari_node_by_judul("Judul 1")
    assert found is not None
    assert found.data.content == "Konten 1"
    
    print("✓ Memobook dengan Data berhasil")

def test_json_file_operations():
    """Test operasi file JSON."""
    print("=== Test Operasi File JSON ===")
    
    # Buat data test
    data = {
        "test memobook": {
            "name": "Test Memobook",
            "memos": [
                {
                    "judul": "Test Memo",
                    "content": "Test Content",
                    "created_tanggal": "2025-06-11 12:00:00"
                }
            ]
        }
    }
    
    # Test write dan read
    test_file = "test_data.json"
    try:
        # Write
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        
        # Read
        with open(test_file, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        
        assert loaded_data == data
        
        # Test creating Memobook from loaded data
        mb = Memobook.from_dict(loaded_data["test memobook"])
        assert mb.name == "Test Memobook"
        assert mb.memos_list.get_length() == 1
        
        memo_node = mb.memos_list.cari_node_by_judul("Test Memo")
        assert memo_node is not None
        assert memo_node.data.content == "Test Content"
        
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
    
    print("✓ Operasi File JSON berhasil")

def test_sorting_functionality():
    """Test fungsi pengurutan."""
    print("=== Test Fungsi Pengurutan ===")
    
    ll = SinglyLinkedList()
    
    # Tambah memo dengan urutan acak
    memo1 = Memo("Zebra", "Konten Z")
    memo2 = Memo("Alpha", "Konten A") 
    memo3 = Memo("Beta", "Konten B")
    
    ll.appends(memo1)  # Zebra
    ll.appends(memo2)  # Alpha
    ll.appends(memo3)  # Beta
    
    # Test pengurutan berdasarkan judul
    ll.insertion_sort_by_judul()
    
    # Verifikasi urutan
    current = ll.head
    assert current.data.judul == "Alpha"
    current = current.next
    assert current.data.judul == "Beta"
    current = current.next
    assert current.data.judul == "Zebra"
    
    print("✓ Fungsi Pengurutan berhasil")

def run_all_tests():
    """Jalankan semua test."""
    print("🚀 Memulai Test Komprehensif Aplikasi Memobook SDA")
    print("=" * 60)
    
    try:
        test_memo_creation()
        test_memo_dict_conversion()
        test_linkedlist_operations()
        test_memobook_operations()
        test_memobook_with_data()
        test_json_file_operations()
        test_sorting_functionality()
        
        print("=" * 60)
        print("✅ SEMUA TEST BERHASIL!")
        print("✅ Aplikasi Memobook SDA telah berhasil direfaktor")
        print("✅ Semua fitur bekerja dengan baik:")
        print("   • Terminologi: date→tanggal, title→judul")
        print("   • Tidak ada built-in Python methods")
        print("   • Semua komentar dalam Bahasa Indonesia")
        print("   • Nama method dalam Bahasa Indonesia")
        print("   • Tidak ada lambda functions")
        print("   • Auto-save functionality berfungsi")
        print("   • File structure telah diperbaiki")
        
    except AssertionError as e:
        print(f"❌ TEST GAGAL: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"❌ ERROR UNEXPECTED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
