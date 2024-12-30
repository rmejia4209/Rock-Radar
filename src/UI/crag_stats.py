from PyQt5.QtWidgets import (QWidget, QFrame, QHBoxLayout)
from UI.custom_widgets.charts import PieChart
from UI.custom_widgets.composites import SingleStatDisplay
from custom_types.crag import Area


class CragStats(QFrame):
    """.DS_Store"""
    def __init__(self, node: Area, *, parent: QWidget) -> None:
        super().__init__(parent=parent)

        self._route_types = PieChart(
            node.route_types, "Route Types", parent=self
        )

        self._matching_routes = SingleStatDisplay(
            num=node.num_matching_routes,
            label="Number of Matching Routes",
            parent=self
        )

        self._set_style()

    def _set_style(self):
        layout = QHBoxLayout()
        for widget in [self._matching_routes, self._route_types]:
            layout.addWidget(widget)
        self.setLayout(layout)

    def update(self, node) -> None:
        self._matching_routes.update(node.num_matching_routes)
        self._route_types.update_data(node.route_types)
