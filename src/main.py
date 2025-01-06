import sys
import time
from typing import Callable, Any
from PyQt5.QtWidgets import QApplication
from UI.app import MainWindow
from data.route_builder import build_area_tree, build_area_tree_threaded
from parser.parser import build_json_sources
from scraper.scraper import save_area_ids


def start_app():
    """Create an app object and show the window"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


def load_speed_test() -> None:
    """
    Measures the execution time of loading the data using a single thread vs
    multiple threads
    """
    def measure_speed(func: Callable[[], Any], *args) -> int:
        start = time.time()
        func()
        return time.time() - start

    single_thread_time = measure_speed(build_area_tree)
    multi_thread_time = measure_speed(build_area_tree_threaded)
    diff = single_thread_time - multi_thread_time
    percent_change = int((diff / single_thread_time) * 100)

    print(f'1 Thread: {single_thread_time}')
    print(f'Multiple Threads: {multi_thread_time}')
    print(f'Difference: {diff}')
    print(f'Percent Difference: {percent_change}%')
    return


def main(cmd: str):

    if cmd == 'start-app':
        start_app()
    elif cmd == 'get-areas':
        save_area_ids()
    elif cmd == 'save-region':
        pass
    elif cmd == 'build-src-data':
        build_json_sources()
    elif cmd == 'measure-load-speed':
        load_speed_test()


if __name__ == "__main__":
    cmd = 'start-app' if len(sys.argv) == 1 else sys.argv[1]
    main(cmd)
