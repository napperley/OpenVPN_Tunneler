__author__ = 'Nick Apperley'

import json
import os
import shutil
import stat

model_file = ''
connections = None


def load_connections(username):
    """
    Loads all connections from the model (JSON file) for the specified user into memory.
    :type username: str
    :param username: Name of the user.
    """
    global model_file
    global connections
    read_mode = 'r'

    if connections is None:
        model_file = '/home/{}/.openvpn_tunneler/connections.json'.format(username)
        _create_model(username)
        with open(model_file, read_mode):
            connections = json.load(open(model_file, read_mode))


def _save_connections():
    write_mode = 'w'

    if connections is not None:
        with open(model_file, write_mode) as f:
            json.dump(connections, f)


def _create_model(username):
    append = 'w+'
    # Use the following mode: u=rwx, g=rx, o-rwx
    permission_mode = stat.S_IRWXU | stat.S_IRGRP + stat.S_IXGRP | 00

    if not os.path.exists(model_file):
        _create_conf_dir(username)
        with open(model_file, append) as f:
            f.write('{\n')
            f.write('}\n')
        os.chmod(model_file, permission_mode)
        shutil.chown(model_file, user=username, group=username)


def _create_conf_dir(username):
    conf_dir = '/home/{}/.openvpn_tunneler'.format(username)
    # Use the following mode: u=rwx, g=rx, o-rwx
    mode = stat.S_IRWXU | stat.S_IRGRP + stat.S_IXGRP | 00

    if not os.path.exists(conf_dir):
        os.mkdir(conf_dir, mode)
        shutil.chown(conf_dir, user=username, group=username)


def add_connection(conn_name, conf_dir, ovpn_file):
    """
    Adds a new connection to the model.
    :type conn_name: str
    :type conf_dir: str
    :type ovpn_file: str
    :param conn_name:  Connection name.
    :param conf_dir:  Path to the configuration directory.
    :param ovpn_file: Path to the OVPN file.
    """
    if connections is not None:
        connections[conn_name] = {'conf-dir': conf_dir, 'ovpn-file': ovpn_file}
        _save_connections()


def edit_connection(old_conn_name, new_conn_name, conf_dir, ovpn_file):
    """
    Changes an existing connection in the model.
    :type old_conn_name: str
    :type new_conn_name: str
    :type conf_dir: str
    :type ovpn_file: str
    :param old_conn_name: Old connection name.
    :param new_conn_name: New connection name.
    :param conf_dir: Path to the configuration directory.
    :param ovpn_file: Path to the OVPN file.
    """
    if connections is not None:
        del connections[old_conn_name]
        connections[new_conn_name] = {'conf-dir': conf_dir, 'ovpn-file': ovpn_file}
        _save_connections()


def remove_connection(conn_name):
    """
    Removes an existing connection from the model.
    :type conn_name: str
    :param conn_name: Connection name.
    """
    if connections is not None:
        del connections[conn_name]
        _save_connections()
