from PyQt5.QtCore import pyqtSignal

__author__ = 'Nick Apperley'

import os
import openvpn
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLineEdit
from PyQt5 import uic


class ConnectDialog(QDialog):
    vpn_connected = pyqtSignal(object)

    def __init__(self, conf_dir, ovpn_file):
        ui_file = '{}/connect_dialog.ui'.format(os.path.dirname(os.path.abspath(__file__)))

        super().__init__()
        self.conf_dir = conf_dir
        self.ovpn_file = ovpn_file
        uic.loadUi(ui_file, self)
        self._setup_ui()
        self._setup_events()

    def _setup_ui(self):
        btn_box = self.findChild(QDialogButtonBox, 'btn_box')
        connect_btn = btn_box.button(QDialogButtonBox.Ok)

        connect_btn.setText('Connect')

    def _setup_events(self):
        btn_box = self.findChild(QDialogButtonBox, 'btn_box')
        close_btn = btn_box.button(QDialogButtonBox.Close)
        connect_btn = btn_box.button(QDialogButtonBox.Ok)

        connect_btn.clicked.connect(self.connect)
        close_btn.clicked.connect(lambda: self.close())

    def connect(self):
        username = self.findChild(QLineEdit, 'username_txt').text()
        password = self.findChild(QLineEdit, 'password_txt').text()
        process = openvpn.open_vpn_connection(username, password, self.conf_dir, self.ovpn_file)

        self.vpn_connected.emit(process)
        self.close()
