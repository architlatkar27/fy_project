class Data:
    def __init__(self, value, node):
        self.value = value
        self.nodes = [node, ]

    def __str__(self) -> str:
        return "value: {} nodes: {}\n".format(self.value, self.nodes)
    
    def add_node(self, node):
        self.nodes.append(node)


class BTreeNode:
    '''
    leaf: bool -- indicates whether node is leaf node or not
    keys: list -- list of Data objects
    child: list -- list of child nodes of the node
    '''

    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.child = []

    def __str__(self) -> str:
        return "is leaf: {}\nkeys: {}\nchild: {}".format(self.leaf, self.keys, self.child)

# Tree
class BTree:
    '''
    root: BtreeNode -- root node
    t:    int -- degree of each node
    insert(): takes in value and node and then performs insertion
    print_tree(): prints complete tree
    search_key(): search for key in the btree
    '''
    def __init__(self, t, default):
        self.root = BTreeNode(True)
        self.t = t
        self.default = default
        print("created btree")

        # Insert node
    def insert(self, k):
        root = self.root
        # print(root)
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode()
            self.root = temp
            temp.child.insert(0, root)
            self.split_child(temp, 0)
            self.insert_non_full(temp, k)
        else:
            self.insert_non_full(root, k)

        # Insert nonfull
    def insert_non_full(self, x, k):
        '''
        k is the insertion key of the form (key, containerID)
        x is the node in which it is to be inserted
        '''
        # val, node = k
        # print(k)
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(Data(self.default, -1))
            while i >= 0 and k[0] < x.keys[i].value:
                # print("i: {}".format(i))
                x.keys[i + 1] = x.keys[i]
                i -= 1
            if x.keys[i].value != k[0]:
                x.keys[i + 1] = Data(k[0], k[1])
            elif x.keys[i].value == k[0] and k[1] not in x.keys[i].nodes:
                x.keys[i].nodes.append(k[1])
        else:
            while i >= 0 and k[0] <= x.keys[i].value:
                i -= 1
            i += 1
            if len(x.child[i].keys) == (2 * self.t) - 1:
                self.split_child(x, i)
                if k[0] > x.keys[i].value:
                    i += 1
            self.insert_non_full(x.child[i], k)

        # Split the child
    def split_child(self, x, i):
        t = self.t
        y = x.child[i]
        z = BTreeNode(y.leaf)
        x.child.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        if not y.leaf:
            z.child = y.child[t: 2 * t]
            y.child = y.child[0: t - 1]

    # Print the tree
    def print_tree(self, x, l=0):
        print("Level ", l, " ", len(x.keys), end=":")
        for i in x.keys:
            print(i, end=" ")
        print()
        l += 1
        if len(x.child) > 0:
            for i in x.child:
                self.print_tree(i, l)

    # Search key in the tree
    def search_key(self, k, x=None):
        if x is not None:
            i = 0
            while i < len(x.keys) and k > x.keys[i].value:
                i += 1
            if i < len(x.keys) and k == x.keys[i].value:
                return x.keys[i]
            elif x.leaf:
                return False
            else:
                return self.search_key(k, x.child[i])

        else:
            return self.search_key(k, self.root)

    def search_range(self, mink, maxk, x=None):
        '''
        query for certain range

        Algorithm - 
        i = 0
        Find the least value gte mink. then go for every value in the node till lte maxk
        '''
        pass

# def main():
    # B = BTree(3)

    # for i in range(30):
    #     # B.insert((i, 2 * i))
    #     # print("insert iteration: {}".format(i))
    #     B.insert((i%3, i%4))
    #     # B.print_tree(B.root)

    # B.print_tree(B.root)

    # node, i = B.search_key(2)
    # print(node)
    # print(i)


# if __name__ == '__main__':
#     main()
