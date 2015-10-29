__author__ = 'Nick Apperley'

import os
import connections_model
from gui.add_connection_dialog import AddConnectionDialog
from gui.edit_connection_dialog import EditConnectionDialog
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5 import uic


class MainWindow(QMainWindow):
    name_col = 0
    addr_col = 1

    def __init__(self, username):
        ui_file = '{}/main_window.ui'.format(os.path.dirname(os.path.abspath(__file__)))

        super().__init__()
        self.username = username
        uic.loadUi(ui_file, self)
        self._setup_ui()
        self._setup_events()

    def _setup_ui(self):
        pos = 0
        header = ['Connection Name', 'Address']
        # Must specify a type as the first argument to the findChild method otherwise an error will be thrown.
        tbl = self.findChild(QTableWidget, 'connections_tbl')

        tbl.setHorizontalHeaderLabels(header)
        connections_model.load_connections(self.username)
        tbl.setRowCount(len(connections_model.connections))
        for key, i in connections_model.connections.items():
            tbl.setItem(pos, MainWindow.name_col, QTableWidgetItem(key))
            tbl.setItem(pos, MainWindow.addr_col, QTableWidgetItem(i['addr']))
        tbl.resizeColumnsToContents()

    def _setup_events(self):
        # Must specify a type as the first argument to the findChild method otherwise an error will be thrown.
        add_conn_action = self.findChild(QAction, 'add_conn_action')
        # Must specify a type as the first argument to the findChild method otherwise an error will be thrown.
        remove_conn_action = self.findChild(QAction, 'remove_conn_action')
        # Must specify a type as the first argument to the findChild method otherwise an error will be thrown.
        edit_conn_action = self.findChild(QAction, 'edit_conn_action')

        add_conn_action.triggered.connect(self.show_add_connection_dialog)
        edit_conn_action.triggered.connect(self.show_edit_connection_dialog)
        remove_conn_action.triggered.connect(self.remove_connection)

    def show_add_connection_dialog(self):
        dialog = AddConnectionDialog()

        dialog.connection_added.connect(self.add_connection)
        dialog.show()

    def show_edit_connection_dialog(self):
        no_selection = -1
        tbl = self.findChild(QTableWidget, 'connections_tbl')

        if tbl.currentRow() != no_selection:
            dialog = EditConnectionDialog(tbl.item(tbl.currentRow(), MainWindow.name_col).text())
            dialog.connection_changed.connect(self.edit_connection)
            dialog.show()

    def center(self):
        # noinspection PyArgumentList
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())

    # Event handler (listener).
    def add_connection(self, conn_name, addr):
        tbl = self.findChild(QTableWidget, 'connections_tbl')

        tbl.setRowCount(tbl.rowCount() + 1)
        tbl.setItem(tbl.rowCount() - 1, MainWindow.name_col, QTableWidgetItem(conn_name))
        tbl.setItem(tbl.rowCount() - 1, MainWindow.addr_col, QTableWidgetItem(addr))
        tbl.resizeColumnsToContents()

    # Event handler (listener).
    def edit_connection(self, conn_name, addr):
        tbl = self.findChild(QTableWidget, 'connections_tbl')
        current_row = tbl.currentRow()

        tbl.item(current_row, MainWindow.name_col).setText(conn_name)
        tbl.item(current_row, MainWindow.addr_col).setText(addr)
        tbl.resizeColumnsToContents()

    def remove_connection(self):
        no_selection = -1
        tbl = self.findChild(QTableWidget, 'connections_tbl')
        title = 'OpenVPN Client'
        msg = 'Remove selected row'
        dialog_input = None

        if tbl.currentRow() != no_selection:
            # noinspection PyCallByClass,PyTypeChecker
            dialog_input = QMessageBox.question(self, title, msg, QMessageBox.Yes | QMessageBox.No)
            if dialog_input == QMessageBox.Yes:
                connections_model.remove_connection(tbl.item(tbl.currentRow(), MainWindow.name_col).text())
                tbl.removeRow(tbl.currentRow())
