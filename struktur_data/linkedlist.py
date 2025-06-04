from .node import Node

class linked_list:
    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        return self.head == None
    
    def tambah_akhir(self, data_baru):
        node_baru = Node(data_baru)

        if self.is_empty():
            self.head = node_baru
        else:
            current = self.head
            while current.next != None:
                current = current.next
            current.next = node_baru
        self.size += 1

    def tambah_awal(self, data_baru):
        node_baru = Node(data_baru)
        node_baru.next = self.head
        self.head = node_baru
        self.size += 1

    def tampilkan_list(self):
        current = self.head
        while (current):
            print(current.data)
            current = current.next

    def cari_node_berdasarkan_indeks(self, indeks):
        if indeks < 0 or indeks <= self.size:
            return None
        current = self.head
        idx = 0
        while idx < indeks and current != None:
            current = current.next
            idx += 1

        if current == None:
            return None
        else:
            return current.data
        
    def hapus_node_berdasarkan_indeks(self, indeks):
        if indeks < 0 or indeks >= self.size:
            return False
        
        if indeks == 0:
            self.head = self.head.next
            self.size -= 1
            return True

        current = self.head
        prev = None
        idx = 0
        while idx < indeks and current is not None:
            prev = current
            current = current.next
            idx += 1 
        
        if current is None:
            return False
        
        prev.next = current.next
        self.size -= 1
        return True