__author__ = 'Nick Apperley'

import os
import connections_model
import colour
import PyQt5.QtCore as QtCore
from PyQt5.QtGui import QValidator, QRegExpValidator
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QWidget
from PyQt5 import uic


class EditConnectionDialog(QDialog):
    # Custom event.
    connection_changed = QtCore.pyqtSignal(str, str, str)

    def __init__(self, username, conn_name):
        ui_file = '{}/connection_dialog.ui'.format(os.path.dirname(os.path.abspath(__file__)))

        super().__init__()
        self._fields = ['name_txt']
        self.username = username
        self.old_conn_name = conn_name
        self.conn = connections_model.connections[self.old_conn_name]
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
        save_btn = self.findChild(QWidget, 'btn_layout').button(QDialogButtonBox.Save)
        field = None
        valid = True

        for i in self._fields:
            field = self.findChild(QWidget, i)
            if not field.hasAcceptableInput():
                valid = False
                break
        save_btn.setEnabled(valid)

    def _setup_ui(self):
        btn_layout = self.findChild(QWidget, 'btn_layout')
        conn_name = self.findChild(QWidget, 'name_txt')
        conn_name_validator = QRegExpValidator(conn_name)

        conn_name_validator.setRegExp(QtCore.QRegExp('([a-zA-Z]{2})(.*)'))
        conn_name.setValidator(conn_name_validator)
        self.findChild(QWidget, 'name_txt').setText(self.old_conn_name)
        self.findChild(QWidget, 'conf_dir_txt').setText(self.conn['conf-dir'])
        self.findChild(QWidget, 'ovpn_file_txt').setText(self.conn['ovpn-file'])
        self.findChild(QWidget, 'title_lbl').setText('Edit Connection')
        btn_layout.setStandardButtons(QDialogButtonBox.Save | QDialogButtonBox.Close)
        self.setWindowTitle('Edit Connection')

    def _setup_events(self):
        btn_layout = self.findChild(QWidget, 'btn_layout')

        btn_layout.button(QDialogButtonBox.Save).clicked.connect(self.edit_connection)
        btn_layout.button(QDialogButtonBox.Close).clicked.connect(lambda: self.close())
        self.findChild(QWidget, 'ovpn_file_btn').clicked.connect(self.select_ovpn_file)
        self.findChild(QWidget, 'conf_dir_btn').clicked.connect(self.select_conf_dir)
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

    def edit_connection(self):
        """
        An event handler that edits a connection.
        """
        new_conn_name = self.findChild(QWidget, 'name_txt').text()
        conf_dir = self.findChild(QWidget, 'conf_dir_txt').text()
        ovpn_file = self.findChild(QWidget, 'ovpn_file_txt').text()

        connections_model.edit_connection(self.old_conn_name, new_conn_name, conf_dir, ovpn_file)
        # Fire the event.
        self.connection_changed.emit(new_conn_name, conf_dir, ovpn_file)
        self.close()
