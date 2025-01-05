# from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIntValidator  # QFont
from PyQt5.QtWidgets import (
    QWidget, QFrame, QComboBox, QRadioButton, QVBoxLayout, QHBoxLayout,
    QSlider, QLineEdit, QCheckBox
)
from PyQt5.QtCore import Qt, pyqtSignal

from UI.custom_widgets.labels import SmallLabel


class _BaseDropDown(QComboBox):
    """
    Wrapper for the base QComboBox. This widget accepts a list of any type
    and adds the objects to the drop down. The objects should have
    a valid __str__ defined in order to be rendered properly.
    """
    def __init__(self, vals: list[any], txt: str, parent: QWidget) -> None:
        """
        Args:
            vals (list[any]): Options for the dropdown(__str__ must be defined)
            txt (str): Placeholder text when an option is not selected
            parent (QWidget): The parent of the widget
        """
        super().__init__(parent=parent)
        self.setPlaceholderText(txt)
        self._add_items(vals)

    def _add_items(self, vals: list[any]) -> None:
        """Adds the items to the valid options for the drop down"""
        for item in vals:
            self.addItem(str(item), item)

    def _set_val(self, val: any) -> None:
        """
        Sets the current data to val if val is a valid option. Useful for
        returning to the previous state after the options have been updated.
        """
        if val is None:
            return
        for idx in range(self.count()):
            if val == self.itemData(idx):
                self.setCurrentIndex(idx)
        return

    def update_items(self, vals: list[any]) -> None:
        """
        Clears the current options and adds the given options. Attempts to
        set current value back to the previous value if it is a valid option.
        """
        current_val = self.currentData()
        self.clear()
        self._add_items(vals)
        self._set_val(current_val)
        return


class DropDown(QFrame):
    """
    Public Dropdown widget. This widget has a custom signal that emits the
    currently selected **object** when the selection has been changed.
    This widget also has a label above the dropdown.

    Attributes:
        _drop_down (_BaseDropDown):
            The dropdown of this widget.
        _emit_data (bool):
            A boolean used to prevent the emission of a signal when the
            options are updated.

    Signals:
        item_changed (pyqtSignal):
            emit's the currently selected data after the selection has changed.
    """
    item_changed: pyqtSignal = pyqtSignal(object)
    _dropdown: _BaseDropDown
    _emit_data: bool

    def __init__(
        self, vals: list[any], label: str, place_holder_txt: str,
        parent: QWidget
    ) -> None:
        """
        Args:
            vals (list[any]): Options for dropdown (__str__ must be defined).
            label (str): The widget's label.
            place_holder_txt (str): The dropdown's placeholder text.
            parent (QWidget): The parent of the widget.
        """
        super().__init__(parent=parent)

        self._dropdown = _BaseDropDown(vals, place_holder_txt, parent=self)
        self._dropdown.currentIndexChanged.connect(self._emit_current_data)
        self._emit_data = True
        self._set_style(label)
        return

    def _emit_current_data(self) -> None:
        """Emits the item_changed signal if _emit_data is set to True"""
        if self._emit_data:
            self.item_changed.emit(self._dropdown.currentData())
        return

    def _set_style(self, label) -> None:
        """Sets the layout/style of the widget"""
        layout = QVBoxLayout()
        for widget in [SmallLabel(label, parent=self), self._dropdown]:
            layout.addWidget(widget)
        layout.setSpacing(0)
        self.setLayout(layout)

    @property
    def current_val(self) -> any:
        """Returns the dropdown's current value"""
        return self._dropdown.currentData()

    def reset(self) -> None:
        self._dropdown.setCurrentIndex(-1)

    def update_items(self, vals: list[any]) -> None:
        """
        Update's the dropdowns options with the given values. Prevents
        the emission item_changed signal during the update.
        """
        self._emit_data = False
        self._dropdown.update_items(vals)
        self._emit_data = True


class RadioButtons(QFrame):
    """TODO"""
    _options: list[QRadioButton]

    def __init__(
        self, options: str, *, orient_horizontally: bool = False,
        parent: QWidget
    ) -> None:
        """TODO"""
        super().__init__(parent=parent)
        self._current_val = None
        self._create_radio_buttons(options)
        self._set_style(orient_horizontally)

    def _create_radio_buttons(self, options) -> None:
        """TODO:
        creates radio buttons and connects them
        """
        self._options = []
        for option in options:
            self._options.append(
                QRadioButton(option.capitalize(), parent=self)
            )

    def _set_style(self, orient_horizontally) -> None:
        layout = QHBoxLayout() if orient_horizontally else QVBoxLayout()
        for option in self._options:
            layout.addWidget(option)
        self.setLayout(layout)

    @property
    def current_val(self) -> str | None:
        """TODO: does what you think it does"""
        for option in self._options:
            if option.isChecked():
                return option.text()


class BaseSlider(QSlider):
    """TODO:"""
    def __init__(
        self, *, min_val: int | float, max_val: int | float, parent: QWidget,
        resolution: int | None = None
    ) -> None:
        super().__init__(Qt.Horizontal, parent=parent)
        self._set_limits(min_val, max_val, resolution)
        return

    @staticmethod
    def _calculate_resolution(min_val):
        """Calculates the resolution"""
        if isinstance(min_val, int):
            return 1
        return 10 * len(str(min_val).split('.')[1])

    def _set_limits(
        self, min_val: int | float, max_val: int | float,
        resolution: int | None
    ) -> None:
        """Sets the limits of the slider"""
        if resolution is None:
            self._resolution = BaseSlider._calculate_resolution(min_val)
        else:
            self._resolution = resolution

        self.setMinimum(int(min_val * self._resolution))
        self.setMaximum(int(max_val * self._resolution))
        return

    @property
    def current_val(self) -> float:
        """Returns the current value divided by the multiple"""
        return self.value() / self._resolution


class Slider(QWidget):
    """TODO:"""
    def __init__(
        self, *, min_val: int | float, max_val: int | float, label: str,
        parent: QWidget, resolution: int | None = None
    ) -> None:
        super().__init__(parent=parent)
        self._slider = BaseSlider(
            min_val=min_val, max_val=max_val, resolution=resolution,
            parent=self
        )
        self._set_style(label)
        return

    def _set_style(self, label: str) -> None:
        """TODO"""
        layout = QHBoxLayout()
        layout.addWidget(SmallLabel(label, parent=self))
        layout.addWidget(self._slider)
        self.setLayout(layout)

    @property
    def current_val(self) -> float:
        """Returns the current value divided by the multiple"""
        return self._slider.current_val


class BaseNumLineEdit(QLineEdit):
    """TODO"""
    def __init__(
        self, *, example_txt: str, min_val: int, max_val: int, parent: QWidget
    ) -> None:
        """TODO"""
        super().__init__(parent=parent)
        self.setPlaceholderText(example_txt)
        self.setValidator(QIntValidator(min_val, max_val))
        return

    @property
    def current_val(self) -> int | None:
        """Returns the current value"""
        if self.text():
            return int(self.text())
        return


class NumLineEdit(QFrame):
    """TODO"""
    def __init__(
        self, label: str, example_txt: str, min_val: str, max_val: int,
        *, parent: QWidget
    ) -> None:
        super().__init__(parent=parent)
        self._num_input = BaseNumLineEdit(
            example_txt=example_txt, min_val=min_val, max_val=max_val,
            parent=self
        )
        self._set_style(label)

    def _set_style(self, label: str) -> None:
        """TODO"""
        layout = QHBoxLayout()
        layout.addWidget(SmallLabel(label, parent=self))
        layout.addWidget(self._num_input)
        self.setLayout(layout)
        return

    @property
    def current_val(self) -> int:
        """Returns the current value"""
        return self._num_input.current_val


class Checkboxes(QFrame):
    def __init__(
        self, options: list[str], *, orient_horizontally: bool = True,
        checkall: bool = False, parent: QWidget
    ) -> None:
        super().__init__(parent=parent)
        self._create_checkboxes(options)
        self._set_style(orient_horizontally)
        if checkall:
            self.select_all()

    def _create_checkboxes(self, options: list[str]) -> None:
        """Creates the checkboxes based on the options"""
        self._options = []
        for option in options:
            self._options.append(QCheckBox(option))
        return

    def _set_style(self, orient_horizontally: bool) -> None:
        """Sets the layout of the checkboxes"""
        layout = QHBoxLayout() if orient_horizontally else QVBoxLayout()
        for option in self._options:
            layout.addWidget(option)
        self.setLayout(layout)

    def select_all(self) -> None:
        """Sets the checked state of all options to true"""
        for option in self._options:
            option.setChecked(True)

    @property
    def current_vals(self) -> list[str]:
        """Returns the currently selected values"""
        return [
            option.text() for option in self._options if option.isChecked()
        ]
