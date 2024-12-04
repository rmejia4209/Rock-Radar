from PyQt5.QtWidgets import QWidget, QVBoxLayout

from UI.custom_widgets.labels import TitleLabel


class Settings(QWidget):
    """.DS_Store"""
    def __init__(self, parent: QWidget):
        super().__init__(parent=parent)

    @property
    def title(self):
        return "Settings"

    def _set_style(self) -> None:
        """TODO:"""
        layout = QVBoxLayout()
        layout.addWidget(TitleLabel("Settings", self))
        self.setLayout(layout)
