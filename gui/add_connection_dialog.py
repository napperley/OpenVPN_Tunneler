__author__ = 'Nick Apperley'

import os
import connections_model
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLineEdit
from PyQt5 import uic


class AddConnectionDialog(QDialog):
    # Custom event.
    connection_added = QtCore.pyqtSignal(str, str)

    def __init__(self):
        ui_file = '{}/connection_dialog.ui'.format(os.path.dirname(os.path.abspath(__file__)))

        super().__init__()
        uic.loadUi(ui_file, self)
        self._setup_ui()
        self._setup_events()

    def _setup_ui(self):
        # Must specify a type as the first argument to the findChild method otherwise an error will be thrown.
        btn_layout = self.findChild(QDialogButtonBox, 'btn_layout')
        add_btn = btn_layout.button(QDialogButtonBox.Ok)

        add_btn.setText('Add')

    def _setup_events(self):
        # Must specify a type as the first argument to the findChild method otherwise an error will be thrown.
        btn_layout = self.findChild(QDialogButtonBox, 'btn_layout')
        close_btn = btn_layout.button(QDialogButtonBox.Close)
        add_btn = btn_layout.button(QDialogButtonBox.Ok)

        add_btn.clicked.connect(self.add_connection)
        close_btn.clicked.connect(lambda: self.close())

    def add_connection(self):
        conn_name = self.findChild(QLineEdit, 'name_txt').text()
        addr = self.findChild(QLineEdit, 'addr_txt').text()

        connections_model.add_connection(conn_name, addr)
        # Fire the event.
        self.connection_added.emit(conn_name, addr)
        self.close()
