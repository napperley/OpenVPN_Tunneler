__author__ = 'Nick Apperley'

import os
import connections_model
import colour
import PyQt5.QtCore as QtCore
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QDialog, QFileDialog, QWidget, QDialogButtonBox
from PyQt5 import uic


class AddConnectionDialog(QDialog):
    # Custom event.
    connection_added = QtCore.pyqtSignal(str, str, str)

    def __init__(self, username):
        ui_file = '{}/connection_dialog.ui'.format(os.path.dirname(os.path.abspath(__file__)))

        super().__init__()
        self.username = username
        self._fields = ['name_txt', 'conf_dir_txt', 'ovpn_file_txt']
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
        conn_name = self.findChild(QWidget, 'name_txt')
        root_reg_ex = QtCore.QRegExp('(/)(.*)')
        conn_name_reg_ex = QtCore.QRegExp('([a-zA-Z]{2})(.*)')
        conf_dir_txt = self.findChild(QWidget, 'conf_dir_txt')
        ovpn_file_txt = self.findChild(QWidget, 'ovpn_file_txt')
        add_btn = self.findChild(QWidget, 'btn_layout').button(QDialogButtonBox.Ok)

        conf_dir_txt.setValidator(QRegExpValidator(root_reg_ex, conf_dir_txt))
        ovpn_file_txt.setValidator(QRegExpValidator(root_reg_ex, ovpn_file_txt))
        add_btn.setText('Add')
        add_btn.setEnabled(False)
        conn_name.setValidator(QRegExpValidator(conn_name_reg_ex, conn_name))

    def _setup_events(self):
        btn_layout = self.findChild(QWidget, 'btn_layout')

        self.findChild(QWidget, 'ovpn_file_btn').clicked.connect(self.select_ovpn_file)
        self.findChild(QWidget, 'conf_dir_btn').clicked.connect(self.select_conf_dir)
        btn_layout.button(QDialogButtonBox.Ok).clicked.connect(self.add_connection)
        btn_layout.button(QDialogButtonBox.Close).clicked.connect(lambda: self.close())
        self.findChild(QWidget, 'name_txt').textChanged.connect(self.text_changed)

    def select_ovpn_file(self):
        """
        An event handler that displays a Open File dialog box to get the path to the OpenVPN configuration file.
        """
        file_type_filter = 'OVPN File (*.ovpn)'
        file_pos = 0
        base_dir = '/home/{}'.format(self.username)
        title = 'Select OVPN File'
        dialog_input = QFileDialog().getOpenFileName(self, title, base_dir, file_type_filter)
        ovpn_file_txt = self.findChild(QWidget, 'ovpn_file_txt')

        if dialog_input[file_pos] != '':
            ovpn_file_txt.setText(dialog_input[file_pos])
            self._validate_dialog()

    def select_conf_dir(self):
        """
        An event handler that displays a Choose Directory dialog box to get the path to the configuration directory.
        """
        base_dir = '/home/{}'.format(self.username)
        title = 'Select Configuration Directory'
        dialog_input = QFileDialog().getExistingDirectory(self, title, base_dir)
        conf_dir_txt = self.findChild(QWidget, 'conf_dir_txt')

        if dialog_input != '':
            conf_dir_txt.setText(dialog_input)
            self._validate_dialog()

    def add_connection(self):
        """
        An event handler that adds a new connection.
        """
        conn_name = self.findChild(QWidget, 'name_txt').text()
        conf_dir = self.findChild(QWidget, 'conf_dir_txt').text()
        ovpn_file = self.findChild(QWidget, 'ovpn_file_txt').text()

        connections_model.add_connection(conn_name, conf_dir, ovpn_file)
        # Fire the event.
        self.connection_added.emit(conn_name, conf_dir, ovpn_file)
        self.close()
