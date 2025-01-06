from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout
from PyQt5.QtCore import Qt
from UI.custom_widgets.labels import ExtraLargeLabel, SmallBoldLabel


class SingleStatDisplay(QFrame):
    """
    A widget that is composed of an extra large label and a small label.
    Used to display a singular piece of data. Number can be updated via
    the update method

    Attributes:
        _number (ExtraLargeLabel): label for number
        _label (SmallLabel): label for description
    """
    _number: ExtraLargeLabel
    _label: SmallBoldLabel

    def __init__(self, num: int, label: str, parent: QWidget):
        """
        Args:
            num (int): The number passed to the _number attribute
            label (str): The text passed to the _label attribute
            parent (QWidget): The parent of the widget
        """
        super().__init__(parent=parent)
        self._number = ExtraLargeLabel(str(num), parent=self)
        self._label = SmallBoldLabel(label, parent=self)
        self._set_style()

    def _create_layout(self) -> QVBoxLayout:
        """
        Returns a vertical layout object with the widget's attributes added
        and centered.
        """
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        for widget in [self._number, self._label]:
            layout.addWidget(widget)
        return layout

    def _set_style(self) -> None:
        """Set's the layout of the widget and adds a border"""
        self.setLayout(self._create_layout())
        # TODO: fix UI later
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)

    def update_val(self, val: int) -> None:
        """Updates the number displayed"""
        self._number.setText(str(val))

    def update_label(self, text: str) -> None:
        """Updates the label"""
        self._label.update_text(text)
