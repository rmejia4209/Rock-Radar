from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtCore import QSize
# from UI.custom_UI.labels import RegularLabel


class Link(QPushButton):
    """
    A basic button without a border and underline text. Used to
    resemble a link.
    """
    def __init__(self, text: str, *, tip: str, parent: QWidget) -> None:
        """
        Initialize the widget.
        Args:
            txt (str): Text to be displayed by button
            tip (str): Button's tooltip displayed when hovered
            parent (QWidget): The parent of the widget
        """
        super().__init__(text=text, parent=parent)
        self.setToolTip(tip)
        self._set_style(tip)
        return

    def _set_style(self, tip: str) -> None:
        """Set the font of the link"""
        font = QFont()
        font.setPointSize(14)
        font.setUnderline(True)
        self.setFont(font)
        self.setStyleSheet("border: none;")
        return


class Icon(QPushButton):
    """QPushButton with QIcon as the button"""
    def __init__(
        self, icon_path: str, *, size: tuple[int, int] = (50, 50),
        parent: QWidget | None = None
    ) -> None:
        """
        # TODO:
        """
        super().__init__(parent=parent)

        icon = QIcon(icon_path)
        self.setIcon(icon)
        w, h = size
        self.setIconSize(QSize(w, h))
        self.setStyleSheet("border:none;")
        self.setFixedSize(w+5, h+5)
        return


class ButtonWithIcon(QPushButton):
    """
    A basic button without a border and underline text. Used to
    resemble a link.
    """
    def __init__(self, txt: str, fp: str, parent: QWidget) -> None:
        """
        Initialize the widget.
        Args:
            txt (str): Text to be displayed by button
        """
        super().__init__(txt, parent=parent)
        self.setIcon(QIcon(fp))
        return
