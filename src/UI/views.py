from PyQt5.QtWidgets import (QWidget, QFrame, QHBoxLayout)
# from PyQt5.QtCore import Qt
from UI.custom_widgets.composites import SingleStatDisplay
from custom_types.crag import Area


class NumberOfRoutes(QFrame):
    """.DS_Store"""
    def __init__(self, node: Area, parent: QWidget) -> None:
        super().__init__(parent=parent)

        self._total_routes = SingleStatDisplay(
            num=node.total_num_routes,
            label="Total Number of Routes",
            parent=self
        )
        self._matching_routes = SingleStatDisplay(
            num=node.num_matching_routes,
            label="Number of Matching Routes",
            parent=self
        )

        self._set_style()

    def _set_style(self):
        layout = QHBoxLayout()
        for widget in [self._total_routes, self._matching_routes]:
            layout.addWidget(widget)
        self.setLayout(layout)

    def update(self, node) -> None:
        self._total_routes.update(node.total_num_routes)
        self._matching_routes.update(node.num_matching_routes)
