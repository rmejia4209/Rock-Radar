import os
from PyQt5.QtWidgets import (
    QWidget, QFrame, QScrollArea, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal, Qt
from UI.custom_widgets.buttons import Link
from UI.custom_widgets.feedback import ButtonWithProgressBar
from UI.custom_widgets.composites import SingleStatDisplay
from scraper.scraper import download_and_merge_data
from custom_types.custom_types import AreaMap


class AreaList(QScrollArea):

    area_selected = pyqtSignal(str)

    def __init__(self, areas: list[str], *, parent: QWidget):
        super().__init__(parent=parent)
        self._container = QWidget(parent=self)
        self._areas = self._create_links(areas)

        self._set_style()

    def _create_links(self, areas: list[str]) -> list[Link]:
        """
        Creates a list of links based on the provided list

        Args:
            areas (list[str]): list of areas

        Returns:
            list[Link]:
                list of Link buttons connected to the area selected signal
        """
        links = []
        for area in areas:
            new_link = Link(area, parent=self._container)
            new_link.clicked.connect(
                lambda state, area=area: self.area_selected.emit(area)
            )
            links.append(new_link)
        return links

    def _set_content_layout(self) -> None:
        """Sets the layout of the content"""
        layout = QVBoxLayout()
        for link in self._areas:
            layout.addWidget(link, alignment=Qt.AlignTop | Qt.AlignLeft)
        layout.addStretch()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self._container.setLayout(layout)

    def _set_style(self) -> None:
        self._set_content_layout()
        # self.setFrameShape(QFrame.NoFrame)
        self.setWidget(self._container)
        self.setWidgetResizable(True)
        return

    def remove_region(self, region: str) -> None:
        """
        Removes the region from the list of areas.

        Args:
            region (str): the name of the region to be removed
        """
        tar_idx = None
        for idx, button in enumerate(self._areas):
            if button.text() == region:
                self._container.layout().removeWidget(button)
                button.clicked.disconnect()
                button.deleteLater()
                tar_idx = idx
        self._areas.pop(tar_idx)


class AreaDownloader(QFrame):

    new_region_added = pyqtSignal(str)

    def __init__(self, available_areas: AreaMap, *, parent: QWidget) -> None:
        super().__init__(parent=parent)

        self._data = available_areas
        self._sidebar = AreaList(list(self._data.keys()), parent=self)
        parent_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'Icons'
        )
        self._num_routes_stat = SingleStatDisplay(
            sum([self._data[region]['routes'] for region in self._data]),
            "Total Number of Routes",
            parent=self
            )
        self._download_button = ButtonWithProgressBar(
            "Download Area",
            download_and_merge_data,
            error_icon_path=os.path.join(parent_dir, 'warning.png'),
            success_icon_path=os.path.join(parent_dir, 'check.png'),
            success_msg='Area successfully downloaded!',
            parent=self
        )
        self._current_region = None
        self._connect_widgets()
        self._set_layout()

    def _connect_widgets(self) -> None:
        """Connects the children to one another"""
        self._sidebar.area_selected.connect(self._update_args)
        self._download_button.finished.connect(self._remove_region)

    def _remove_region(self) -> None:
        """
        Removes the region from the scroll area and resets the stat displayed
        """
        self._sidebar.remove_region(self._current_region)
        del self._data[self._current_region]
        self.new_region_added.emit(self._current_region)
        self._current_region = None
        self._num_routes_stat.update_val(
            sum([self._data[region]['routes'] for region in self._data])
        )
        self._num_routes_stat.update_label('Total Number of Routes')

    def _update_args(self, region: str) -> None:
        """Updates the download buttons args"""
        if not self._download_button.is_running():
            self._download_button.set_args(self._data[region]['id'], region)
            self._current_region = region
            self._num_routes_stat.update_val(self._data[region]['routes'])
            self._num_routes_stat.update_label(f'Number of Routes in {region}')
        return

    def _create_top_layout(self) -> QVBoxLayout:
        """TODO"""
        layout = QHBoxLayout()
        layout.addWidget(self._sidebar, 2)
        layout.addWidget(self._num_routes_stat, 1)
        return layout

    def _set_layout(self) -> None:
        """TODO"""
        layout = QVBoxLayout()
        layout.addLayout(self._create_top_layout())
        layout.addWidget(self._download_button)
        self.setLayout(layout)
