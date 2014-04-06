# encoding=utf-8
'''Data structures.'''
import itertools


class LinkedListNode(object):
    '''A node in a :class:`LinkedList`.

    Attributes:
        value: Any value.
        head (LinkedListNode): The node in front.
        tail (LinkedListNode): The node in back.
    '''
    __slots__ = ('value', 'head', 'tail')

    def __init__(self, value, head=None, tail=None):
        self.value = value
        self.head = head
        self.tail = tail

    def link_head(self, node):
        '''Add a node to the head. '''
        assert not node.tail
        old_head = self.head

        if old_head:
            assert old_head.tail == self
            old_head.tail = node
            node.head = old_head

        node.tail = self
        self.head = node

    def link_tail(self, node):
        '''Add a node to the tail.'''
        assert not node.head
        old_tail = self.tail

        if old_tail:
            assert old_tail.head == self
            old_tail.head = node
            node.tail = old_tail

        node.head = self
        self.tail = node

    def unlink(self):
        '''Remove this node and link any head or tail.'''
        old_head = self.head
        old_tail = self.tail

        self.head = None
        self.tail = None

        if old_head:
            old_head.tail = old_tail

        if old_tail:
            old_tail.head = old_head


class LinkedList(object):
    '''Doubly linked list.

    Attributes:
        map (dict): A mapping of values to nodes.
        head (:class:`LinkedListNode`): The first node.
        tail (:class:`LinkedListNode`): The last node.
    '''
    def __init__(self):
        self.map = {}
        self.head = None
        self.tail = None

    def __contains__(self, value):
        return value in self.map

    def __iter__(self):
        current_node = self.head
        while True:
            if not current_node:
                break

            yield current_node.value

            current_node = current_node.tail

    def __reversed__(self):
        return reversed(self)

    def __len__(self):
        return len(self.map)

    def index(self, value):
        for test_value, count in zip(self, itertools.count()):
            if test_value == value:
                return count

        raise IndexError()

    def __getitem__(self, key):
        if not self.map:
            raise IndexError('List is empty.')

        if key == 0:
            return self.head.value
        elif key == len(self.map) - 1:
            return self.tail.value

        for value, count in zip(self, itertools.count()):
            if count == key:
                return value

        raise IndexError('Value not in list.')

    def append(self, value):
        if value in self.map:
            raise ValueError('Linked list can only contain one of value.')

        node = LinkedListNode(value)
        self.map[value] = node

        if self.tail:
            self.tail.link_tail(node)

        self.tail = node

        if not self.head:
            self.head = node

    def appendleft(self, value):
        if value in self.map:
            raise ValueError('Linked list can only contain one of value.')

        node = LinkedListNode(value)
        self.map[value] = node

        if self.head:
            self.head.link_head(node)

        self.head = node

        if not self.tail:
            self.tail = node

    def remove_node(self, node):
        if self.head == node:
            self.head = self.head.tail

        if self.tail == node:
            self.tail = self.tail.head

        node.unlink()

    def remove(self, value):
        try:
            node = self.map[value]
        except KeyError:
            raise ValueError('Value not in list.')

        del self.map[value]
        self.remove_node(node)

    def pop(self):
        if not self.map:
            raise IndexError('List is empty.')

        value = self.tail.value

        self.remove_node(self.tail)
        del self.map[value]
        return value

    def popleft(self):
        if not self.map:
            raise IndexError('List is empty.')

        value = self.head.value

        self.remove_node(self.head)
        del self.map[value]
        return value

    def clear(self):
        self.map = {}
        self.head = None
        self.tail = None
