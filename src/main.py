import sys
from PyQt5.QtWidgets import QApplication
from UI.app import MainWindow
from data.route_builder import build_area_tree


def main():
    """Create an app object and show the window"""
    root = build_area_tree()
    root.init_stats()
    app = QApplication(sys.argv)
    window = MainWindow(root)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
