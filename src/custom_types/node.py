from __future__ import annotations


class Node:
    _name: str
    _parent: Node | None
    _children: list[Node]
    _is_leaf: bool
    _internal_keys: dict[str: any]
    _leaf_keys: dict[str: any]

    def __init__(
        self, name: str, *, parent: Node | None = None, is_leaf: bool = False
    ) -> None:
        """.DS_Store"""
        self._name = name
        self._parent = parent
        if self._parent:
            self._parent.add_child(self)

        self._is_leaf = is_leaf
        self._is_leaf_parent = False

    def __str__(self) -> str:
        return f"{self._name}"

    @property
    def name(self) -> str:
        return self._name

    @property
    def parent(self) -> Node:
        return self._parent

    @property
    def children(self) -> list[Node]:
        if self._is_leaf:
            raise Exception("Error: Cannot access children of a leaf node")
        else:
            return self._children

    @property
    def is_leaf(self) -> bool:
        """Returns is_leaf attribute"""
        return self._is_leaf

    @property
    def is_leaf_parent(self) -> bool | None:
        """Returns true if node has leaves as children"""
        return self._is_leaf_parent

    def _add_leaf(self, child: Node) -> None:
        """
        Attempts to add a leaf child to _children. Raises exception if
        the node is not a parent of leaf children.
        """
        # Set leaf parent status iff length is 0
        if len(self._children) == 0:
            self._is_leaf_parent = True

        if self._is_leaf_parent:
            self._children.append(child)
        else:
            raise Exception("Error: Cannot add non-leaf node to leaf parent")
        return

    def add_child(self, child: Node) -> None:
        """
        Adds a child to the node. Raises error if node is a leaf.
        Raises error if child is leaf and node contains non-leaf nodes.
        """
        if self._is_leaf:
            raise Exception("Error: Cannot add child to leaf node")
        else:
            if child.is_leaf:
                self._add_leaf(child)
            else:
                self._children(child)
        return

    @property
    def sort_keys(self, **kwargs) -> None:
        self._internal_node_key = kwargs.get(
            "internal_node_key", self._internal_node_key
        )
        self._primary_leaf_key = kwargs.get(
            "leaf_node_key", self._internal_node_key
        )

    def _sort_leaf_nodes(self) -> None:
        """Sorts the children of a leaf parent node based on the set keys"""
        self._children.sort(
            key=lambda node: getattr(node, self._primary_leaf_key),
            reverse=self._primary_leaf_key_reverse
        )

    def _sort_internal_node(self) -> None:
        """Sorts an internal node's children based on the set keys"""
        self._children.sort(
            key=lambda node: getattr(node, self._primary_key),
            reverse=self._primary_key_reverse
        )

    def sort(self) -> None:
        """
        Recursively sorts all of the children node. Does not sort leaf
        nodes (i.e., sorting stops at leaf parents)
        """
        # Base case - Sorting stops at the parents of leaf nodes
        if self._is_leaf_parent:
            self._sort_leaf_nodes()
        else:
            for child in self._children:
                child.sort()
            self._sort_internal_node._
