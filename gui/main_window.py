__author__ = 'Nick Apperley'

import os
import connections_model
import openvpn
from gui.add_connection_dialog import AddConnectionDialog
from gui.edit_connection_dialog import EditConnectionDialog
from gui.connect_dialog import ConnectDialog
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QTableWidgetItem, QMessageBox, QWidget
from PyQt5 import uic


class MainWindow(QMainWindow):
    name_col = 0
    addr_col = 1

    def __init__(self, username):
        ui_file = '{}/main_window.ui'.format(os.path.dirname(os.path.abspath(__file__)))

        super().__init__()
        self.username = username
        self.vpn_process = None
        uic.loadUi(ui_file, self)
        self._setup_ui()
        self._setup_events()

    def _setup_ui(self):
        pos = 0
        header = ['Connection Name', 'OVPN File']
        tbl = self.findChild(QWidget, 'connections_tbl')

        self.statusBar().showMessage('Not connected to a VPN')
        tbl.setHorizontalHeaderLabels(header)
        connections_model.load_connections(self.username)
        tbl.setRowCount(len(connections_model.connections))
        for key, i in connections_model.connections.items():
            tbl.setItem(pos, MainWindow.name_col, QTableWidgetItem(key))
            tbl.setItem(pos, MainWindow.addr_col, QTableWidgetItem(i['ovpn-file']))
        tbl.resizeColumnsToContents()

    def _setup_events(self):

        self.findChild(QAction, 'add_conn_action').triggered.connect(self.show_add_connection_dialog)
        self.findChild(QAction, 'edit_conn_action').triggered.connect(self.show_edit_connection_dialog)
        self.findChild(QAction, 'remove_conn_action').triggered.connect(self.remove_connection)
        self.findChild(QAction, 'connect_action').triggered.connect(self.toggle_connection)

    def toggle_connection(self):
        """
        An event handler that toggles the VPN connection state (connected/disconnected).
        """
        connect_action = self.findChild(QAction, 'connect_action')

        if connect_action.text() == 'Connect':
            self._connect_vpn()
        else:
            self._disconnect_vpn()

    def _disconnect_vpn(self):
        connect_action = self.findChild(QAction, 'connect_action')

        openvpn.close_vpn_connection(self.vpn_process)
        self.vpn_process = None
        self.statusBar().showMessage('Disconnected')
        connect_action.setText('Connect')

    def _connect_vpn(self):
        no_selection = -1
        tbl = self.findChild(QWidget, 'connections_tbl')
        connection = {}
        dialog = None
        conn_name = ''

        if tbl.currentRow() != no_selection:
            conn_name = tbl.item(tbl.currentRow(), MainWindow.name_col).text()
            connection = connections_model.connections[conn_name]
            dialog = ConnectDialog(conn_name, connection['conf-dir'], connection['ovpn-file'])
            dialog.vpn_connected.connect(self.vpn_connected)
            dialog.vpn_login_failed.connect(
                lambda: self.statusBar().showMessage('Invalid VPN username and/or password'))
            dialog.vpn_conn_timeout.connect(lambda: self.statusBar().showMessage('Cannot connect to OpenVPN server'))
            dialog.show()

    def vpn_connected(self, vpn_process):
        """
        An event handler for the vpn_connected event.
        :param vpn_process: OS process that manages the OpenVPN connection.
        """
        connect_action = self.findChild(QAction, 'connect_action')

        self.vpn_process = vpn_process
        self.statusBar().showMessage('Connected')
        connect_action.setText('Disconnect')

    def show_add_connection_dialog(self):
        """
        An event handler that shows the Add Connection dialog box.
        """
        dialog = AddConnectionDialog(self.username)

        dialog.connection_added.connect(self.add_connection)
        dialog.show()

    def show_edit_connection_dialog(self):
        """
        An event handler that shows the Edit Connection dialog box.
        """
        no_selection = -1
        tbl = self.findChild(QWidget, 'connections_tbl')

        if tbl.currentRow() != no_selection:
            dialog = EditConnectionDialog(self.username, tbl.item(tbl.currentRow(), MainWindow.name_col).text())
            dialog.connection_changed.connect(self.edit_connection)
            dialog.show()

    def center(self):
        # noinspection PyArgumentList
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())

    def add_connection(self, conn_name, conf_dir, ovpn_file):
        """
        An event handler that adds a new connection.
        :param conn_name: Unique name of the connection.
        :param conf_dir: Path to the configuration directory.
        :param ovpn_file: Path to the OpenVPN configuration file.
        """
        tbl = self.findChild(QWidget, 'connections_tbl')

        tbl.setRowCount(tbl.rowCount() + 1)
        tbl.setItem(tbl.rowCount() - 1, MainWindow.name_col, QTableWidgetItem(conn_name))
        tbl.setItem(tbl.rowCount() - 1, MainWindow.addr_col, QTableWidgetItem(ovpn_file))
        tbl.resizeColumnsToContents()

    def edit_connection(self, conn_name, conf_dir, ovpn_file):
        """
        An event handler that edits a connection.
        :param conn_name: Unique name of the connection.
        :param conf_dir: Path to the configuration directory.
        :param ovpn_file: Path to the OpenVPN configuration file.
        """
        tbl = self.findChild(QWidget, 'connections_tbl')
        current_row = tbl.currentRow()

        tbl.item(current_row, MainWindow.name_col).setText(conn_name)
        tbl.item(current_row, MainWindow.addr_col).setText(ovpn_file)
        tbl.resizeColumnsToContents()

    def remove_connection(self):
        """
        An event handler that removes a connection.
        """
        no_selection = -1
        tbl = self.findChild(QWidget, 'connections_tbl')
        title = 'OpenVPN Client'
        msg = 'Remove selected row'
        dialog_result = None

        if tbl.currentRow() != no_selection:
            # noinspection PyCallByClass,PyTypeChecker
            dialog_result = QMessageBox.question(self, title, msg, QMessageBox.Yes | QMessageBox.No)
            if dialog_result == QMessageBox.Yes:
                connections_model.remove_connection(tbl.item(tbl.currentRow(), MainWindow.name_col).text())
                tbl.removeRow(tbl.currentRow())
