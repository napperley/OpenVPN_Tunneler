__author__ = 'Nick Apperley'

import os
import connections_model
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLineEdit, QLabel, QFileDialog, QPushButton
from PyQt5 import uic


class EditConnectionDialog(QDialog):
    # Custom event.
    connection_changed = QtCore.pyqtSignal(str, str, str)

    def __init__(self, username, conn_name):
        ui_file = '{}/connection_dialog.ui'.format(os.path.dirname(os.path.abspath(__file__)))

        super().__init__()
        self.username = username
        self.old_conn_name = conn_name
        self.conn = connections_model.connections[self.old_conn_name]
        uic.loadUi(ui_file, self)
        self._setup_ui()
        self._setup_events()

    def _setup_ui(self):
        # Must specify a type as the first argument to the findChild method otherwise an error will be thrown.
        btn_layout = self.findChild(QDialogButtonBox, 'btn_layout')

        self.findChild(QLineEdit, 'name_txt').setText(self.old_conn_name)
        self.findChild(QLineEdit, 'conf_dir_txt').setText(self.conn['conf-dir'])
        self.findChild(QLineEdit, 'ovpn_file_txt').setText(self.conn['ovpn-file'])
        self.findChild(QLabel, 'title_lbl').setText('Edit Connection')
        btn_layout.setStandardButtons(QDialogButtonBox.Save | QDialogButtonBox.Close)
        self.setWindowTitle('Edit Connection')

    def _setup_events(self):
        # Must specify a type as the first argument to the findChild method otherwise an error will be thrown.
        btn_layout = self.findChild(QDialogButtonBox, 'btn_layout')
        close_btn = btn_layout.button(QDialogButtonBox.Close)
        save_btn = btn_layout.button(QDialogButtonBox.Save)
        ovpn_file_btn = self.findChild(QPushButton, 'ovpn_file_btn')
        conf_dir_btn = self.findChild(QPushButton, 'conf_dir_btn')

        save_btn.clicked.connect(self.edit_connection)
        close_btn.clicked.connect(lambda: self.close())
        ovpn_file_btn.clicked.connect(self.select_ovpn_file)
        conf_dir_btn.clicked.connect(self.select_conf_dir)

    def select_ovpn_file(self):
        filter = 'OVPN File (*.ovpn)'
        file_pos = 0
        base_dir = '/home/{}'.format(self.username)
        title = 'Select OVPN File'
        dialog_input = QFileDialog().getOpenFileName(self, title, base_dir, filter)
        ovpn_file_txt = self.findChild(QLineEdit, 'ovpn_file_txt')

        if dialog_input[file_pos] != '':
            ovpn_file_txt.setText(dialog_input[file_pos])

    def select_conf_dir(self):
        base_dir = '/home/{}'.format(self.username)
        title = 'Select Configuration Directory'
        dialog_input = QFileDialog().getExistingDirectory(self, title, base_dir)
        conf_dir_txt = self.findChild(QLineEdit, 'conf_dir_txt')

        if dialog_input != '':
            conf_dir_txt.setText(dialog_input)

    def edit_connection(self):
        new_conn_name = self.findChild(QLineEdit, 'name_txt').text()
        conf_dir = self.findChild(QLineEdit, 'conf_dir_txt').text()
        ovpn_file = self.findChild(QLineEdit, 'ovpn_file_txt').text()

        connections_model.edit_connection(self.old_conn_name, new_conn_name, conf_dir, ovpn_file)
        # Fire the event.
        self.connection_changed.emit(new_conn_name, conf_dir, ovpn_file)
        self.close()
