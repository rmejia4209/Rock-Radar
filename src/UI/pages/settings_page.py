from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSignal
from UI.components.area_downloader import AreaDownloader
from UI.components.settings import Settings
from custom_types.crag import Area
from custom_types.custom_types import AreaMap


class SettingsPage(QWidget):
    settings_changed = pyqtSignal()
    new_region_added = pyqtSignal(str)

    def __init__(
        self, data_root: Area, available_areas: AreaMap, *, parent: QWidget
    ) -> None:
        super().__init__(parent=parent)
        self._title = 'Settings'
        self._settings = Settings(data_root, parent=self)
        self._downloader = AreaDownloader(available_areas, parent=self)

        self._connect_widgets()
        self._set_main_layout()

    @property
    def title(self):
        return self._title
    
    def _connect_widgets(self) -> None:
        """
        Connects the children widget's signals to the containers signals
        """
        self._settings.settings_changed.connect(self.settings_changed.emit)
        self._downloader.new_region_added.connect(self.new_region_added.emit)

    def _set_main_layout(self) -> None:
        """Sets the main layout of the page"""
        layout = QVBoxLayout()
        for widget in [self._settings, self._downloader]:
            layout.addWidget(widget)
        self.setLayout(layout)
