from .node import Node

class SinglyLinkedList:
    """Implementasi Singly Linked List kustom untuk menyimpan data."""
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def appends(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def display(self):
        if self.is_empty():
            print("Tidak ada data.")
            return
        current = self.head
        count = 1
        while current:
            print(f"--- Data {count} ---")
            print(current.data)
            current = current.next
            count += 1

    def cari_node_by_judul(self, judul):
        current = self.head
        while current:
            if current.data.judul.lower() == judul.lower():
                return current
            current = current.next
        return None

    def delete_node_by_judul(self, judul):
        if self.is_empty():
            print("List kosong, tidak ada yang bisa dihapus.")
            return False
        if self.head.data.judul.lower() == judul.lower():
            self.head = self.head.next
            print(f"Data '{judul}' berhasil dihapus.")
            return True
        current = self.head
        prev = None
        while current and current.data.judul.lower() != judul.lower():
            prev = current
            current = current.next
        if current is None:
            print(f"Data '{judul}' tidak ditemukan.")
            return False
        prev.next = current.next
        print(f"Data '{judul}' berhasil dihapus.")
        return True

    def get_length(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def insertion_sort_by_judul(self):
        if self.is_empty() or self.head.next is None:
            return
        sorted_list_head = None
        current = self.head
        while current:
            next_node_to_process = current.next
            if sorted_list_head is None or \
               current.data.judul.lower() <= sorted_list_head.data.judul.lower():
                current.next = sorted_list_head
                sorted_list_head = current
            else:
                search_ptr = sorted_list_head
                while search_ptr.next is not None and \
                      search_ptr.next.data.judul.lower() < current.data.judul.lower():
                    search_ptr = search_ptr.next
                current.next = search_ptr.next
                search_ptr.next = current
            current = next_node_to_process
        self.head = sorted_list_head
        print("Data telah diurutkan berdasarkan judul menggunakan Insertion Sort.")

    def linear_search_by_judul(self, judul_to_search):
        current = self.head
        position = 0
        while current:
            if current.data.judul.lower() == judul_to_search.lower():
                print(f"Data '{judul_to_search}' ditemukan pada posisi {position + 1}.")
                print(current.data)
                return current.data
            current = current.next
            position += 1
        print(f"Data '{judul_to_search}' tidak ditemukan.")
        return None

    def to_list_of_dicts(self):
        if self.is_empty():
            return []
        
        # Hitung jumlah node terlebih dahulu
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

    def load_from_list_of_dicts(self, list_of_dicts):
        self.head = None
        for data_dict in list_of_dicts:
            # Import dinamis untuk menghindari circular import
            from memobook.memo import Memo
            data_obj = Memo.from_dict(data_dict)
            self.appends(data_obj)

    def insertion_sort_by_tanggal(self):
        """Mengurutkan data berdasarkan tanggal menggunakan Insertion Sort."""
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
        print("Data telah diurutkan berdasarkan tanggal menggunakan Insertion Sort.")