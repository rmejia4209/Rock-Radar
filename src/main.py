import sys
from PyQt5.QtWidgets import QApplication
from UI.app import MainWindow
from data.route_builder import (
    build_area_tree, get_areas_available_for_download
)
from parser.parser import build_json_sources
from scraper.scraper import save_area_ids


def start_app():
    """Create an app object and show the window"""
    available_areas = get_areas_available_for_download()
    root = build_area_tree()
    root.init_stats()
    app = QApplication(sys.argv)
    window = MainWindow(root, available_areas)
    window.show()
    app.exec()


def main(cmd: str):

    if cmd == 'start-app':
        start_app()
    elif cmd == 'init-areas':
        save_area_ids()
    elif cmd == 'save-region':
        pass
    elif cmd == 'build-src-data':
        build_json_sources()


if __name__ == "__main__":
    cmd = 'start-app' if len(sys.argv) == 1 else sys.argv[1]
    main(cmd)
