from tkinter.tix import Tree
from typing import Dict, List

from src.LabelSetting.Models.NodeLabel import NodeLabel

class TreeNode:
    def __init__(self, index: int) -> None:
        self.index: int = index
        self.children: List[TreeNode] = []

class SpanningTree:

    def __init__(self, root: int, nodes: Dict[int, NodeLabel]) -> None:
        self.node_labels = nodes
        self.root: TreeNode = self.gen_spanning_tree(root)

    def gen_spanning_tree(self, node_index: int) -> TreeNode:
        root = TreeNode(node_index)

        children = self.node_labels[node_index].outgoing_nodes
        for child in children:
            child_node = self.gen_spanning_tree(child)
            root.children.append(child_node)

        return root
    
    @staticmethod
    def print_tree(root: TreeNode, indent_level: int = 0) -> None:
        SpanningTree._print_level(f"{root.index}", indent_level)
        for child in root.children:
            SpanningTree.print_tree(child, indent_level + 1)
    
    @staticmethod
    def _print_level(message: str, indent_level: int) -> None:
        indent = ""
        if indent_level > 0:
            indent = "|  " * (indent_level - 1)
            indent = f"{indent}|__"
        print(f"{indent}{message}")