# from PyQt5.QtCore import QSize
# from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QFrame, QComboBox, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

from UI.custom_widgets.labels import SmallBoldLabel


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
        for widget in [SmallBoldLabel(label, parent=self), self._dropdown]:
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
