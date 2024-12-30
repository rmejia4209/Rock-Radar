from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal
from UI.sidebar import Sidebar
from UI.crag_stats import CragStats
from UI.route_filter import RouteFilterWidget
from custom_types.node import Node

# TODO: add signal/slot to update node changes


class Home(QWidget):
    """
    TODO: write doc string
    """
    node_changed = pyqtSignal(str)

    def __init__(self, data_root: Node, *, parent: QWidget) -> None:
        """TODO: write doc string"""
        super().__init__(parent=parent)
        self._data = data_root
        self._side_bar = Sidebar(data_root, parent=self)
        self._area_stats = CragStats(data_root, parent=self)
        self._route_filter = RouteFilterWidget(
            self._data.route_filter, parent=self
        )
        self._connect_widgets()
        self._set_style()
        return

    @property
    def title(self) -> str:
        return f"{self._side_bar.current_node}"

    def _connect_widgets(self) -> None:
        """Connects the widget's children's signals & slots"""
        self._side_bar.level_changed.connect(
            lambda node: self._update_stats_and_title(node)
        )
        self._route_filter.filter_updated.connect(self.refresh_data)
        return

    def _update_stats_and_title(self, node: Node) -> None:
        """Updates the stats and title with the given node"""
        self._area_stats.update(node)
        self.node_changed.emit(f"{node.name}")
        return

    def _create_details_layout(self) -> QVBoxLayout:
        """TODO: write doc string"""
        layout = QVBoxLayout()
        for view in [self._route_filter, self._area_stats]:
            layout.addWidget(view)
        return layout

    def _set_style(self) -> None:
        main_layout = QHBoxLayout()
        main_layout.addWidget(self._side_bar)
        main_layout.addLayout(self._create_details_layout())
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

    def refresh_data(self) -> None:
        """Refreshes the data displayed"""
        self._data.calculate_stats()
        self._data.sort()
        node = self._side_bar.current_node
        self._area_stats.update(node)
        self._side_bar.refresh()
        return
