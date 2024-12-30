from __future__ import annotations


class Node:
    """
    TODO:
    """
    # Instance attributes
    _name: str
    _parent: Node | None
    _children: list[Node]
    _is_leaf: bool

    # Class attributes
    _node_sort_key: str = "name"
    _leaf_sort_key: str = "name"
    _node_attributes: dict[str, str] = {}
    _leaf_attributes: dict[str, str] = {}

    def __init__(
        self, name: str, *, parent: Node | None = None, is_leaf: bool = False
    ) -> None:
        """.DS_Store"""
        self._name = name
        self._parent = parent
        self._is_leaf = is_leaf
        self._is_leaf_parent = False
        self._children = []

        if self._parent:
            self._parent.add_child(self)

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

    @property
    def node_sort_keys(self) -> list[str]:
        """Returns the valid inner node sorting keys"""
        return [val.title() for val in type(self)._node_attributes.keys()]

    @property
    def leaf_sort_keys(self) -> list[str]:
        """Returns the valid leaf sorting keys"""
        return [val.title() for val in type(self)._leaf_attributes.keys()]

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
                self._children.append(child)
        return

    def _set_sort_keys(self, **kwargs) -> None:
        """
        Sets the sorting keys for the entire tree. The sorting keys represent
        attributes of the node and are passed via a lambda funciton. Accepted
        key word arguments are outlined below. Will not changed unspecified
        keys.

        Args:
            - node_sort_key (str): Primary key for sorting internal nodes
            - leaf_sort_key (str): Primary key for sorting leaves
        """
        type(self)._node_sort_key = kwargs.get(
            "node_sort_key", type(self)._node_sort_key
        )

        type(self)._leaf_sort_key = kwargs.get(
            "leaf_sort_key", type(self)._leaf_sort_key
        )

        return

    def set_sort_keys(self, sort_keys: dict[str, str]) -> None:
        """Sets the sort keys based on the provided dictionary"""
        node_key = type(self)._node_attributes[sort_keys['node'].lower()]
        leaf_key = type(self)._leaf_attributes[sort_keys['leaf'].lower()]
        self._set_sort_keys(node_sort_key=node_key, leaf_sort_key=leaf_key)
        return

    def _sort_internal_node(self) -> None:
        """Sorts an internal node's children based on the set keys"""
        reversed_order = (
            not isinstance(getattr(self, type(self)._node_sort_key), str)
        )
        self._children.sort(
            key=lambda node: getattr(node, type(self)._node_sort_key),
            reverse=reversed_order
        )

    def _sort_leaf_nodes(self) -> None:
        """Sorts the children of a leaf parent node based on the set keys"""
        # TODO: code smell...
        bandaid = {'_length': 1, '_num_pitches': 1, '_grade': 'a'}
        val = getattr(self, type(self)._leaf_sort_key, None)
        val = bandaid.get(type(self)._leaf_sort_key) if val is None else val
        reversed_order = not isinstance(val, str)
        self._children.sort(
            key=lambda node: getattr(node, type(self)._leaf_sort_key),
            reverse=reversed_order
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
            self._sort_internal_node()
