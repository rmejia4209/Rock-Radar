# from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QStackedLayout
import qdarktheme
from UI.navbar import NavBar
from UI.home import Home
from UI.settings import Settings
from custom_types.node import Node
# TODO: add data def & management here
# TODO: add signal/slot to update node changes


class MainWindow(QMainWindow):
    """
    TODO: write doc string
    """
    _data: Node
    _navbar: NavBar
    _home: Home
    _settings: Settings

    def __init__(
        self, data_root: Node, available_areas: dict[str, dict[str, str | int]]
    ) -> None:
        """TODO: write doc string"""
        super().__init__()
        self._data = data_root
        self._navbar = NavBar(f"{self._data.name}", parent=self)
        self._home = Home(data_root, parent=self)
        self._settings = Settings(data_root, available_areas, parent=self)
        self._connect_widgets()

        self._pages_layout = QStackedLayout()
        self._set_style()
        self.setCentralWidget(self._build_widget())
        return

    def _connect_widgets(self) -> None:
        """Connects the signals of the widget's children to different slots"""
        self._navbar.page_changed.connect(lambda idx: self._change_page(idx))
        self._settings.settings_changed.connect(self._home.refresh_data)
        self._home.node_changed.connect(
            lambda title: self._navbar.update_title(title)
        )
        return

    def _change_page(self, idx) -> None:
        """Changes the current page in view"""
        self._pages_layout.setCurrentIndex(idx)
        self._navbar.update_title(
            self._home.title if idx == 0 else self._settings.title
        )

    def _set_style(self) -> None:
        """Customize the widgets displayed by the app"""
        # title & size
        self.setWindowTitle("Rock Radar")
        # self.setFixedSize(800, 400)
        qdarktheme.enable_hi_dpi()
        qdarktheme.setup_theme("light")
        return

    def _set_pages_layout(self) -> None:
        """TODO"""
        for page in [self._home, self._settings]:
            self._pages_layout.addWidget(page)
        return

    def _create_main_layout(self,) -> QVBoxLayout:
        """TODO: write doc string"""
        self._set_pages_layout()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self._navbar)
        main_layout.addLayout(self._pages_layout)
        main_layout.setSpacing(0)

        return main_layout

    def _build_widget(self) -> QWidget:
        widget = QWidget()
        widget.setLayout(self._create_main_layout())
        return widget
