import math

class Node:
    def __init__(self, key, node):
        self.key = key
        self.nodes = [node, ]
        self.left = None
        self.right = None

class height:
    def __init__(self):
        self.height = 0

def insert(root, key, node):
    '''
    Take in key and node and add it to the bst
    '''
    
