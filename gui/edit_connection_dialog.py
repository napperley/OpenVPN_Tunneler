__author__ = 'Nick Apperley'

import os
import connections_model
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLineEdit, QLabel
from PyQt5 import uic


class EditConnectionDialog(QDialog):
    # Custom event.
    connection_changed = QtCore.pyqtSignal(str, str)

    def __init__(self, conn_name):
        ui_file = '{}/connection_dialog.ui'.format(os.path.dirname(os.path.abspath(__file__)))

        super().__init__()
        self.old_conn_name = conn_name
        self.conn = connections_model.connections[self.old_conn_name]
        uic.loadUi(ui_file, self)
        self._setup_ui()
        self._setup_events()

    def _setup_ui(self):
        # Must specify a type as the first argument to the findChild method otherwise an error will be thrown.
        btn_layout = self.findChild(QDialogButtonBox, 'btn_layout')

        self.findChild(QLineEdit, 'name_txt').setText(self.old_conn_name)
        self.findChild(QLineEdit, 'addr_txt').setText(self.conn['addr'])
        self.findChild(QLabel, 'title_lbl').setText('Edit Connection')
        btn_layout.setStandardButtons(QDialogButtonBox.Save | QDialogButtonBox.Close)
        self.setWindowTitle('Edit Connection')

    def _setup_events(self):
        # Must specify a type as the first argument to the findChild method otherwise an error will be thrown.
        btn_layout = self.findChild(QDialogButtonBox, 'btn_layout')
        close_btn = btn_layout.button(QDialogButtonBox.Close)
        save_btn = btn_layout.button(QDialogButtonBox.Save)

        save_btn.clicked.connect(self.edit_connection)
        close_btn.clicked.connect(lambda: self.close())

    def edit_connection(self):
        new_conn_name = self.findChild(QLineEdit, 'name_txt').text()
        addr = self.findChild(QLineEdit, 'addr_txt').text()

        connections_model.edit_connection(self.old_conn_name, new_conn_name, addr)
        # Fire the event.
        self.connection_changed.emit(new_conn_name, addr)
        self.close()
