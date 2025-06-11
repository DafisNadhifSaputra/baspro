from .node import Node
from memobook import Memo

class SinglyLinkedList:
    """Implementasi Singly Linked List kustom untuk menyimpan Memo."""
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def appends(self, memo_data):
        new_node = Node(memo_data)
        if self.is_empty():
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def display(self):
        if self.is_empty():
            print("Tidak ada memo.")
            return
        current = self.head
        count = 1
        while current:
            print(f"--- Memo {count} ---")
            print(current.data)
            current = current.next
            count += 1

    def find_node_by_title(self, title):
        current = self.head
        while current:
            if current.data.title.lower() == title.lower():
                return current
            current = current.next
        return None

    def delete_node_by_title(self, title):
        if self.is_empty():
            print("List kosong, tidak ada yang bisa dihapus.")
            return False
        if self.head.data.title.lower() == title.lower():
            self.head = self.head.next
            print(f"Memo '{title}' berhasil dihapus.")
            return True
        current = self.head
        prev = None
        while current and current.data.title.lower() != title.lower():
            prev = current
            current = current.next
        if current is None:
            print(f"Memo '{title}' tidak ditemukan.")
            return False
        prev.next = current.next
        print(f"Memo '{title}' berhasil dihapus.")
        return True

    def get_length(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def insertion_sort_by_title(self):
        if self.is_empty() or self.head.next is None:
            return
        sorted_list_head = None
        current = self.head
        while current:
            next_node_to_process = current.next
            if sorted_list_head is None or current.data.title.lower() <= sorted_list_head.data.title.lower():
                current.next = sorted_list_head
                sorted_list_head = current
            else:
                search_ptr = sorted_list_head
                while search_ptr.next is not None and search_ptr.next.data.title.lower() < current.data.title.lower():
                    search_ptr = search_ptr.next
                current.next = search_ptr.next
                search_ptr.next = current
            current = next_node_to_process
        self.head = sorted_list_head
        print("Memo telah diurutkan berdasarkan title menggunakan Insertion Sort.")

    def linear_search_by_title(self, title_to_search):
        current = self.head
        position = 0
        while current:
            if current.data.title.lower() == title_to_search.lower():
                print(f"Memo '{title_to_search}' ditemukan pada posisi {position + 1}.")
                print(current.data)
                return current.data
            current = current.next
            position += 1
        print(f"Memo '{title_to_search}' tidak ditemukan.")
        return None

    def to_list_of_dicts(self):
        if self.is_empty():
            return []
        
        # Hitung jumlah node
        count = self.get_length()
        
        # Buat array dengan ukuran yang tepat
        result = [None] * count
        current = self.head
        index = 0
        
        while current and index < count:
            result[index] = current.data.to_dict()
            current = current.next
            index += 1
            
        return result

    def load_from_list_of_dicts(self, list_of_memo_dicts):
        self.head = None
        for memo_dict in list_of_memo_dicts:
            memo_obj = Memo.from_dict(memo_dict) # Memanggil staticmethod
            self.appends(memo_obj)

    def insertion_sort_by_date(self):
        """Mengurutkan memo berdasarkan tanggal menggunakan Insertion Sort."""
        if self.is_empty() or self.head.next is None:
            return
        
        sorted_list_head = None
        current = self.head
        
        while current:
            next_node_to_process = current.next
            
            if sorted_list_head is None or \
               current.data.created_tanggal <= sorted_list_head.data.created_tanggal:
                current.next = sorted_list_head
                sorted_list_head = current
            else:
                search_ptr = sorted_list_head
                while search_ptr.next is not None and \
                      search_ptr.next.data.created_tanggal < current.data.created_tanggal:
                    search_ptr = search_ptr.next
                current.next = search_ptr.next
                search_ptr.next = current
            
            current = next_node_to_process
        
        self.head = sorted_list_head
        print("Memo telah diurutkan berdasarkan tanggal menggunakan Insertion Sort.")