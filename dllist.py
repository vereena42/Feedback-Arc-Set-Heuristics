class Node:
    def __init__(self, data):
        self.item = data
        self.nref = None
        self.pref = None

class DoublyLinkedList:

    def __init__(self, data_list=None):
        if data_list is None:
            self.start_node = None
        else:
            prev_node = None
            for node in data_list:
                if prev_node is None:
                    self.start_node = node
                else:
                    prev_node.nref = node
                    node.pref = prev_node
                prev_node = node

    def insert(self, data):
        if self.start_node is None:
            self.start_node = data
            self.start_node.pref = None
            self.start_node.nref = None
        else:
            data.nref = self.start_node
            data.pref = None
            self.start_node.pref = data
            self.start_node = data

    def insert_after(self, data, prev):
        if prev is None:
            data.pref = None
            data.nref = self.start_node
            if self.start_node is not None:
                self.start_node.pref = data
            self.start_node = data
        else:
            data.pref = prev
            data.nref = prev.nref
            prev.nref = data
            if data.nref is not None:
                data.nref.pref = data

    def delete(self, data):
        p = data.pref
        if p != None:
            p = p.item
        q = data.nref
        if q != None:
            q = q.item
        if self.start_node is data:
            self.start_node = data.nref
            if self.start_node != None:
                self.start_node.pref = None
        elif data.nref is None:
            data.pref.nref = None
        else:
            data.pref.nref = data.nref
            data.nref.pref = data.pref
    
    def to_list(self):
        result = []
        node = self.start_node
        while node is not None:
            result.append(node.item)
            node = node.nref
        return result
