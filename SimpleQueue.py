# Array implementation of Queue
class Queue:
    # Initialize the queue with a default capacity of 10 and size of 0 with front and back pointers
    def __init__(self, cap=10):
        self.cap = cap
        self.size = 0
        self.front = 0
        self.back = 0
        self.list = [None] * cap

    """
    Return the capacity of the queue
    Runtime: O(1)
    """

    def capacity(self):
        return self.cap

    """
    Add data onto the back of the queue. If the queue is full, call grow() to resize the queue
    Runtime: O(1) if the queue is not full, O(n) if the queue is full and resizing is needed
    """

    def enqueue(self, data):
        if self.size == self.cap:
            self.grow()

        self.list[self.back] = data
        self.back = (self.back + 1) % self.cap
        self.size += 1

    """
    Dequeue data from the front of the queue. If the queue is empty, raise an IndexError

    Return: the removed element of the queue

    Runtime: O(1)
    """

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue() used on empty queue")

        temp = self.get_front()
        self.front = (self.front + 1) % self.cap
        self.size -= 1
        return temp

    """
    Return the front element of the queue
    Runtime: O(1)
    """

    def get_front(self):
        return self.list[self.front]

    """
    Check if the queue is empty
    Runtime: O(1)
    """

    def is_empty(self):
        return self.size == 0

    """
    Return the size of the queue
    Runtime: O(1)
    """

    def __len__(self):
        return self.size

    """Resize function that resizes the queue by 2X. 
    Create a new list thats double the size and copy the elements over but wraps around the queue when going out of bounds
    Runtime: O(n) where n is the size of the queue
    """

    def grow(self):
        self.cap *= 2
        j = self.front
        temp = [None] * self.cap

        for i in range(self.size):
            temp[i] = self.list[j]
            j = (j + 1) % self.size

        self.front = 0
        self.back = self.size
        self.list = temp
