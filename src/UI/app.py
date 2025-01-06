# from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QStackedLayout
import qdarktheme
from UI.navbar import NavBar
from UI.home import Home
from UI.pages.settings_page import SettingsPage
from custom_types.crag import Area
from data.route_builder import (
    build_area_tree, build_subtree, get_region_fp,
    get_areas_available_for_download
)
from parser.parser import build_json_sources


class MainWindow(QMainWindow):
    """
    TODO: write doc string
    """
    _root: Area
    _navbar: NavBar
    _home: Home
    _settings: SettingsPage

    def __init__(self) -> None:
        """TODO: write doc string"""
        super().__init__()
        self._root = self._build_tree()

        self._navbar = NavBar(f"{self._root.name}", parent=self)
        self._home = Home(self._root, parent=self)
        self._settings = SettingsPage(
            self._root, get_areas_available_for_download(), parent=self
        )

        self._connect_widgets()
        self._pages_layout = QStackedLayout()
        self._set_style()
        self.setCentralWidget(self._build_widget())
        return

    def _build_tree(self) -> Area:
        """
        Returns the root of the data tree.
        TODO: added threaded version

        Returns:
            Area: root of the areas
        """
        root = build_area_tree()
        root.init_stats()
        return root

    def _connect_widgets(self) -> None:
        """Connects the signals of the widget's children to different slots"""
        self._navbar.page_changed.connect(lambda idx: self._change_page(idx))
        self._settings.settings_changed.connect(self._home.refresh_data)
        self._settings.new_region_added.connect(self._add_region)
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
        self.setFixedSize(1200, 900)
        qdarktheme.enable_hi_dpi()
        qdarktheme.setup_theme("light")
        return

    def _set_pages_layout(self) -> None:
        """TODO"""
        for page in [self._home, self._settings]:
            self._pages_layout.addWidget(page)
        return

    def _create_main_layout(self,) -> QVBoxLayout:
        """"""
        self._set_pages_layout()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self._navbar)
        main_layout.addLayout(self._pages_layout)
        main_layout.setSpacing(0)

        return main_layout

    def _add_region(self, region: str) -> None:
        """
        Builds a json source file for the given region and adds the region to
        the data root. Refreshes the data via calling _home's refresh_data
        method.

        Args:
            region (str): name of the region
        """
        build_json_sources([region])
        subtree = build_subtree(get_region_fp(region))

        if subtree.name == 'USA':
            state = subtree.children[0]
            for country in self._root.children:
                if country.name == 'USA':
                    state.parent = country
                    country.add_child(state)
                    break
        else:
            subtree.parent = self._root
            self._root.add_child(subtree)
        self._root.init_stats()
        self._home.refresh_data()
        return

    def _build_widget(self) -> QWidget:
        widget = QWidget()
        widget.setLayout(self._create_main_layout())
        return widget
