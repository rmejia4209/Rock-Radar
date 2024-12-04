import os
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout
from PyQt5.QtCore import pyqtSignal
from UI.custom_widgets.buttons import ButtonWithIcon
from UI.custom_widgets.navigation import ScrollableLinkList
from UI.custom_widgets.labels import RegularLabel
from custom_types.node import Node


class Sidebar(QFrame):
    level_changed = pyqtSignal(Node)

    def __init__(self, current_node: Node, parent: QWidget) -> None:
        super().__init__(parent=parent)

        self._current_node = current_node

        fp = os.path.join(os.path.dirname(__file__), "Icons", "back.png")
        self._search = RegularLabel("Search Coming Soon", parent=self)
        self._back_button = ButtonWithIcon("Back", fp, parent=self)
        self._links = ScrollableLinkList(self._current_node, parent=self)

        self._connect_widgets()
        self._set_style()

        return

    @property
    def current_node(self) -> Node:
        """Returns the current node"""
        return self._current_node

    def _update_node(self, node: Node) -> None:
        self._current_node = node
        self._back_button.setToolTip(f"{self._current_node}")
        # self._title.setText(f"{self._current_node}")
        self.level_changed.emit(self._current_node)

    def move_down(self, node: Node) -> None:
        self._back_button.show()
        self._update_node(node)

    def move_up(self) -> None:
        if self._current_node.parent:
            self._update_node(self._current_node.parent)
            self._links.move_up()

        if not self._current_node.parent:
            self._back_button.hide()

    def _connect_widgets(self) -> None:
        self._links.level_changed.connect(lambda node: self.move_down(node))
        self._back_button.clicked.connect(self.move_up)

    def _set_layout(self) -> None:
        """Sets the layout of the widget"""
        layout = QVBoxLayout()
        for widget in [self._search, self._back_button, self._links]:
            layout.addWidget(widget)
        layout.setSpacing(5)
        self.setLayout(layout)

    def _set_style(self) -> None:
        """Set up the main layout"""

        self._set_layout()
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)
        self._back_button.hide()
        return
