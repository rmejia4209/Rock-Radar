from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtChart import QChartView, QChart, QPieSeries
from UI.custom_widgets.labels import SmallBoldLabel


class _BasePieChart(QChartView):
    """TODO"""
    _colors: list[QColor] = [
        QColor(255, 99, 132),  # Red
        QColor(54, 162, 235),  # Blue
        QColor(75, 192, 192),  # Green
    ]

    def __init__(self, data: dict[str, int], *, parent: QWidget):
        super().__init__(parent=parent)
        self._pie_chart = QPieSeries()
        self._add_data_to_pie(data)
        self._chart = QChart()
        self._set_style()

    def _add_data_to_pie(self, data) -> None:
        """Adds data to the pie chart"""
        for label, val in data.items():
            self._pie_chart.append(label, val)

    def _style_chart(self) -> None:
        """Styles the chart"""
        # Add the pie chart to the chart and set animation
        self._chart.addSeries(self._pie_chart)
        self._chart.setAnimationOptions(QChart.SeriesAnimations)

        # Style the legend of the pie chart
        legend = self._chart.legend()
        legend.setAlignment(Qt.AlignRight)
        legend.setMarkerShape(legend.MarkerShapeCircle)
        return

    def _set_style(self) -> None:
        """Set the style of the chart view"""

        for pie_slice, color in zip(
            self._pie_chart.slices(), _BasePieChart._colors
        ):
            pie_slice.setBrush(color)
        self._style_chart()
        self.setChart(self._chart)
        self.setRenderHint(QPainter.Antialiasing)

    def update_data(self, data: dict[str, int]) -> None:
        """Updates the pie charts current values"""
        for idx, pie_slice in enumerate(self._pie_chart.slices()):
            pie_slice.setValue(data[pie_slice.label()])


class PieChart(QFrame):
    """TODO"""
    # TODO: UI Issues
    # - Label and chart are not centered
    # - Chart background is white, not off white
    def __init__(
        self, data: dict[str, int], label: str, *, parent: QWidget
    ) -> None:
        """TODO"""
        super().__init__(parent=parent)
        self._pie_chart = _BasePieChart(data, parent=self)
        self._label = SmallBoldLabel(label, parent=self)
        self._set_style()

    def _create_layout(self) -> QVBoxLayout:
        """
        Returns a vertical layout object with the widget's attributes added
        and centered
        """
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        for widget in [self._pie_chart, self._label]:
            layout.addWidget(widget)
        return layout

    def _set_style(self) -> None:
        """Sets the style of the widget"""
        self.setLayout(self._create_layout())
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)

    def update_data(self, data: dict[str, int]) -> None:
        """Updates the data of the pie chart"""
        self._pie_chart.update_data(data)
