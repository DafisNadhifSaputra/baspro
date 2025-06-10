class Node:
    """Node untuk Singly Linked List, menyimpan objek Note."""
    def __init__(self, note_data):
        # Menyimpan data catatan yang diberikan
        self.data = note_data
        # Pointer ke node berikutnya, awalnya None (tidak ada node berikutnya)
        self.next = None