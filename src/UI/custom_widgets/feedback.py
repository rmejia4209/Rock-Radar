from typing import Any, Callable
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QFrame, QPushButton, QLabel, QProgressBar, QHBoxLayout,
    QVBoxLayout
)
from PyQt5.QtCore import QThread, pyqtSignal
from UI.custom_widgets.labels import IconLabel


class _StatusMessage(QFrame):

    def __init__(self, icon_path: str, *, parent: QWidget):
        super().__init__(parent=parent)
        self._icon = IconLabel(icon_path)
        self._label = QLabel()
        self._set_style()

    def _create_layout(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        for widget in [self._icon, self._label]:
            layout.addWidget(widget)
        return layout

    def _set_style(self) -> None:
        layout = self._create_layout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setLayout(layout)

    def set_label_name(self, name: str) -> None:
        self._label.setObjectName(name)

    def set_status(self, text: str) -> None:
        self._label.setText(text)


class ErrorMessage(_StatusMessage):

    def __init__(self, icon_path: str, *, parent: QWidget) -> None:
        super().__init__(icon_path, parent=parent)
        self.set_label_name('ErrorMsgLabel')
        self.setStyleSheet(
            """
                ErrorMessage { border: 2px solid red; }
                QLabel#ErrorMsgLabel { color: red; }
            """
        )


class SuccessMsg(_StatusMessage):
    def __init__(self, msg: str, icon_path: str, *, parent: QWidget) -> None:
        super().__init__(icon_path, parent=parent)
        self.set_label_name('SuccessMsg')
        self.setStyleSheet(
            """
                SuccessMsg { border: 2px solid green; }
                QLabel#SuccessMsg { color: green; }
            """
        )
        self.set_status(msg)


class Worker(QThread):
    """
    Subclass of QThread. This widget

    Attributes:
        _func (Callable[..., int]):
            Generator function that is executed when the run method is called
        _args (Any):
            Arguments passed to the generator function. Must be set prior to
            calling the run method

    Signals:
        progress (pyqtSignal[int]):
            Signal emitted regularly during execution of the function
        progress (pyqtSignal[int]):
            Signal emitted if function raises an error
        success (pyqtSignal[]):
            Signal emitted on successful execution of the function
    """

    _func: Callable[..., int]

    # Signals
    progress = pyqtSignal(int)
    error = pyqtSignal(str)
    success = pyqtSignal()

    def __init__(self, func: Callable[..., int], *, parent: QWidget):
        super().__init__(parent=parent)
        self._func = func

    def set_args(self, *args) -> None:
        """
        Sets the args to be passed to the saved generator during execution.
        Args:
            *args (any): must match the signature of the given function
        """
        self._args = args

    def run(self) -> None:
        """
        Runs the saved generator and regularly emits a progress update.
        If an error is encountered, the error is emitted via the error signal.
        A success signal is emitted on completion.
        """
        nums = list(range(0, 30))
        try:
            for progress in self._func(*nums):  # self._func(*self._args):
                self.progress.emit(progress)
            self.success.emit()
        except Exception as e:
            self.error.emit(str(e))


class ProgressBar(QWidget):
    success = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, func: Callable[..., Any], parent: QWidget) -> None:
        """TODO"""
        super().__init__(parent=parent)
        self._worker = Worker(func, parent=self)
        self._progress_bar = QProgressBar(self)
        self._progress_bar.setRange(0, 100)
        self._connect_widgets()
        self._set_layout()

    def _update_progress(self, val: int) -> None:
        self._progress_bar.setValue(val)

    def _connect_widgets(self) -> None:
        """Connects the children widgets to one another"""
        self._worker.progress.connect(self._update_progress)
        self._worker.error.connect(self.error.emit)
        self._worker.success.connect(self.success.emit)

    def _set_layout(self) -> None:
        layout = QHBoxLayout()
        layout.addWidget(self._progress_bar)
        self.setLayout(layout)

    def start_task(self, *args) -> None:
        self._worker.set_args(*args)
        self._worker.start()
        return
    
    def is_running(self) -> bool:
        """Returns true if the worker is still running"""
        return self._worker.isRunning()


class ButtonWithProgressBar(QWidget):

    finished = pyqtSignal()

    def __init__(
        self, label: str, func: Callable[..., Any], *, error_icon_path: str,
        success_icon_path: str, success_msg: str, parent: QWidget
    ) -> None:
        super().__init__(parent=parent)
        self._progress_bar = ProgressBar(func, parent=self)
        self._button = QPushButton(label, parent=self)
        self._error_msg = ErrorMessage(error_icon_path, parent=self)
        self._success_msg = SuccessMsg(
            success_msg, success_icon_path, parent=self
        )
        self._args = None
        self._connect_widgets()
        self._set_layout()

    def _connect_widgets(self) -> None:
        """TODO"""
        self._button.clicked.connect(self._start_task)
        self._progress_bar.error.connect(self._display_error)
        self._progress_bar.success.connect(self._display_success)

    def _set_layout(self) -> None:
        """TODO"""
        layout = QVBoxLayout()
        widgets = [
            self._progress_bar, self._error_msg, self._success_msg,
            self._button
        ]
        for widget in widgets:
            layout.addWidget(widget)
        self._progress_bar.hide()
        self._error_msg.hide()
        self._success_msg.hide()
        self.setLayout(layout)

    def _display_error(self, msg: str) -> None:
        """
        Displays the error label box with the error message
        and hides the progress bar.
        """
        self._progress_bar.hide()
        self._error_msg.set_status(msg)
        self._error_msg.show()

    def _display_success(self) -> None:
        """Displays the success label box and hides the progress bar."""
        self._progress_bar.hide()
        self._success_msg.show()
        self.finished.emit()

    def _start_task(self) -> None:
        """Starts the task if the args have been set."""
        if not self._args or self._progress_bar.is_running():
            return
        self._error_msg.hide()
        self._success_msg.hide()
        self._progress_bar.show()
        self._progress_bar.start_task(*self._args)

    def set_args(self, *args: Any) -> None:
        """
        Sets the arguments to be passed along to the saved func
        Args:
            *args (any): must match the signature of the given function
        """
        self._args = args

    def is_running(self) -> bool:
        """Returns true if the progress_bar is currently executing a task"""
        return self._progress_bar.is_running()