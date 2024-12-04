from PyQt5.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QHBoxLayout, QScrollArea, QStackedLayout
)
from PyQt5.QtCore import pyqtSignal, Qt
from UI.custom_widgets.buttons import Link, Icon
from UI.custom_widgets.labels import RegularLabel, TitleLabel
from custom_types.node import Node


class LinkList(QFrame):
    """
    Widget that displays the children of a given node. Useful for moving
    down a tree. Requires a button to be connected to the available signal
    to traverse back up.

    Attributes:
        _current_node: Current parent node.
        _links (list[Link] | list[RegularLabel]): List of widgets displayed.

    Signals:
        level_changed (pyqtSignal): emit's the currently selected node
                                        after the widget has updated
    """
    level_changed: pyqtSignal = pyqtSignal(Node)
    _current_node: Node
    _links: list[Link] | list[RegularLabel]

    def __init__(self, current_node: Node, parent: QWidget) -> None:
        """
        Args:
            current_node (Node): Current parent node
            parent (QWidget): The parent of the widget.
        """
        super().__init__(parent=parent)
        self._current_node = current_node
        self._links = []

        self._layout = QVBoxLayout()
        self._set_style()
        return

    def _build_link_list(self) -> None:
        """
        Iterates over the children of the current node. If the current node
        is a parent of leaves, RegularLabels are added to _links. Otherwise,
        Links are added and a lambda function is connected to their
        clicked event.
        """
        is_leaf_parent = self._current_node.is_leaf_parent
        for child in self._current_node.children:
            if is_leaf_parent:
                new_link = RegularLabel(txt=f"{child}", parent=self)
            else:
                new_link = Link(text=f"{child}", tip=f"{child}", parent=self)
                new_link.clicked.connect(
                    lambda state, root=child: self.update_links(root)
                )
            self._links.append(new_link)
        return

    def _add_children_to_layout(self) -> None:
        """Adds the widgets in _links to the layout"""
        for link in self._links:
            self._layout.addWidget(link, alignment=Qt.AlignTop | Qt.AlignLeft)
        self._layout.addStretch()
        return

    def _set_style(self) -> None:
        """Sets the main layout and margins of the widget"""
        self._build_link_list()
        self._add_children_to_layout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)

    def _disconnect_signals(self) -> None:
        """Removes connection from Link"""
        if len(self._links) > 0 and isinstance(self._links[0], Link):
            for link in self._links:
                link.clicked.disconnect()

    def _remove_links_from_layout(self) -> None:
        """Clears the Links/RegularLabels from the layout and from _links"""
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._links.clear()

    def update_links(self, node: Node, emit: bool = True) -> None:
        """
        Updates the list of Links/RegularLabels.
        Args:
            node (Node): The new parent node
            emit (bool): True if signal should be emitted
        """
        self._disconnect_signals()
        self._remove_links_from_layout()
        self._current_node = node
        self._build_link_list()
        self._add_children_to_layout()
        # Signal is only emitted when moving down the tree
        if emit:
            self.level_changed.emit(self._current_node)

    def move_up(self) -> None:
        """Updates list of Links by move up the tree. Signal is suppressed"""
        self.update_links(node=self._current_node.parent, emit=False)


class ScrollableLinkList(QScrollArea):
    """
    Wrapper class for LinkList. Used to keep the sized fixed and add a
    scroll bar as needed.
    Attributes:
        _links (LinkList): Widget that contains the Links
    Signals:
        level_changed (pyqtSignal): Signal used to connect to the LinkList
    """
    level_changed: pyqtSignal = pyqtSignal(Node)
    _links: LinkList

    def __init__(self, current_node: Node, parent: QWidget) -> None:
        """
        Args:
            current_node (Node): The current node
            parent (QWidget): The parent of the widget
        """
        super().__init__(parent=parent)
        self._links = LinkList(current_node=current_node, parent=self)
        self._links.level_changed.connect(
            lambda node: self.level_changed.emit(node)
        )
        self._set_style()
        return

    def _set_style(self) -> None:
        """Sets the style of the widget"""
        # self.setStyleSheet("border-color: transparent;")
        self.setFrameShape(QFrame.NoFrame)

        self.setWidget(self._links)
        self.setWidgetResizable(True)
        return

    def move_up(self) -> None:
        """Calls the move_up method of the LinkList widget"""
        self._links.move_up()
        return


class DualIcon(QWidget):
    """TODO: write docstring"""
    index_changed = pyqtSignal(int)

    def __init__(
        self, file_paths: tuple[str, str], *, parent: QWidget
    ) -> None:
        super().__init__(parent=parent)
        self._buttons = [Icon(fp, parent=self) for fp in file_paths]
        self._layout = QStackedLayout()
        self._set_style()

    def _flip_button(self) -> None:
        """Changes the current layout displayed & emits a signal"""
        next_idx = 1 if self._layout.currentIndex() == 0 else 0
        self._layout.setCurrentIndex(next_idx)
        self.index_changed.emit(next_idx)

    def _set_style(self) -> None:
        """
        Connects the buttons to the _flip_button method and
        adds them to the stacked layout
        """
        for button in self._buttons:
            button.clicked.connect(self._flip_button)
            self._layout.addWidget(button)
        self.setLayout(self._layout)


class DualPageNavBar(QFrame):
    """TODO: write docstring"""
    page_changed = pyqtSignal(int)

    def __init__(
        self, txt: str, file_paths: tuple[str, str], *, parent: QWidget
    ) -> None:
        super().__init__(parent=parent)
        self._button = DualIcon(file_paths, parent=self)
        self._button.index_changed.connect(
            lambda idx: self.page_changed.emit(idx)
        )
        self._title = TitleLabel(txt, parent=self)
        self._set_style()

    def _create_layout(self) -> QHBoxLayout:
        """Returns a stylized layout with the widgets added"""
        layout = QHBoxLayout()
        for widget in [self._button, self._title]:
            layout.addWidget(widget, alignment=Qt.AlignCenter)
            layout.addStretch(1)
        layout.setSizeConstraint(QHBoxLayout.SetMinimumSize)
        layout.setContentsMargins(0, 0, 0, 0)
        return layout

    def _set_style(self) -> None:
        """Sets the style of the widget"""
        self.setLayout(self._create_layout())
        self.setSizePolicy(
            self.sizePolicy().Preferred, self.sizePolicy().Fixed
        )
        return

    def _turn_on_borders(self) -> None:
        """Turns on the borders to better visualize the widget"""
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)

    def update_title(self, txt: str) -> None:
        """Updates the title"""
        self._title.setText(txt)
