import matplotlib.pyplot as plt

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def rotate_right(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def rotate_left(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def insert(self, root, key):
        # Keep track of rotations
        self.last_action = f"Inserting {key}"
        
        if not root:
            return Node(key)

        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Balance cases
        if balance > 1 and key < root.left.key:  # Left Left
            self.last_action += "\nLeft-Left Rotation"
            return self.rotate_right(root)
        if balance < -1 and key > root.right.key:  # Right Right
            self.last_action += "\nRight-Right Rotation"
            return self.rotate_left(root)
        if balance > 1 and key > root.left.key:  # Left Right
            self.last_action += "\nLeft-Right Rotation"
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        if balance < -1 and key < root.right.key:  # Right Left
            self.last_action += "\nRight-Left Rotation"
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def pre_order(self, root):
        result = []
        if root:
            result.append(root.key)
            result.extend(self.pre_order(root.left))
            result.extend(self.pre_order(root.right))
        return result

    def visualize(self, root, filename, action):
        fig, ax = plt.subplots(figsize=(10, 8))
        self._plot_tree(ax, root, 0, 0, 1)
        
        plt.text(0, -2, action, ha='center', va='center', fontsize=10, 
                bbox=dict(facecolor='white', edgecolor='black', alpha=0.7))
        
        ax.set_axis_off()
        # Adjust the plot limits to accommodate the text
        ax.set_ylim(bottom=-3)
        plt.savefig(filename, bbox_inches='tight')
        plt.close(fig)

    def _plot_tree(self, ax, node, x, y, dx):
        if node:
            balance = self.get_balance(node)
            node_label = f"{node.key}\n(Balance: {balance})"
            ax.text(x, y, node_label, ha='center', va='center', fontsize=10, 
                   bbox=dict(facecolor='white', edgecolor='black'))
            if node.left:
                ax.plot([x, x - dx], [y, y - 1], 'k-')
                self._plot_tree(ax, node.left, x - dx, y - 1, dx / 2)
            if node.right:
                ax.plot([x, x + dx], [y, y - 1], 'k-')
                self._plot_tree(ax, node.right, x + dx, y - 1, dx / 2)

# Inserting the letters into the AVL Tree
# letters = ["G", "T", "M", "E", "D", "J", "P", "F", "R", "Q", "A", "H"]

# D, J, E, F, H, Q, M et A
letters = ["D", "J", "E", "F", "H", "Q", "M", "A"]

avl_tree = AVLTree()
root = None

for i, letter in enumerate(letters):
    root = avl_tree.insert(root, letter)
    avl_tree.visualize(root, f"avl_tree_step_{i}.png", avl_tree.last_action)

list = avl_tree.pre_order(root)

print("Preorder traversal of the AVL Tree after inserting the given letters:")
print(list)
