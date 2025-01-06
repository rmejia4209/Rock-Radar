from PyQt5.QtWidgets import (
    QWidget, QPushButton, QFrame, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal
from UI.custom_widgets.labels import HeaderLabel
from UI.custom_widgets.inputs import DropDown, RadioButtons
from UI.components.area_downloader import AreaDownloads
from custom_types.crag import Area


class SortingSettings(QFrame):
    """
    TODO: doc string
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
        self._set_style()

    def _create_dropdown_layout(self) -> QHBoxLayout:
        """Returns a horizontal layout with the dropdowns"""
        layout = QHBoxLayout()
        for widget in [self._area_sorting, self._crag_sorting]:
            layout.addWidget(widget)
        return layout

    def _set_style(self) -> None:
        """Sets the main layout and style of the widget"""
        layout = QVBoxLayout()
        layout.addWidget(self._title)
        layout.addLayout(self._create_dropdown_layout())
        self.setLayout(layout)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)

    def get_selections(self) -> dict[str, str] | None:
        """Returns the current sort key selections"""
        area_option = self._area_sorting.current_val
        crag_option = self._crag_sorting.current_val

        if area_option and crag_option:
            return {'node': area_option, 'leaf': crag_option}
        return


class ModelOptions(QFrame):
    def __init__(self, options: list[str], *, parent: QWidget) -> None:
        """TODO"""
        super().__init__(parent=parent)
        self._title = HeaderLabel('Model Options', parent=self)
        self._model_options = RadioButtons(options, parent=self)
        self._set_style()

    def _set_style(self) -> None:
        """Sets the layout of the widget"""
        layout = QVBoxLayout()
        for widget in [self._title, self._model_options]:
            layout.addWidget(widget)
        self.setLayout(layout)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)

    def get_selection(self) -> str:
        """Returns the currently selected model"""
        return self._model_options.current_val


class MetricSelection(QFrame):
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

    def _set_style(self) -> None:
        """Set the style of the widget"""
        main_layout = QVBoxLayout()
        main_layout.addWidget(self._title)
        options = QHBoxLayout()
        for widget in [self._area_metrics, self._crag_metrics]:
            options.addWidget(widget)
        main_layout.addLayout(options)
        self.setLayout(main_layout)

    def get_selections(self) -> None:
        """Returns the current selections"""
        return self._area_metrics.current_val, self._crag_metrics.current_val


class Settings(QWidget):
    """
    TODO
    """
    settings_changed = pyqtSignal()

    def __init__(self, data_root: Area, *, parent: QWidget):
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

        self.foo = AreaDownloads(parent=self)

        self._connect_widgets()
        self._set_style()

    @property
    def title(self):
        return "Settings"

    def _connect_widgets(self):
        self._apply.clicked.connect(self.apply_sort_settings)

    def _group_left_side(self):
        layout = QVBoxLayout()
        for widget in [self._sort_settings, self._metrics]:
            layout.addWidget(widget)
        return layout

    def _group_right_side(self):
        layout = QVBoxLayout()
        layout.addWidget(self._model_options)
        return layout

    def _set_style(self) -> None:
        """TODO:"""
        main_layout = QVBoxLayout()
        widget_layout = QHBoxLayout()
        for layout in [self._group_left_side(), self._group_right_side()]:
            widget_layout.addLayout(layout)
        main_layout.addLayout(widget_layout)
        main_layout.addWidget(self._apply)
        main_layout.addWidget(self.foo)
        self.setLayout(main_layout)

    def _set_model(self) -> None:
        """Sets model if model has been selected"""
        model = self._model_options.get_selection()
        if model:
            self._data_root.set_ranking_model(model)
        return

    def _set_sort_keys(self) -> None:
        """Attempts to set the sorting keys if selected"""
        sort_keys = self._sort_settings.get_selections()
        if sort_keys:
            self._data_root.set_sort_keys(sort_keys)
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
