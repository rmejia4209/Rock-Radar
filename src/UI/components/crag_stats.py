from PyQt5.QtWidgets import (QWidget, QFrame, QHBoxLayout, QVBoxLayout)
from UI.custom_widgets.charts import PieChart, BarGraph
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
        self._grade_frequencies = BarGraph(
            node.grades, 'Crag Grades', parent=self
        )

        self._set_style()

    def _create_top_row(self) -> QHBoxLayout:
        """Returns a horizontal layout"""
        layout = QHBoxLayout()
        for widget in [self._matching_routes, self._route_types]:
            layout.addWidget(widget)
        return layout

    def _create_main_layout(self) -> QVBoxLayout:
        """Returns the main layout"""
        layout = QVBoxLayout()
        layout.addLayout(self._create_top_row())
        layout.addWidget(self._grade_frequencies)
        return layout

    def _set_style(self):
        self.setLayout(self._create_main_layout())

    def update(self, node) -> None:
        self._matching_routes.update_val(node.num_matching_routes)
        self._route_types.update_data(node.route_types)
        self._grade_frequencies.update_data(node.grades)
