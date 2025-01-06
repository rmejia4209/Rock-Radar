from PyQt5.QtWidgets import (
    QWidget, QPushButton, QFrame, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal
from UI.custom_widgets.labels import HeaderLabel
from UI.custom_widgets.inputs import DropDown, RadioButtons
from UI.components.area_downloader import AreaDownloader
from custom_types.crag import Area


class SortingSettings(QFrame):
    """
    This widget groups together settings related to sorting crags & routes.
    """

    def __init__(
        self, area_options: list[str], crag_options: list[str],
        *, parent: QWidget
    ) -> None:
        super().__init__(parent=parent)
        self._title = HeaderLabel('Sorting Settings', parent=self)
        self._area_sorting = DropDown(
            area_options, 'Sort crags by', 'Please select', parent=self
        )
        self._crag_sorting = DropDown(
            crag_options, 'Sort routes by', 'Please select', parent=self
        )
        self._set_main_layout()

    def _create_dropdown_layout(self) -> QHBoxLayout:
        """Returns a horizontal layout with the dropdowns"""
        layout = QHBoxLayout()
        for widget in [self._area_sorting, self._crag_sorting]:
            layout.addWidget(widget)
        return layout

    def _set_main_layout(self) -> None:
        """Sets the main layout and style of the widget"""
        layout = QVBoxLayout()
        layout.addWidget(self._title)
        layout.addLayout(self._create_dropdown_layout())
        self.setLayout(layout)

    def get_selections(self) -> tuple[str, str]:
        """Returns the current sort key selections"""
        return self._area_sorting.current_val, self._crag_sorting.current_val


class ModelOptions(QFrame):
    """
    Contains settings related to the model used to compare crags.

    The raw model is simply the sum of the product of popularity and rating
    for each route in a crag (i.e., sum([popularity * rating])).

    The logarithmic model is the sum of the the product of the log of the
    popularity and rating for each route in a crag
    (i.e., sum([log(popularity) * rating])). This
    """

    def __init__(self, options: list[str], *, parent: QWidget) -> None:
        super().__init__(parent=parent)
        self._title = HeaderLabel('Model Options', parent=self)
        self._model_options = RadioButtons(options, parent=self)
        self._set_layout()

    def _set_layout(self) -> None:
        """Sets the layout of the widget"""
        layout = QVBoxLayout()
        for widget in [self._title, self._model_options]:
            layout.addWidget(widget)
        self.setLayout(layout)

    def get_selection(self) -> str:
        """Returns the currently selected model"""
        return self._model_options.current_val


class MetricSelection(QFrame):
    """
    Groups together settings for metrics displayed next to crags and routes.
    """
    def __init__(
        self, area_options: list[str], crag_options: list[str],
        *, parent: QWidget
    ) -> None:
        """TODO"""
        super().__init__(parent=parent)
        self._title = HeaderLabel('Metrics', parent=self)

        self._area_metrics = DropDown(
            area_options, "Crag Metric", "Please Select", parent=self
        )
        self._crag_metrics = DropDown(
            crag_options, "Route Metric", "Please Select", parent=self
        )
        self._set_style()

    def _create_dropdown_layout(self) -> QHBoxLayout:
        """Returns a horizontal layout with the dropdowns"""
        layout = QHBoxLayout()
        for widget in [self._area_metrics, self._crag_metrics]:
            layout.addWidget(widget)
        return layout

    def _set_style(self) -> None:
        """Set the style of the widget"""
        main_layout = QVBoxLayout()
        main_layout.addWidget(self._title)
        main_layout.addLayout(self._create_dropdown_layout())
        self.setLayout(main_layout)

    def get_selections(self) -> None:
        """Returns the current selections"""
        return self._area_metrics.current_val, self._crag_metrics.current_val


class Settings(QWidget):
    """
    Container widget that contains settings for the app
    """
    settings_changed = pyqtSignal()

    def __init__(self, data_root: Area, *, parent: QWidget) -> None:
        super().__init__(parent=parent)
        self._data_root = data_root
        self._sort_settings = SortingSettings(
            data_root.node_sort_keys, data_root.leaf_sort_keys, parent=self
        )
        self._model_options = ModelOptions(self._data_root.models, parent=self)
        self._metrics = MetricSelection(
            self._data_root.get_area_metrics(),
            self._data_root.get_crag_metrics(),
            parent=self
        )
        self._apply = QPushButton("Apply")

        self._connect_widgets()
        self._set_main_layout()

    def _connect_widgets(self):
        self._apply.clicked.connect(self.apply_sort_settings)

    def _group_left_side(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        for widget in [self._sort_settings, self._metrics]:
            layout.addWidget(widget)
        return layout

    def _group_right_side(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.addWidget(self._model_options)
        return layout

    def _group_top(self) -> QHBoxLayout:
        """Returns a layout with the left and right sides added in"""
        layout = QHBoxLayout()
        for side in [self._group_left_side(), self._group_right_side()]:
            layout.addLayout(side)
        return layout

    def _set_main_layout(self) -> None:
        """Sets the main layout of the container widget"""
        main_layout = QVBoxLayout()
        main_layout.addLayout(self._group_top())
        main_layout.addWidget(self._apply)
        self.setLayout(main_layout)

    def _set_model(self) -> None:
        """Sets model if model has been selected"""
        model = self._model_options.get_selection()
        if model:
            self._data_root.set_ranking_model(model)
        return

    def _set_sort_keys(self) -> None:
        """Sets the sorting keys if both have been selected"""
        node_key, leaf_key = self._sort_settings.get_selections()
        if node_key and leaf_key:
            self._data_root.set_sort_keys({'node': node_key, 'leaf': leaf_key})
        return

    def _set_display_metrics(self) -> None:
        """Attempts to set the display metrics"""
        area_metric, crag_metric = self._metrics.get_selections()
        if area_metric:
            self._data_root.set_area_metric(area_metric)
        if crag_metric:
            self._data_root.set_crag_metric(crag_metric)
        return

    def apply_sort_settings(self) -> None:
        """Applies the current selections to the sort settings"""
        self._set_model()
        self._set_display_metrics()
        self._set_sort_keys()
        self.settings_changed.emit()
