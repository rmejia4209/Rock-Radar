from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtChart import (
    QChartView, QChart, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis,
    QValueAxis
)
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


class _BaseBarGraph(QChartView):
    """TODO"""
    def __init__(self, data: dict[str, int], *, parent: QWidget):
        super().__init__(parent=parent)
        self._bar_graph = QBarSeries()
        self._bar_set = QBarSet('')
        self._x_axis = QBarCategoryAxis()
        self._y_axis = QValueAxis()
        self._chart = QChart()
        self._add_data_to_bar_graph(data)
        self._set_style(data)

    def _add_data_to_bar_graph(self, data: dict[str, int]) -> None:
        """Adds data to the pie chart"""
        self._bar_set.append([data[key] for key in sorted(data)])
        self._bar_set.setColor(QColor(54, 162, 235))
        self._bar_graph.append(self._bar_set)
        return

    def _format_axes(self, data: dict[str, int]) -> None:
        """Formats the x and y axes of the graph"""
        # Set axes' values
        self._x_axis.append(sorted(data))
        self._y_axis.setRange(0, max(data.values())+2)
        self._y_axis.setLabelFormat("%.0f")

        # Attach to chart and bar series
        self._chart.addAxis(self._y_axis, Qt.AlignLeft)
        self._chart.addAxis(self._x_axis, Qt.AlignBottom)
        self._bar_graph.attachAxis(self._y_axis)
        self._bar_graph.attachAxis(self._x_axis)
        return

    def _style_chart(self, data: dict[str, int]) -> None:
        """Styles the chart"""
        # Add the pie chart to the chart and set animation
        self._chart.addSeries(self._bar_graph)
        self._chart.setAnimationOptions(QChart.SeriesAnimations)
        self._format_axes(data)
        self._chart.legend().setVisible(False)
        return

    def _set_style(self, data: dict[str, int]) -> None:
        """Set the style of the chart view"""
        self._style_chart(data)
        self.setChart(self._chart)
        self.setRenderHint(QPainter.Antialiasing)

    def update_data(self, data: dict[str, int]) -> None:
        """Updates the pie charts current values"""
        self._y_axis.setRange(0, max(data.values())+2)
        for idx, key in enumerate(sorted(data)):
            self._bar_set.replace(idx, data[key])


class _BaseChart(QFrame):
    """TODO"""
    # TODO: UI Issues
    # - Label and chart are not centered
    # - Chart background is white, not off white
    def __init__(
        self, graph_type: str, data: dict[str, int], label: str,
        *, parent: QWidget
    ) -> None:
        """TODO"""
        super().__init__(parent=parent)
        self._graph = self._create_graph(data, graph_type)
        self._label = SmallBoldLabel(label, parent=self)
        self._set_style()

    def _create_graph(
        self, data: dict[str, int], graph_type: str
    ) -> QChartView:
        """Returns a QChartView based on the given graph type"""
        if graph_type == 'bar':
            return _BaseBarGraph(data, parent=self)
        elif graph_type == 'pie':
            return _BasePieChart(data, parent=self)

    def _create_layout(self) -> QVBoxLayout:
        """
        Returns a vertical layout object with the widget's attributes added
        and centered
        """
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        for widget in [self._graph, self._label]:
            layout.addWidget(widget)
        return layout

    def _set_style(self) -> None:
        """Sets the style of the widget"""
        self.setLayout(self._create_layout())
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)

    def update_data(self, data: dict[str, int]) -> None:
        """Updates the data of the pie chart"""
        self._graph.update_data(data)


class PieChart(_BaseChart):
    """TODO"""
    def __init__(
        self, data: dict[str, int], label: str, *, parent: QWidget
    ) -> None:
        """TODO"""
        super().__init__('pie', data, label, parent=parent)


class BarGraph(_BaseChart):
    """TODO"""
    def __init__(
        self, data: dict[str, int], label: str, *, parent: QWidget
    ) -> None:
        """TODO"""
        super().__init__('bar', data, label, parent=parent)
