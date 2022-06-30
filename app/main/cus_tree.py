class Data:
    def __init__(self, key):
        self.key = key
        self.values = set()

    def add_node(self, value):

        self.values.add(value)


# Tree
class Tree:

    def __init__(self, index):
        self.index = index
        self.nodes = dict()
        print("created Tree")

        # Insert node
    def insert(self, key, value):
        if key not in self.nodes:
            self.nodes[key] = Data(key)
            self.nodes[key].add_node(value)
        else:
            self.nodes[key].add_node(value)
    # Print the tree
    def print_tree(self):
        print("Index: " + str(self.index))
        for k, v in self.nodes.items():
            print(k, v.values)
            # print(str(k) + ", " + str(v))

    # Search key in the tree
    def search_key(self, key):
        print(self.nodes)
        if key in self.nodes.keys():
            return self.nodes[key].values
        else:
            return set()

# def main():
#     B = Tree()

#     B.insert(6, "shard1")
#     B.insert(6, "shard2")
#     B.insert(6, "shard3")
#     B.insert(5, "shard1")
#     B.insert(5, "shard6")
#     B.insert(6, "shard4")
#     B.insert(4, "shard11")
#     B.insert(6, "shard1")

#     B.print_tree()

#     x = B.search_key(6)
#     print(x)


# if __name__ == '__main__':
#     main()
