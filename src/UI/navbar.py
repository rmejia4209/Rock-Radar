import os
from PyQt5.QtWidgets import QWidget
from UI.custom_widgets.navigation import DualPageNavBar


class NavBar(DualPageNavBar):
    """.DS_Store"""
    def __init__(self, title: str, parent: QWidget) -> None:
        parent_folder = os.path.join(os.path.dirname(__file__), "Icons")
        file_paths = (
            os.path.join(parent_folder, "gear.png"),
            os.path.join(parent_folder, "home.png")
        )
        super().__init__(title, file_paths, parent=parent)
