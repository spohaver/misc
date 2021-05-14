#!/usr/bin/env python3
# Testing out the Binary Search Tree


class binarySearchTree:

    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def add_item(self, item):
        """ adds an item either to the left or right of the root self.data
        :param item: item to be added
        :type item: int/str
        """
        if isinstance(item, int):
            item = str(item)
        if item == self.data:
            return

        if item < self.data:
            # add data in the left subtree
            if self.left:
                self.left.add_item(item)
            else:
                self.left = binarySearchTree(item)
        else:
            # add data in the right subtree
            if self.right:
                self.right.add_item(item)
            else:
                self.right = binarySearchTree(item)

    def ordered_sort(self):
        """ does an in-order-traversal through the items in the tree, starting
            with the left most item, working to the right
        :returns: list of items sorted in order, ascending
        :rtype: list
        """
        elements = []
        # visit left tree
        if self.left:
            elements += self.left.ordered_sort()
        # visit base node
        elements.append(self.data)
        # visit right tree
        if self.right is not None:
            elements += self.right.ordered_sort()
        return elements

    def reverse_sort(self):
        """ does an reverse-order-traversal through the items in the tree,
            starting with the right most item, working to the left
        :returns: list of items sorted in order, descending
        :rtype: list
        """
        elements = []
        # visit right tree
        if self.right is not None:
            elements += self.right.reverse_sort()
        # visit base node
        elements.append(self.data)
        # visit left tree
        if self.left:
            elements += self.left.reverse_sort()
        return elements

    def search(self, query):
        """ takes the query and goes through the tree to see if theres a match
        :param query: the search query
        :type query: int/str
        :return: True if found, False if not found
        :rtype: bool
        """
        if self.data == query:
            return True

        if val < self.data:
            if self.left:
                self.left.search(query)
            else:
                return False
        if val > self.data:
            if self.right:
                return self.left.search(query)
            else:
                return False


def build_tree(elements):
    """ take first item of the list as the root of the BST, and build a tree
    :param elements: A list of elements
    :type elements: list
    :return: binary search tree object based on elements
    :rtype: object
    """
    # TODO: probably take the list, sort, get middle value & place as root
    if not isinstance(elements, list):
        print('data provided is not in a list format')
    root = binarySearchTree(elements[0])
    for index in range(1, len(elements)):
        root.add_item(elements[index])
    return root
