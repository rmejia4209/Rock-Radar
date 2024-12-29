from PyQt5.QtWidgets import (
    QWidget, QFrame, QHBoxLayout, QVBoxLayout, QPushButton
)
from PyQt5.QtCore import pyqtSignal
from UI.custom_widgets.inputs import DropDown, NumLineEdit, Checkboxes
from custom_types.crag import Grade, RouteFilterWidget


class GradeDropDown(DropDown):
    """
    Wrapper for the base DropDown class that has climbing grades. This widget
    prefills the placeholder text, keeps a list of valid grade options, and
    handles updating valid options based on a min or max grade input.

    Attributes:
        _grades (list[Grade]): list of all common grades

    Signals:
        item_changed (SignalInstance): unaltered from base class

    """
    _grades: list[Grade] = Grade.get_all_common_grades()

    def __init__(self, label: str, parent: QWidget) -> None:
        """
        Args:
            label (str): The label of the dropdown.
            parent (QWidget): The parent of the widget.
        """
        place_holder_txt = "Please Select Grade"
        super().__init__(
            type(self)._grades, label, place_holder_txt, parent=parent
        )

    @property
    def grade(self) -> Grade | None:
        """
        Returns the current grade selected or None if a grade
        has not been selected.
        """
        return self.current_val

    def _find_idx(self, grade_bound: Grade) -> int:
        """
        Returns the index of the matching grade in _grades
        """
        for idx, grade in enumerate(type(self)._grades):
            if grade_bound == grade:
                return idx

    def update_min(self, min_grade: Grade) -> None:
        """
        Removes the lower grades from the list of valid options
        (i.e., removes grades from index 0 to index start)
        """
        start = self._find_idx(min_grade)
        self.update_items(type(self)._grades[start:])

    def update_max(self, max_grade: Grade) -> None:
        """
        Removes the upper grades from the list of valid options
        (i.e., removes grades from index end+1 to len(_grades))
        """
        end = self._find_idx(max_grade)
        self.update_items(type(self)._grades[:end+1])


class RouteFilterWidget(QFrame):
    """
    TODO
    """
    _route_filter: RouteFilterWidget
    _min_grade: GradeDropDown
    _max_grade: GradeDropDown
    _route_types: Checkboxes
    _min_length: NumLineEdit
    _min_num_pitches: NumLineEdit
    _apply: QPushButton
    filter_updated = pyqtSignal()

    def __init__(
        self, route_filter: RouteFilterWidget, parent: QWidget
    ) -> None:
        super().__init__(parent=parent)

        self._route_filter = route_filter
        self._min_grade = GradeDropDown(label="Minimum Grade", parent=self)
        self._max_grade = GradeDropDown(label="Maximum Grade", parent=self)
        self._route_types = Checkboxes(
            self._route_filter.available_route_types,
            orient_horizontally=False, checkall=True, parent=self
        )
        self._min_length = NumLineEdit(
            'Minimum Length (ft):', 'e.g., 100', 0, 30000, parent=self
        )
        self._min_num_pitches = NumLineEdit(
            'Minimum Number of Pitches', 'e.g., 4', 0, 6000, parent=self
        )
        self._apply = QPushButton("Apply")
        self._connect_widgets()
        self._set_style()

    def _connect_widgets(self) -> None:
        self._min_grade.item_changed.connect(
            lambda grade: self._max_grade.update_min(grade)
        )
        self._max_grade.item_changed.connect(
            lambda grade: self._min_grade.update_max(grade)
        )
        self._apply.clicked.connect(self.update_filter)

    def _create_row(self, widgets: list[QWidget]) -> QHBoxLayout:
        """Returns a horizontal layout with the given widgets"""
        layout = QHBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)
        layout.setSpacing(0)
        return layout

    def _build_left_side(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        widget_rows = [
            [self._min_grade, self._max_grade],
            [self._min_length, self._min_num_pitches]
        ]
        for widget_row in widget_rows:
            layout.addLayout(self._create_row(widget_row))
        layout.setSpacing(0)
        return layout

    def _build_top(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.addLayout(self._build_left_side())
        layout.addWidget(self._route_types)
        layout.setSpacing(0)
        return layout

    def _set_style(self) -> None:
        layout = QVBoxLayout()
        layout.addLayout(self._build_top())
        layout.addWidget(self._apply)
        layout.setSpacing(5)
        self.setLayout(layout)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)

    def update_filter(self) -> None:
        """Updates _route_filter based on the current inputs"""
        lower_grade = self._min_grade.grade
        upper_grade = self._max_grade.grade
        if lower_grade:
            self._route_filter.lower_grade = lower_grade
        if upper_grade:
            self._route_filter.upper_grade = upper_grade

        min_len = self._min_length.current_val
        min_num_pitches = self._min_num_pitches.current_val
        self._route_filter.set_min_length(min_len if min_len else 0)
        self._route_filter.set_min_num_pitches(
            min_num_pitches if min_num_pitches else 0
        )

        self._route_filter.set_route_types(self._route_types.curret_vals)
        self.filter_updated.emit()
