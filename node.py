class Node:

    def __init__(self, val, prev_h=None, next_h=None, prev_v=None, next_v=None):
        self.val = val
        self.prev_h = prev_h
        self.prev_v = prev_v
        self.next_h = next_h
        self.next_v = next_v
        self.adjac_h = [prev_h, next_h]
        self.adjac_v = [prev_v, next_v]
