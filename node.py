class Node:

    def __init__(self, val=None, prev_h=None, next_h=None, prev_v=None, next_v=None, isColHeader=False, isOrigin=False):
        self.isColHeader = isColHeader
        self.isOrigin = isOrigin
        self.val = val
        self.prev_h = prev_h
        self.prev_v = prev_v
        self.next_h = next_h
        self.next_v = next_v
        self.adjac_h = [prev_h, next_h]
        self.adjac_v = [prev_v, next_v]

    def __iter__(self):
        self.prev = self
        return self

    def __next__(self):
        self.prev = self.prev.next_h
        return self.prev
