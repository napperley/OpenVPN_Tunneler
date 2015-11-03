__author__ = 'Nick Apperley'

import sys
from gui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication


def _main():
    # Must assign an instance of QApplication to a variable otherwise a Segmentation Fault will occur.
    app = QApplication(sys.argv)
    # Must assign an instance of MainWindow to a variable otherwise the main window won't display.
    main_window = MainWindow(sys.argv[1])

    main_window.show()
    # Keep the program running.
    sys.exit(app.exec_())


if __name__ == '__main__':
    _main()
