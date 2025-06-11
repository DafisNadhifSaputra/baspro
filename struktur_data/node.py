class Node:
    """Node untuk Singly Linked List, menyimpan objek Memo."""
    def __init__(self, memo_data):
        # Menyimpan data memo yang diberikan
        self.data = memo_data
        # Pointer ke node berikutnya, awalnya None (tidak ada node berikutnya)
        self.next = None