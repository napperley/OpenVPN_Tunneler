__author__ = 'Nick Apperley'

import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QAction
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        ui_file = '{}/main_window.ui'.format(os.path.dirname(os.path.abspath(__file__)))

        super().__init__()
        uic.loadUi(ui_file, self)
        self.setup_events()
        self.show()

    def setup_events(self):
        # Must specify a type as the first argument to the findChild method otherwise an error will be thrown.
        action_add_conn = self.findChild(QAction, 'action_add_conn')

        action_add_conn.triggered.connect(self.add_connection)

    def add_connection(self):
        # noinspection PyTypeChecker,PyCallByClass
        QMessageBox.information(self, 'OpenVPN Client', 'Adding connection...', QMessageBox.Close)
