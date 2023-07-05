class BPlusTree:
    class Node:
        def __init__(self, is_leaf=False):
            self.keys = []
            self.children = []
            self.is_leaf = is_leaf
            self.next_leaf = None

    def __init__(self, order=5):
        self.root = self.Node(is_leaf=True)
        self.order = order

    def __split_child__(self, parent, index):
        node = parent.children[index]
        new_node = self.Node(is_leaf=node.is_leaf)
        parent.keys.insert(index, node.keys[self.order - 1])
        parent.children.insert(index + 1, new_node)
        new_node.keys = node.keys[self.order: (2 * self.order - 1)]
        node.keys = node.keys[0: (self.order - 1)]
        if not node.is_leaf:
            new_node.children = node.children[self.order: (2 * self.order)]
            node.children = node.children[0: self.order]

    def __insert_non_full__(self, node, key):
        index = len(node.keys) - 1
        if node.is_leaf:
            node.keys.append(None)
            while index >= 0 and str(key) < str(node.keys[index]):
                node.keys[index + 1] = node.keys[index]
                index -= 1
            node.keys[index + 1] = key
        else:
            while index >= 0 and str(key) < str(node.keys[index]):
                index -= 1
            index += 1
            if len(node.children[index].keys) == (2 * self.order):
                self.__split_child__(node, index)
                if key > node.keys[index]:
                    index += 1
            self.__insert_non_full__(node.children[index], key)

    def __delete_key__(self, node, key):
        if node.is_leaf:
            index = 0
            while index < len(node.keys) and str(key) > str(node.keys[index]):
                index += 1
            if index < len(node.keys) and key == node.keys[index]:
                node.keys.pop(index)
        else:
            index = 0
            while index < len(node.keys) and str(key) > str(node.keys[index]):
                index += 1
            if index < len(node.keys) and key == node.keys[index]:
                self.__delete_internal_key__(node, key, index)
            else:
                self.__delete_key__(node.children[index], key)

    def __delete_internal_key__(self, node, key, index):
        if node.is_leaf:
            node.keys.pop(index)
        else:
            predecessor = node.children[index]
            if len(predecessor.keys) >= self.order:
                predecessor_key = self.__get_predecessor_key__(predecessor)
                node.keys[index] = predecessor_key
                self.__delete_key__(predecessor, predecessor_key)
            else:
                successor = node.children[index + 1]
                if len(successor.keys) >= self.order:
                    successor_key = self.__get_successor_key__(successor)
                    node.keys[index] = successor_key
                    self.__delete_key__(successor, successor_key)
                else:
                    predecessor.keys.append(node.keys[index])
                    predecessor.keys += successor.keys
                    predecessor.children += successor.children
                    node.keys.pop(index)
                    node.children.pop(index + 1)
                    self.__delete_key__(predecessor, key)

    def __get_predecessor_key__(self, node):
        if node.is_leaf:
            return node.keys[-1]
        return self.__get_predecessor_key__(node.children[-1])

    def __get_successor_key__(self, node):
        if node.is_leaf:
            return node.keys[0]
        return self.__get_successor_key__(node.children[0])

    def __search_key__(self, node, key):
        if node.is_leaf:
            for i, k in enumerate(node.keys):
                if k == key:
                    return node
            return None
        else:
            i = 0
            while i < len(node.keys) and str(key) > str(node.keys[i]):
                i += 1
            if i < len(node.keys) and str(key) == str(node.keys[i]):
                return node
            else:
                return self.__search_key__(node.children[i], key)

    def __contains__(self, key):
        return self.search(key) is not None

    def insert(self, key):
        if key in self:
            return

        if len(self.root.keys) == (2 * self.order):
            old_root = self.root
            self.root = self.Node()
            self.root.children.append(old_root)
            self.__split_child__(self.root, 0)

        self.__insert_non_full__(self.root, key)

    def delete(self, key):
        if key not in self:
            return

        if len(self.root.keys) == 0:
            if self.root.is_leaf:
                self.root = None
            else:
                self.root = self.root.children[0]
        self.__delete_key__(self.root, key)

    def search(self, key):
        return self.__search_key__(self.root, key)

    def print_tree(self):
        if not self.root:
            print("Tree is empty.")
            return

        queue = [(self.root, 0)]
        while queue:
            node, level = queue.pop(0)
            indent = "  " * level

            if node.is_leaf:
                print(indent + "Leaf Node:")
                keys_str = ", ".join(str(key) for key in node.keys)
                print(indent + "Keys: " + keys_str)
            else:
                print(indent + "Internal Node:")
                keys_str = ", ".join(str(key) for key in node.keys)
                print(indent + "Keys: " + keys_str)

            if not node.is_leaf:
                for child in node.children:
                    queue.append((child, level + 1))



if __name__=="__main__":
    a = BPlusTree() 
    for i in range (0, 25):
        a.insert(f"cool {i}")

    print(a.__contains__("cool 10"))
    a.insert(20)
    a.insert(30)
    a.insert(30.12353)
    a.delete(20)
    a.delete(30.12353)
    a.print_tree()
