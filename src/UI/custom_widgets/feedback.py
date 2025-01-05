from typing import Any, Callable
from PyQt5.QtWidgets import QWidget, QProgressBar, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal


class Worker(QThread):
    progress = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(self, func: Callable[..., Any], *, parent: QWidget):
        super().__init__()
        self._func = func

    def set_args(self, *args) -> None:
        print('Set Args')
        self._args = args

    def run(self) -> None:
        try:
            for progress in self._func(*self._args):
                self.progress.emit(progress)
        except Exception as e:
            self.error.emit(str(e))


class ProgressBar(QWidget):

    def __init__(self, func: Callable[..., Any], parent: QWidget) -> None:
        """TODO"""
        super().__init__(parent=parent)
        self._worker = Worker(func, parent=self)
        self._progress_bar = QProgressBar(self)
        self._progress_bar.setRange(0, 100)

        self._connect_widgets()
        self._set_layout()

    def _update_progress(self, val: int) -> None:
        print(f'getting {val}')
        self._progress_bar.setValue(val)

    def _connect_widgets(self) -> None:
        """Connects the children widgets to one another"""
        self._worker.progress.connect(self._update_progress)

    def _set_layout(self) -> None:
        layout = QHBoxLayout()
        layout.addWidget(self._progress_bar)
        self.setLayout(layout)

    def start_task(self, *args) -> None:
        self._worker.set_args(*args)
        self._worker.start()
        return