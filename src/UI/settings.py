from PyQt5.QtWidgets import (
    QWidget, QPushButton, QFrame, QVBoxLayout, QHBoxLayout, QLineEdit
)

from UI.custom_widgets.labels import TitleLabel, HeaderLabel
from UI.custom_widgets.inputs import (
    DropDown, RadioButtons, Slider, NumLineEdit
)
from custom_types.crag import Area


class SortBy(QWidget):
    """
    TODO: doc string
    """

    def __init__(
        self, sorting_options: list[str], obj: str, *, parent: QWidget
    ) -> None:
        super().__init__(parent=parent)
        self._primary_key = DropDown(
            sorting_options, f'Sort {obj} by', 'Please select', parent=self
        )
        self._secondary_key = DropDown(
            sorting_options, 'then by', 'Please select', parent=self
        )
        self._connect_widgets()
        self._set_style()

    def _connect_widgets(self) -> None:
        """
        Connects the drop downs to update the selection in the
        secondary/primary dropdown when a selection is made in the
        primary/secondary dropdown.
        """
        self._primary_key.item_changed.connect(
            lambda selected_option: self._clear_selection(
                selected_option, self._secondary_key
            )
        )
        self._secondary_key.item_changed.connect(
            lambda selected_option: self._clear_selection(
                selected_option, self._primary_key
            )
        )

    def _clear_selection(self, option: str, dropdown: DropDown) -> None:
        """
        Resets the selection in dropdown if the dropdown's current value
        is equal to the given option
        """
        if dropdown.current_val == option:
            dropdown.reset()

    def _set_style(self) -> None:
        """Sets the layout of the widget"""
        layout = QVBoxLayout()
        for widget in [self._primary_key, self._secondary_key]:
            layout.addWidget(widget)
        self.setLayout(layout)

    def get_selections(self) -> dict[str, str]:
        """Returns the current selctions"""
        if (
            not self._primary_key.current_val
            or not self._secondary_key.current_val
        ):
            return {}
        return {
            'primary': self._primary_key.current_val,
            'secondary': self._secondary_key.current_val
        }


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
        self._area_sorting = SortBy(area_options, 'crags', parent=self)
        self._crag_sorting = SortBy(crag_options, 'routes', parent=self)
        self._set_style()

    def _set_style(self) -> None:
        """Sets the layout of the widget"""
        main_layout = QVBoxLayout()
        main_layout.addWidget(self._title)
        dropdowns = QHBoxLayout()
        for widget in [self._area_sorting, self._crag_sorting]:
            dropdowns.addWidget(widget)
        main_layout.addLayout(dropdowns)
        self.setLayout(main_layout)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)

    def get_selections(self) -> dict[str, str] | None:
        area_options = self._area_sorting.get_selections()
        crag_options = self._crag_sorting.get_selections()

        if not area_options or not crag_options:
            return {}
        return {
            "node": area_options,
            "leaf": crag_options
        }


class ModelOptions(QFrame):
    def __init__(
        self, options: list[str], logistic_coefficient_limits: tuple[int, int],
        *, parent: QWidget
    ) -> None:
        """TODO"""
        super().__init__(parent=parent)
        self._title = HeaderLabel('Model Options', parent=self)
        self._model_options = RadioButtons(options, parent=self)
        self._min_popularity = NumLineEdit(
            'Min Popularity:', 'e.g., 25', min_val=0, max_val=1000, parent=self
        )
        min_val, max_val = logistic_coefficient_limits
        self._trust_slider = Slider(
            min_val=min_val, max_val=max_val, resolution=1000,
            label="Trust Parameter", parent=self
        )
        self._set_style()

    def _set_style(self) -> None:
        """Sets the layout of the widget"""
        layout = QVBoxLayout()
        widgets = [
            self._title, self._model_options, self._min_popularity,
            self._trust_slider
        ]
        for widget in widgets:
            layout.addWidget(widget)
        self.setLayout(layout)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)

    def get_selection(self) -> str:
        """Returns the currently selected model"""
        return self._model_options.current_val

    def get_coefficients(self) -> tuple[float, int]:
        """Returns the currently set coefficents (trust, population)"""
        trust = self._trust_slider.current_val
        min_popularity = self._min_popularity.current_val
        return trust, min_popularity


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
    """.DS_Store"""
    def __init__(self, data_root: Area, *, parent: QWidget):
        super().__init__(parent=parent)
        self._data_root = data_root
        area_options = data_root.node_sort_keys
        crag_options = data_root.leaf_sort_keys
        self._sort_settings = SortingSettings(
            area_options, crag_options, parent=self
        )
        self._data_root.logistic_coefficient_limits
        self._model_options = ModelOptions(
            self._data_root.models,
            self._data_root.logistic_coefficient_limits,
            parent=self
        )
        self._metrics = MetricSelection(
            self._data_root.get_area_metrics(),
            self._data_root.get_crag_metrics(),
            parent=self
        )
        self._apply = QPushButton("Apply")
        self._connect_widgets()
        self._set_style()
        print("Released")

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
        self.setLayout(main_layout)

    def _set_model(self) -> None:
        """Attempts to set the model if selected"""
        model = self._model_options.get_selection()
        if model == 'Logistic':
            trust, popularity = self._model_options.get_coefficients()
            self._data_root.set_ranking_model(model, popularity, trust)
        elif model:
            self._data_root.set_ranking_model(model)

    def _set_sort_keys(self) -> None:
        """Attempts to set the sorting keys if selected"""
        sort_keys = self._sort_settings.get_selections()
        if sort_keys:
            self._data_root.set_sort_keys(sort_keys)
            self._data_root.sort()

    def _set_display_metrics(self) -> None:
        """Attempts to set the display metrics"""
        area_metric, crag_metric = self._metrics.get_selections()
        if area_metric:
            self._data_root.set_area_metric(area_metric)
        if crag_metric:
            self._data_root.set_crag_metric(crag_metric)

    def apply_sort_settings(self) -> None:
        """Applies the current selections to the sort settings"""
        self._set_model()
        self._set_display_metrics()
        self._set_sort_keys()
