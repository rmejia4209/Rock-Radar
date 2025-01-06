from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QLabel


class Label(QLabel):
    """
    A Label widget that allows the font size and style to specified. While
    it can be used alone, its best to use an ancestor widget for consistency.
    """
    def __init__(
        self, txt: str, *, size: int = 14, underlined: bool = False,
        bold: bool = False, parent: QWidget
    ) -> None:
        """
        Args:
            txt (str): Text to be displayed
            size (int): Font size
            underlined (bool): Underlined setting
            bold (bool): Bold setting
            parent (QWidget): The parent of the widget
        """
        super().__init__(txt, parent=parent)
        self._set_style(size, underlined, bold)
        return

    def _set_style(self, size: int, underlined: bool, bold: bool) -> None:
        """Sets the style based on the provided arguments"""
        font = QFont()
        font.setPointSize(size)
        font.setUnderline(underlined)
        font.setBold(bold)
        self.setFont(font)
        return

    def update_text(self, text: str) -> None:
        """Wrapper method to update the text"""
        self.setText(text)


class TitleLabel(Label):
    """Label with a bold font size of 24pts"""
    def __init__(self, txt: str, parent: QWidget) -> None:
        super().__init__(txt, size=36, bold=True, parent=parent)


class HeaderLabel(Label):
    """Label with a bold font size of 16pts"""
    def __init__(self, txt: str, parent: QWidget) -> None:
        super().__init__(txt, size=16, bold=True, parent=parent)


class ExtraLargeLabel(Label):
    """Label with a bold font size of 36pts"""
    def __init__(self, txt: str, parent: QWidget) -> None:
        super().__init__(txt, size=36, bold=True, parent=parent)


class SmallBoldLabel(Label):
    """Label with a bold font size of 12pts"""
    def __init__(self, txt: str, parent: QWidget) -> None:
        super().__init__(txt, size=12, bold=True, parent=parent)


class SmallLabel(Label):
    """Label with a bold font size of 12pts"""
    def __init__(self, txt: str, parent: QWidget) -> None:
        super().__init__(txt, size=12, parent=parent)


class RegularLabel(Label):
    """Label with a font size of 14pts"""
    def __init__(self, txt: str, parent: QWidget) -> None:
        super().__init__(txt, size=14, bold=False, parent=parent)


class IconLabel(QLabel):
    """TODO"""
    def __init__(
        self, icon_path: str, *, size: tuple[int, int] = (50, 50),
        parent: QWidget | None = None
    ) -> None:
        """TODO"""
        super().__init__(parent=parent)

        icon = QIcon(icon_path)
        self.setPixmap(icon.pixmap(*size))
        return
