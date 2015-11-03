from PyQt5.QtCore import pyqtSignal

__author__ = 'Nick Apperley'

import os
import openvpn
import colour
import PyQt5.QtCore as QtCore
from PyQt5.QtGui import QRegExpValidator
from invalid_credentials_error import InvalidCredentialsError
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QWidget
from PyQt5 import uic


class ConnectDialog(QDialog):
    # Custom event.
    vpn_connected = pyqtSignal(object)
    # Custom event.
    vpn_login_failed = pyqtSignal()
    # Custom event.
    vpn_conn_timeout = pyqtSignal()

    def __init__(self, conn_name, conf_dir, ovpn_file):
        ui_file = '{}/connect_dialog.ui'.format(os.path.dirname(os.path.abspath(__file__)))

        super().__init__()
        self._fields = ['username_txt', 'password_txt']
        self.conn_name = conn_name
        self.conf_dir = conf_dir
        self.ovpn_file = ovpn_file
        uic.loadUi(ui_file, self)
        self._setup_ui()
        self._setup_events()

    def text_changed(self):
        """
        An event handler that covers a text changed event.
        """
        sender = self.sender()

        if self.findChild(QWidget, sender.objectName()).hasAcceptableInput():
            bg_colour = colour.green
        else:
            bg_colour = colour.red
        sender.setStyleSheet('QLineEdit {{ background-color: {} }}'.format(bg_colour))
        self._validate_dialog()

    def _validate_dialog(self):
        add_btn = self.findChild(QWidget, 'btn_layout').button(QDialogButtonBox.Ok)
        field = None
        valid = True

        for i in self._fields:
            field = self.findChild(QWidget, i)
            if not field.hasAcceptableInput():
                valid = False
                break
        add_btn.setEnabled(valid)

    def _setup_ui(self):
        btn_layout = self.findChild(QWidget, 'btn_layout')
        connect_btn = btn_layout.button(QDialogButtonBox.Ok)
        reg_exp = QtCore.QRegExp(QtCore.QRegExp('([a-zA-Z]{2})(.*)'))

        self.findChild(QWidget, 'username_txt').setValidator(QRegExpValidator(reg_exp))
        self.findChild(QWidget, 'password_txt').setValidator(QRegExpValidator(reg_exp))
        self.findChild(QWidget, 'title_lbl').setText('Connect To {}'.format(self.conn_name))
        connect_btn.setText('Connect')
        connect_btn.setEnabled(False)

    def _setup_events(self):
        btn_layout = self.findChild(QWidget, 'btn_layout')
        close_btn = btn_layout.button(QDialogButtonBox.Close)
        connect_btn = btn_layout.button(QDialogButtonBox.Ok)

        connect_btn.clicked.connect(self.connect)
        self.findChild(QWidget, 'username_txt').textChanged.connect(self.text_changed)
        self.findChild(QWidget, 'password_txt').textChanged.connect(self.text_changed)
        close_btn.clicked.connect(lambda: self.close())

    def connect(self):
        """
        An event handler that opens an OpenVPN connection.
        """
        username = self.findChild(QWidget, 'username_txt').text()
        password = self.findChild(QWidget, 'password_txt').text()

        try:
            self.vpn_connected.emit(openvpn.open_vpn_connection(username, password, self.conf_dir, self.ovpn_file))
        except InvalidCredentialsError:
            self.vpn_login_failed.emit()
        except TimeoutError:
            self.vpn_conn_timeout.emit()
        self.close()
