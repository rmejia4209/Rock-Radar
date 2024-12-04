from __future__ import annotations


class Node:
    _name: str
    _parent: Node | None
    _children: list[Node]
    _is_leaf: bool

    def __init__(
        self, name: str, *, parent: Node | None = None, is_leaf: bool = False
    ) -> None:
        """.DS_Store"""
        self._name = name
        self._parent = parent
        if self._parent:
            self._parent.add_child(self)

        self._is_leaf = is_leaf

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
        return self._is_leaf

    @property
    def is_leaf_parent(self) -> bool | None:
        """Returns True if area has children of type Route or no children"""
        if len(self._children):
            return self._children[0].is_leaf

    def add_child(self, child: Node) -> None:
        self._children.append(child)
